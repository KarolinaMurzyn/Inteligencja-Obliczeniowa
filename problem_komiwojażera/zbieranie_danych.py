from itertools import product
from main import run_once

# Parametry do testów
levels_n      = [ 40, 80,100]
levels_mut    = [0.00, 0.05, 0.10, 0.20, 0.4]
levels_elite  = [0.00, 0.03, 0.05, 0.1, 1.3]
tolerancje    = [None, 1e-3]      # <- test bez i z tolerancją
repeats       = 6                # liczba ziaren RNG
limit_pokolen = [ 100,200]               # maksymalna liczba pokoleń

# Licznik do śledzenia postępu
licznik = 0
total = len(levels_n) * len(levels_mut) * len(levels_elite) * len(tolerancje) * repeats * len(limit_pokolen)

# Główna pętla testowa
for tol in tolerancje:
    for limit in limit_pokolen:
        for n, pm, e in product(levels_n, levels_mut, levels_elite):
            for r in range(repeats):
                run_once(
                    n_miast=n,
                    p_mut=pm,
                    elite_pct=e,
                    seed=r,
                    limit_pokolen=limit,
                    tolerancja=tol
                )
                licznik += 1
                print(f"→ zapisano {licznik}/{total} wierszy", end="\r")

print("\nGotowe! Wszystkie kombinacje przetestowane.")