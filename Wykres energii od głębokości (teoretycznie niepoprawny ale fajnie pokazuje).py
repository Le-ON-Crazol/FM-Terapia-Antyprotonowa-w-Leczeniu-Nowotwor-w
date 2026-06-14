import cv2
import numpy as np
import matplotlib.pyplot as plt

def image_to_fx(image_path, stopien_wielomianu=5):
    # 1. Wczytanie i binarizacja (tak samo jak wcześniej)
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Nie znaleziono pliku!")
        return

    _, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if not contours:
        return

    main_contour = max(contours, key=cv2.contourArea)

    # 2. Wyciągnięcie współrzędnych
    x_raw = main_contour[:, 0, 0]
    y_raw = -main_contour[:, 0, 1] 

    # 3. KLUCZOWE: Sortowanie punktów wzdłuż osi X
    # Aby y = f(x) miało sens, X muszą narastać monotonicznie
    sort_idx = np.argsort(x_raw)
    x = x_raw[sort_idx]
    y = y_raw[sort_idx]

    # 4. Aproksymacja wielomianowa (Metoda Najmniejszych Kwadratów)
    # np.polyfit zwraca wektor współczynników [a_n, a_{n-1}, ..., a_0]
    wspolczynniki = np.polyfit(x, y, stopien_wielomianu)
    
    # Tworzymy obiekt wielomianu do łatwego liczenia wartości
    wielomian = np.poly1d(wspolczynniki)

    # 5. Generowanie ładnego wzoru funkcji jako tekst
    # Formatujemy liczby z notacji naukowej na czytelne, krótkie ułamki
    wzor_str = "f(x) = "
    for i, wsp in enumerate(wspolczynniki):
        potega = stopien_wielomianu - i
        znak = " + " if wsp >= 0 and i > 0 else " " if i==0 else " - "
        wsp_abs = abs(wsp)
        
        # Omijamy wyświetlanie zerowych współczynników
        if wsp_abs < 1e-10: 
            continue
            
        if potega > 1:
            wzor_str += f"{znak}{wsp_abs:.4e} * x^{potega}"
        elif potega == 1:
            wzor_str += f"{znak}{wsp_abs:.4e} * x"
        else:
            wzor_str += f"{znak}{wsp_abs:.4e}"

    print("-" * 50)
    print("WYGENEROWANY WZÓR FUNKCJI:")
    print(wzor_str)
    print("-" * 50)

    # 6. Wizualizacja i sprawdzenie jakości dopasowania
    # Generujemy płynną dziedzinę X do wyrysowania naszej wyliczonej funkcji
    x_plot = np.linspace(min(x), max(x), 1000)
    y_plot = wielomian(x_plot)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'ro', markersize=1, label='Piksele rysunku (posortowane)', alpha=0.3)
    plt.plot(x_plot, y_plot, 'b-', linewidth=2, label=f'Aproksymacja f(x) (stopień {stopien_wielomianu})')
    
    plt.title('Dopasowanie funkcji f(x) do rysunku')
    plt.legend()
    plt.grid(True)
    plt.show()

# Wywołaj skrypt (pamiętaj, rysunek nie może mieć zawijasów "w lewo")
# stopien_wielomianu określa elastyczność funkcji (np. 5 do 15)
image_to_fx("C:\\Users\\leonv\\Desktop\\I3U.png", stopien_wielomianu=50)

# Wywołanie funkcji - wystarczy podstawić nazwę swojego pliku!
# Najlepiej narysować coś w Paincie, np. pętlę albo symbol nieskończoności.
# image_to_function("C:\\Users\\leonv\\Desktop\\I3U.png")