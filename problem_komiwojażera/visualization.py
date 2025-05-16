import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np


def pokaz_animacje(miasta, najlepsze_osobniki,
                   najlepsze_wyniki, srednie_wyniki, najgorsze_wyniki,
                   obszar, pauza=0.05, filename="animacja.gif"):

    n_miast = len(miasta)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    plt.tight_layout()
    canvas = FigureCanvas(fig)  # potrzebne do zapisu klatek

    miasta_x = [m[0] for m in miasta]
    miasta_y = [m[1] for m in miasta]
    ax1.scatter(miasta_x, miasta_y, color='red', zorder=3)

    klatki = []

    for gen, osobnik in enumerate(najlepsze_osobniki, start=1):

        for ln in list(ax1.lines):
            ln.remove()

        ax1.set_title(f'Pokolenie {gen}/{len(najlepsze_osobniki)}')
        ax1.set_xlim(obszar["x_min"], obszar["x_max"])
        ax1.set_ylim(obszar["y_min"], obszar["y_max"])

        for i in range(n_miast):
            a, b = osobnik[i], osobnik[(i + 1) % n_miast]
            ax1.plot([miasta[a][0], miasta[b][0]],
                     [miasta[a][1], miasta[b][1]],
                     'b-', linewidth=1.5, zorder=2)
            plt.pause(pauza)

        ax2.clear()
        pokolenia = range(1, gen + 1)
        ax2.plot(pokolenia, najlepsze_wyniki[:gen], 'g-', label='Najlepsza')
        ax2.plot(pokolenia, srednie_wyniki[:gen], 'b-', label='Średnia')
        ax2.plot(pokolenia, najgorsze_wyniki[:gen], 'r-', label='Najgorsza')
        ax2.set_xlabel('Pokolenie')
        ax2.set_ylabel('Długość trasy')
        ax2.grid(True)
        ax2.legend()
        fig.canvas.draw()

        # Zapisz aktualną klatkę
        klatki.append(np.array(canvas.buffer_rgba()))

    # Zapisz animację do pliku gif
    from PIL import Image
    Image.fromarray(klatki[0]).save(
        filename,
        save_all=True,
        append_images=[Image.fromarray(k) for k in klatki[1:]],
        duration=int(pauza * 6000),
        loop=0
    )
    print(f"Zapisano animację do pliku: {filename}")

    plt.ioff()
    plt.show()



def pokaz_najlepsza_trase(miasta, trasa, obszar,
                          dystans, pokolenie):

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 5))

    # punkty miast
    x = [m[0] for m in miasta]
    y = [m[1] for m in miasta]
    ax.scatter(x, y, color='red', zorder=3)

    # numery miast
    for idx, (xi, yi) in enumerate(zip(x, y)):
        ax.text(xi + 3, yi + 3, str(idx),
                fontsize=9, ha='left', va='bottom')

    # linia trasy
    route_x = [miasta[i][0] for i in trasa] + [miasta[trasa[0]][0]]
    route_y = [miasta[i][1] for i in trasa] + [miasta[trasa[0]][1]]
    ax.plot(route_x, route_y, 'b-', linewidth=1.8, zorder=2)

    # podpis długości i pokolenia
    ax.text(0.02, 0.98,
            f'Długość: {dystans:.2f}\nPokolenie: {pokolenie}',
            transform=ax.transAxes,
            ha='left', va='top', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='gray', alpha=0.8))

    # ustawienia osi
    ax.set_xlim(obszar["x_min"], obszar["x_max"])
    ax.set_ylim(obszar["y_min"], obszar["y_max"])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Najlepsza znaleziona trasa (z numeracją miast)')



    plt.tight_layout()
    plt.show()