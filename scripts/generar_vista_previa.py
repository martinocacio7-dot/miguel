"""Genera analisis/vista_previa_resultados.png: los resultados que debe mostrar el dashboard (sin filtros)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

from datos import COLUMNAS, FILAS
from textos import TITULO

SALIDA = Path(__file__).resolve().parent.parent / "analisis"
SALIDA.mkdir(exist_ok=True)

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_2 = "#52514e"
TINTA_3 = "#8a8985"
REJILLA = "#e6e5e1"
COLOR_TIPO = {"Estándar": "#2a78d6", "Express": "#eb6834"}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "text.color": TINTA,
    "axes.labelcolor": TINTA_2,
    "xtick.color": TINTA_2,
    "ytick.color": TINTA_2,
    "axes.edgecolor": REJILLA,
    "axes.facecolor": SUPERFICIE,
    "figure.facecolor": SUPERFICIE,
})

df = pd.DataFrame(FILAS, columns=COLUMNAS)


def miles(v, _=None):
    return f"{v / 1000:.0f}K" if v >= 1000 else f"{v:.0f}"


def ejes_limpios(ax, grid_eje="y"):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    ax.spines["left"].set_color(REJILLA)
    ax.spines["bottom"].set_color(REJILLA)
    ax.grid(axis=grid_eje, color=REJILLA, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


fig = plt.figure(figsize=(16, 8.4), dpi=110)
gs = fig.add_gridspec(3, 4, height_ratios=[0.55, 2.6, 0.05], hspace=0.45, wspace=0.45,
                      left=0.05, right=0.97, top=0.85, bottom=0.11)

fig.text(0.05, 0.952, TITULO, fontsize=17, fontweight="bold")
fig.text(0.05, 0.915, "Vista previa de los resultados esperados con los 60 registros y sin filtros "
         "(generada con Python para verificar; no es una captura de Power BI)", fontsize=10, color=TINTA_2)

# Tarjetas KPI
kpis = [
    ("Ventas totales (USD)", f"${df.Ventas_USD.sum():,.0f}"),
    ("Promedio general de días de entrega", f"{df.Dias_Entrega.mean():.2f}"),
    ("Costo de envío promedio (USD)", f"${df.Costo_Envio_USD.mean():,.2f}"),
    ("Pedidos analizados", f"{len(df)}"),
]
for i, (etiqueta, valor) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i])
    ax.axis("off")
    ax.text(0, 0.95, etiqueta, fontsize=10, color=TINTA_2, va="top")
    ax.text(0, 0.05, valor, fontsize=24, fontweight="bold", va="bottom")

# Dispersión: X = costo, Y = días, tamaño = ventas, color = tipo de envío
ax = fig.add_subplot(gs[1, 0:2])
for tipo, g in df.groupby("Tipo_Envio"):
    ax.scatter(g.Costo_Envio_USD, g.Dias_Entrega, s=(g.Ventas_USD / 1000) ** 1.6 * 2.2,
               color=COLOR_TIPO[tipo], alpha=0.75, edgecolors=SUPERFICIE, linewidths=1.5, label=tipo, zorder=3)
pendiente, corte = np.polyfit(df.Costo_Envio_USD, df.Dias_Entrega, 1)
xs = np.array([1000, 4700])
ax.plot(xs, pendiente * xs + corte, color=TINTA_2, linewidth=2, zorder=2)
ax.text(3050, pendiente * 3050 + corte + 0.35, f"Tendencia: {pendiente * 1000:.2f} días\npor cada USD 1,000",
        ha="left", fontsize=9, color=TINTA_2)
for pid, dx, dy, ha in [(1022, 0, 0.32, "center"), (1023, 0, 0.32, "center")]:
    p = df[df.ID_Pedido == pid].iloc[0]
    ax.annotate(f"Pedido {pid} (Oeste)\nUSD {p.Costo_Envio_USD:,} · {p.Dias_Entrega} días",
                (p.Costo_Envio_USD, p.Dias_Entrega), xytext=(p.Costo_Envio_USD + dx, p.Dias_Entrega + dy + 0.25),
                ha=ha, fontsize=9, color=TINTA, arrowprops=dict(arrowstyle="-", color=TINTA_3, lw=1))
ax.set_xlim(900, 4900)
ax.set_ylim(0.5, 8.9)
ax.xaxis.set_major_formatter(lambda v, _: f"${v:,.0f}")
ax.set_xlabel("Costo_Envio_USD")
ax.set_ylabel("Dias_Entrega")
ax.set_title("Costo de envío vs. días de entrega por pedido (tamaño = ventas)", loc="left",
             fontsize=12, fontweight="bold", pad=24)
leyenda = [Line2D([0], [0], marker="o", linestyle="", markersize=9, markerfacecolor=c, markeredgecolor=SUPERFICIE,
                  label=t) for t, c in COLOR_TIPO.items()]
leyenda.append(Line2D([0], [0], color=TINTA_2, linewidth=2, label="Línea de tendencia"))
ax.legend(handles=leyenda, loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3, frameon=False, fontsize=9,
          borderaxespad=0.2, handletextpad=0.4)
ejes_limpios(ax, "both")

# Comparación regional (dos paneles con su propia escala en lugar de un eje dual)
reg = df.groupby("Región")[["Costo_Envio_USD", "Dias_Entrega"]].mean().sort_values("Costo_Envio_USD")
for col, (campo, titulo, fmt) in zip([2, 3], [
    ("Costo_Envio_USD", "Costo de envío promedio (USD)", lambda v: f"${v:,.0f}"),
    ("Dias_Entrega", "Días de entrega promedio", lambda v: f"{v:.2f}"),
]):
    ax = fig.add_subplot(gs[1, col])
    y = np.arange(len(reg))
    colores = ["#2a78d6" if r == "Oeste" else "#9ec5f4" for r in reg.index]
    ax.barh(y, reg[campo], height=0.3, color=colores, zorder=3)
    for yi, v in zip(y, reg[campo]):
        ax.text(v, yi, "  " + fmt(v), va="center", fontsize=10, color=TINTA)
    ax.set_yticks(y, reg.index)
    ax.set_xlim(0, reg[campo].max() * 1.32)
    ax.xaxis.set_major_formatter(miles if campo == "Costo_Envio_USD" else (lambda v, _: f"{v:.0f}"))
    ax.set_title(titulo, loc="left", fontsize=12, fontweight="bold", pad=24)
    ax.text(0, 1.02, "por región (promedio)", transform=ax.transAxes, fontsize=9, color=TINTA_2)
    ejes_limpios(ax, "x")

fig.text(0.05, 0.045, "En Power BI estos dos paneles van en un solo gráfico mixto (columnas = costo promedio, "
         "línea = días promedio, eje Y secundario), como pide la guía. Oeste resaltado: mayor costo y mayor demora.",
         fontsize=9, color=TINTA_2)

fig.savefig(SALIDA / "vista_previa_resultados.png", facecolor=SUPERFICIE)
print("OK:", SALIDA / "vista_previa_resultados.png")
