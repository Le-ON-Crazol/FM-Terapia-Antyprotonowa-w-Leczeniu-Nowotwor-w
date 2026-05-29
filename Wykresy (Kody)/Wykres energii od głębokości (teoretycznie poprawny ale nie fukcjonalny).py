import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. STAŁE FIZYCZNE (dla tkanki jako wody)
# ==========================================
m_e_c2 = 0.511        # Energia spoczynkowa elektronu [MeV]
m_p_c2 = 938.27       # Energia spoczynkowa protonu/antyprotonu [MeV]
I = 75e-6             # Średni potencjał jonizacyjny wody [MeV]
Z_A = 0.555           # Stosunek liczby atomowej do masowej dla wody (Z/A)
K = 0.307             # Stała proporcjonalności [MeV * cm^2 / mol]
rho = 1.0             # Gęstość wody [g/cm^3]
C = K * Z_A * rho     # Współczynnik materiałowy

# ==========================================
# 2. RÓWNANIE BETHEGO-BLOCHA (Zdolność hamowania)
# ==========================================
def bethe_bloch(E_kin):
    """Oblicza stratę energii dE/dx dla danej energii kinetycznej."""
    # Jeśli energia jest ekstremalnie mała, równanie przestaje działać (brak relatywizmu)
    if E_kin < 0.01:
        return 0.0
    
    # Przeliczanie energii kinetycznej na zmienne relatywistyczne
    gamma = (E_kin + m_p_c2) / m_p_c2
    beta2 = 1.0 - (1.0 / gamma**2)
    
    if beta2 <= 0: return 0.0
    
    # T_max - maksymalna energia przekazana elektronowi w jednym zderzeniu
    licznik_T = 2 * m_e_c2 * beta2 * gamma**2
    mianownik_T = 1 + 2 * gamma * (m_e_c2 / m_p_c2) + (m_e_c2 / m_p_c2)**2
    T_max = licznik_T / mianownik_T
    
    # Implementacja Wzoru [1] z dokumentu LaTeX
    czlon_logarytmiczny = 0.5 * np.log((2 * m_e_c2 * beta2 * gamma**2 * T_max) / (I**2))
    
    # Pełny wzór dE/dx
    dE_dx = C * (1.0 / beta2) * (czlon_logarytmiczny - beta2)
    return dE_dx

# ==========================================
# 3. SYMULACJA I CAŁKOWANIE (Metoda Eulera)
# ==========================================
E_poczatkowa = 150.0  # Początkowa energia wiązki [MeV]
dx = 0.02             # Krok symulacji w centymetrach (Delta x)

# Zmienne śledzące w pętli
E_aktualna = E_poczatkowa
x_aktualne = 0.0

glebokosci = []
zdeponowana_dawka = []

# Pętla działa, dopóki cząstka ma energię
while E_aktualna > 0.01:
    # 1. Obliczamy, ile energii traci w tym punkcie
    strata = bethe_bloch(E_aktualna)
    
    if strata <= 0:
        break
        
    # Zapisujemy wyniki do list
    glebokosci.append(x_aktualne)
    zdeponowana_dawka.append(strata)
    
    # 2. Aktualizujemy stan cząstki (zabieramy energię, przesuwamy w głąb)
    E_aktualna = E_aktualna - (strata * dx)
    x_aktualne = x_aktualne + dx

# Ostatnia wartość 'x_aktualne' to matematycznie wyliczony zasięg (R)
Zasieg_R = x_aktualne 

# ==========================================
# 4. DODANIE KOMPONENTU ANIHILACJI (Wzór 3 z LaTeX)
# ==========================================
# Przekształcamy listy na tablice numpy dla łatwiejszych obliczeń
x_array = np.array(glebokosci)
dawka_protonu = np.array(zdeponowana_dawka)

# Parametry anihilacji
E_anihilacji = 150.0   # Część energii w MeV zostająca lokalnie
sigma = 0.15           # Rozmycie piku
pik_anihilacji = (E_anihilacji / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x_array - Zasieg_R)**2) / (2 * sigma**2))

# Całkowita dawka antyprotonu
dawka_antyprotonu = dawka_protonu + pik_anihilacji

# ==========================================
# 5. GENEROWANIE WYKRESU
# ==========================================
plt.figure(figsize=(10, 6))

plt.plot(x_array, dawka_protonu, label="Proton (Tylko Bethe-Bloch)", color="blue", linewidth=2)
plt.plot(x_array, dawka_antyprotonu, label="Antyproton (Bethe-Bloch + Anihilacja)", color="red", linewidth=2)

plt.title(f"Rozkład dawki na głębokości (Energia wiązki = {E_poczatkowa} MeV)\nWyliczony zasięg: {Zasieg_R:.2f} cm")
plt.xlabel("Głębokość w tkance [cm]")
plt.ylabel("Zdolność hamowania dE/dx [MeV/cm]")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.xlim(0, Zasieg_R + 1)

plt.show()
