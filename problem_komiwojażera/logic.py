from enum import Enum
import random
from math import sqrt

class opcja_selekcji(Enum):
    ranking = "ranking"
    ruletka = "ruletka"



def generuj_miasta(ilosc_miast, dane_obszaru):
    miasta = []

    #wygenerownie punktów (miast) w wyznaczonym obszarze

    for _ in range(ilosc_miast):
        x = dane_obszaru["x_min"] + (dane_obszaru["x_max"] - dane_obszaru["x_min"]) * random.random()
        y = dane_obszaru["y_min"] + (dane_obszaru["y_max"] - dane_obszaru["y_min"]) * random.random()


        miasta.append((x, y))

    return miasta


#dla generacja 1. populacji
def generuj_populacje(l_miast, l_osobnikow):
    populacja = []
    for _ in range(l_osobnikow):
        permutacja = random.sample(range(l_miast), l_miast)
        populacja.append(permutacja)
    return populacja



def funkcja_jakosci(trasa, miasta):
    dystans = 0
    for i in range(len(trasa)):
        miasto_a = miasta[trasa[i]] #
        miasto_b = miasta[trasa[(i + 1) % len(trasa)]] # zawrotka do pierwszego miasta
        dystans += sqrt((miasto_a[0] - miasto_b[0])**2 + (miasto_a[1] - miasto_b[1])**2) #odległość Euklidesowa

   # print(f"Długość trasy: {dystans:.2f}")
    return dystans


def ocena_populacji(populacja, miasta):
    oceny = []
    for i, osobnik in enumerate(populacja):
        dlugosc = funkcja_jakosci(osobnik, miasta)

        oceny.append(dlugosc)
    return oceny



def selekcja(populacja, oceny, metoda, liczba_wybranych):
    if metoda == opcja_selekcji.ranking:
        # Ranking:
        posortowane = [x for _, x in sorted(zip(oceny, populacja))]
        return posortowane[:liczba_wybranych]

    elif metoda == opcja_selekcji.ruletka:
        # Ruletka:
        suma = sum(1 / o for o in oceny)
        prawdopodobienstwa = [(1 / o) / suma for o in oceny]
        return random.choices(populacja, weights=prawdopodobienstwa, k=liczba_wybranych)

    else:
        raise ValueError("Nieznana metoda selekcji")


def krzyzowanie_ox(rodzic1, rodzic2):

    rozmiar = len(rodzic1)
    locus_start, locus_koniec = sorted(random.sample(range(rozmiar), 2))

    srodek = rodzic1[locus_start:locus_koniec]
    pozostale = [miasto for miasto in rodzic2 if miasto not in srodek]
    potomek = pozostale[:locus_start] + srodek + pozostale[locus_start:]
    return potomek

def mutacja_swap(trasa, prawdopodobienstwo):
    if random.random() < prawdopodobienstwo:
        a, b = random.sample(range(len(trasa)), 2)
        trasa[a], trasa[b] = trasa[b], trasa[a]
    return trasa

def generuj_nowa_populacje(elita, populacja, liczba_osobnikow, p_mutacji, p_krzyzowania):
    nowa_populacja = elita.copy()

    while len(nowa_populacja) < liczba_osobnikow:
        # rodzic1, rodzic2 = random.sample(elita, 2)
        rodzic1, rodzic2 = random.choices(populacja, k=2)

        if random.random() < p_krzyzowania:
            potomek = krzyzowanie_ox(rodzic1, rodzic2)
        else:
            potomek = rodzic1.copy()

        potomek = mutacja_swap(potomek, p_mutacji)
        nowa_populacja.append(potomek)

    return nowa_populacja


def uruchom_algorytm(l_miast, osobniki, limit_pokolen, p_mutacji, p_krzyzowania, elitarna, r_selekcja, obszar,
    tolerancja = 1e-3
    ):

    miasta = generuj_miasta(l_miast, obszar)
    populacja = generuj_populacje(l_miast, osobniki)

    najlepsze_wyniki = []
    srednie_wyniki = []
    najgorsze_wyniki = []
    najlepsze_osobniki = []

    najlepszy_osobnik = None
    najlepsza_ocena = float('inf')
    brak_poprawy = 0

    for generacja in range(limit_pokolen): # iteracja po generacji w ilości pokoleń
        oceny = ocena_populacji(populacja, miasta)

        min_ocena = min(oceny)
        srednia_ocena = sum(oceny) / len(oceny)
        max_ocena = max(oceny)

        najlepsze_wyniki.append(min_ocena)
        srednie_wyniki.append(srednia_ocena)
        najgorsze_wyniki.append(max_ocena)

        if tolerancja is None:
            poprawa = najlepsza_ocena > min_ocena
        else:
            poprawa = najlepsza_ocena - min_ocena > tolerancja

        if poprawa:
            najlepsza_ocena = min_ocena
            najlepszy_osobnik = populacja[oceny.index(min_ocena)]
            brak_poprawy = 0
        else:
            brak_poprawy += 1


            #najlepszy osobnik
        najlepsze_osobniki.append(najlepszy_osobnik.copy())

        ranking_populacji = [x for _, x in sorted(zip(oceny, populacja))]
        elitarna = max(1, elitarna)
        elita = ranking_populacji[:elitarna] #znalezienie elity

        ## ROZAWAŻANIA DOSTYCZĄCE  SZANS NA BYCIE RODZICEM
       # liczba_do_selekcji = max(elitarna * 2, osobniki // 3)
        liczba_do_selekcji =  int(osobniki)
        wybrani = selekcja(populacja, oceny, r_selekcja, liczba_do_selekcji)


        populacja = generuj_nowa_populacje(elita, wybrani, osobniki, p_mutacji, p_krzyzowania)

    else:
        generacja += 1


    return najlepszy_osobnik, najlepsza_ocena, miasta, najlepsze_osobniki, najlepsze_wyniki, srednie_wyniki, najgorsze_wyniki, generacja


