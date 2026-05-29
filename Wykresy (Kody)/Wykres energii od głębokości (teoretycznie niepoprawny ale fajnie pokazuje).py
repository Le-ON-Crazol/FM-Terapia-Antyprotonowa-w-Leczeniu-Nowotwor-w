import numpy as np
import plotly.graph_objects as go

# 1. Definicja osi X (głębokość w tkance w cm)
x = np.linspace(0, 25, 1000)

# 2. Definicja zasięgów do interaktywnego slidera
zasiegi = [5, 10, 15, 20]
widocznosc_sladow = len(zasiegi) * 3 # Po 3 krzywe dla każdego zasięgu

# Inicjalizacja wykresu
fig = go.Figure()

# 3. Generowanie danych i dodawanie krzywych dla każdego zasięgu
for R0 in zasiegi:
    
    # --- PROTON ---
    # Przybliżenie odwrotności pierwiastka (1 / sqrt(R0 - x + epsilon))
    d_proton = np.where(x < R0, 1.0 / np.sqrt(R0 - x + 0.1), 0)
    # Wygładzenie i uformowanie piku na końcu
    d_proton += 3.5 * np.exp(-((x - R0)**2) / (2 * 0.2**2))
    d_proton = (d_proton / np.max(d_proton)) * 100 # Normalizacja do 100%
    
    # --- ANTYPROTON ---
    # Baza protonowa + gigantyczny pik anihilacji (rozkład Gaussa)
    pik_anihilacji = 200 * np.exp(-((x - R0)**2) / (2 * 0.15**2))
    d_antyproton = d_proton + pik_anihilacji
    
    # --- POZYTON ---
    # Zanik wykładniczy z efektem narastania dawki tuż pod skórą
    mu = 0.15 # Współczynnik osłabienia
    k = 3.0   # Współczynnik narastania
    d_pozyton = 100 * (1 - np.exp(-k * x)) * np.exp(-mu * x)
    
    # Ustawiamy widoczność domyślną na zasięg 15 cm
    is_visible = (R0 == 15)
    
    fig.add_trace(go.Scatter(x=x, y=d_antyproton, visible=is_visible, 
                             name=f'Antyproton', line=dict(color='#ff3333', width=3)))
                             
    fig.add_trace(go.Scatter(x=x, y=d_proton, visible=is_visible, 
                             name=f'Proton', line=dict(color='#3399ff', width=3)))
                             
    fig.add_trace(go.Scatter(x=x, y=d_pozyton, visible=is_visible, 
                             name=f'Pozyton (Brak piku)', line=dict(color='#33cc33', width=3, dash='dash')))

# 4. Logika slidera (przełączanie widoczności odpowiednich śladów)
steps = []
for i, R0 in enumerate(zasiegi):
    step = dict(
        method="update",
        args=[{"visible": [False] * widocznosc_sladow}],
        label=f"{R0} cm"
    )
    # Włączenie widoczności tylko dla 3 cząstek przypisanych do wybranego zasięgu
    step["args"][0]["visible"][i*3] = True     # Antyproton
    step["args"][0]["visible"][i*3+1] = True   # Proton
    step["args"][0]["visible"][i*3+2] = True   # Pozyton
    steps.append(step)

sliders = [dict(
    active=2, # Domyślnie pozycja odpowiadająca 15 cm
    currentvalue={"prefix": "Głębokość guza (celowany zasięg wiązki): "},
    pad={"t": 50},
    steps=steps
)]

# 5. Formatowanie interfejsu (Layout)
fig.update_layout(
    title='Symulacja Zdeponowanej Dawki Energii w Tkance',
    xaxis_title='Głębokość w ciele pacjenta [cm]',
    yaxis_title='Dawka względna / Destruktywność [%]',
    sliders=sliders,
    template='plotly_dark', # Ciemny motyw dla lepszego kontrastu
    hovermode='x unified',
    legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
)

# Renderowanie wykresu w domyślnej przeglądarce internetowej
fig.show()