import random
import csv, os
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.ion()

from logic import uruchom_algorytm, opcja_selekcji
from visualization import pokaz_najlepsza_trase, pokaz_animacje


def run_once(n_miast, p_mut, elite_pct, seed, limit_pokolen=40, tolerancja=None, log_csv="wyniki_ruletka.csv"):
    import csv, os, time
    random.seed(seed)
    osobniki = n_miast * 10          # populacja = 10 × N
    p_cross  = 1 - p_mut

    wynik = uruchom_algorytm(
        l_miast       = n_miast,
        osobniki      = osobniki,
        limit_pokolen     = limit_pokolen,
        p_mutacji     = p_mut,
        p_krzyzowania = p_cross,
        elitarna      = max(1, int(osobniki * elite_pct)),
        r_selekcja    = opcja_selekcji.ruletka,
        obszar        = dict(x_min=0, y_min=0, x_max=600, y_max=300),
        tolerancja    = tolerancja
    )

    (best_route, best_len, cities,
     best_each, best_best, mean_list, worst_list,
     gens_run) = wynik

    norm_len = best_len / n_miast
    best_gen = best_best.index(best_len) + 1

    row = dict(
        n_miast=n_miast,
        pop=osobniki,
        limit_pokolen=limit_pokolen,
        p_mut=p_mut,
        p_cross=p_cross,
        elite_pct=elite_pct,
        best_len=round(best_len, 2),
        dl_na_miasto=round(norm_len, 3),
        best_gen=best_gen,
        gen_run=gens_run,
        seed=seed,
        tolerancja=tolerancja,
        czas_s=round(time.process_time(), 3)
    )

    file_exists = os.path.isfile(log_csv)
    with open(log_csv, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=row.keys(), delimiter=";")
        if not file_exists:
            w.writeheader()
        w.writerow(row)

    return row




def main():
    # Parametry algorytmu
    l_miast = 40
    osobniki = 150
    pokolenie = 10
    p_mutacji = 0.1
    p_krzyzowania = 1-p_mutacji
    elitarna = 6
    r_selekcja = opcja_selekcji.ranking

    obszar = {"x_min": 0, "y_min": 0, "x_max": 600, "y_max": 300}
    random.seed(409892)


    start_time = time.time()
    najlepszy_osobnik, najlepsza_ocena, miasta, najlepsze_osobniki, najlepsze_wyniki, srednie_wyniki, najgorsze_wyniki,generacja = uruchom_algorytm(
        l_miast, osobniki, pokolenie, p_mutacji, p_krzyzowania, elitarna, r_selekcja, obszar
    )
    end_time = time.time()
    norm_len = najlepsza_ocena / l_miast
    najlepsza_gen = najlepsze_wyniki.index(najlepsza_ocena) + 1
    print(f"""Parametry algorytmu:
      - Liczba miast: {l_miast}
      - Liczebność populacji: {osobniki}
      - Liczba pokoleń: {pokolenie}
      - Prawdopodobieństwo mutacji: {p_mutacji}
      - Prawdopodobieństwo krzyżowania: {p_krzyzowania}
      - Elitarna selekcja: {elitarna} najlepszych osobników
      - Metoda selekcji: {r_selekcja.value}
      
      """)

    print(f"""Najlepsza trasa: {najlepszy_osobnik}
        Długość: {najlepsza_ocena:.2f}
        Czas działania: {end_time - start_time:.2f}s
        Najlepsza generacja: {najlepsza_gen}
        Algorytm zatrzymał się po {generacja} pokoleniach
        
    """)

    # -------------- zapis do CSV -----------------------------------
    wiersz = dict(
        n_miast=l_miast,
        populacja=osobniki,
        limit_pokolen=pokolenie,
        pokolenia_wykonane=generacja,
        p_mut=p_mutacji,
        p_krzyz=p_krzyzowania,
        elita_proc=elitarna / osobniki,
        najlepsza_dlugosc=najlepsza_ocena,
        dl_na_miasto=norm_len,
        najlepsza_gen=najlepsza_gen,
        czas_s=round(end_time - start_time, 3),
        seed=409892,
      #  tolerancja=tolerancja
    )

    plik_csv = "wyniki_2.csv"
    plik_istnieje = os.path.isfile(plik_csv)

    with open(plik_csv, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=wiersz.keys())
        if not plik_istnieje:
            writer.writeheader()  # nagłówek tylko raz
        writer.writerow(wiersz)




    pokaz_animacje(miasta,
                   najlepsze_osobniki,
                   najlepsze_wyniki,
                   srednie_wyniki,
                   najgorsze_wyniki,
                   obszar,
                   pauza=0.05,
                   filename="moja_animacja.gif")

    pokaz_najlepsza_trase(miasta,
                          najlepszy_osobnik,
                          obszar,
                          najlepsza_ocena,
                          najlepsza_gen
                          )

    plt.show(block=True)


if __name__ == "__main__":
    main()
