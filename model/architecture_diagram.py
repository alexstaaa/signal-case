# -*- coding: utf-8 -*-
"""Схема архитектуры ИИ-агента «Сигнал» -> PNG."""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

out = sys.argv[1]
plt.rcParams["font.family"] = "Segoe UI"

NAVY = "#12304F"
BLUE = "#0B5CAD"
ORANGE = "#E8611A"
BAND1 = "#EAF3FB"
BAND2 = "#FDF1E7"
GREY = "#EEF1F4"
LINE = "#5B6B7B"

fig, ax = plt.subplots(figsize=(16, 7.6), dpi=200)
ax.set_xlim(0, 16)
ax.set_ylim(0, 7.6)
ax.axis("off")


def band(x, y, w, h, color, label, lc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.18",
                                fc=color, ec="none", zorder=0))
    ax.text(x + 0.22, y + h - 0.28, label, fontsize=13, color=lc, weight="bold", va="center", zorder=1)


def box(x, y, w, h, title, sub="", num=None, fc="white", ec=BLUE, tc=NAVY, lw=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    cy = y + h / 2
    if sub:
        ax.text(x + w / 2, cy + 0.17, title, fontsize=12.5, color=tc, weight="bold", ha="center", va="center", zorder=4)
        ax.text(x + w / 2, cy - 0.22, sub, fontsize=10, color="#44546A", ha="center", va="center", zorder=4,
                linespacing=1.15)
    else:
        ax.text(x + w / 2, cy, title, fontsize=12.5, color=tc, weight="bold", ha="center", va="center", zorder=4)
    if num is not None:
        ax.add_patch(plt.Circle((x + 0.02, y + h - 0.02), 0.2, fc=ORANGE, ec="white", lw=1.2, zorder=5))
        ax.text(x + 0.02, y + h - 0.03, str(num), fontsize=10.5, color="white", weight="bold",
                ha="center", va="center", zorder=6)


def arrow(p1, p2, color=LINE, ls="-", lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=16, lw=lw, color=color,
                                 linestyle=ls, zorder=2, shrinkA=0, shrinkB=0))


def line(pts, color=LINE, ls="-", lw=1.8):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, linestyle=ls, zorder=2, solid_capstyle="round")


def label(x, y, text, color="#44546A", size=9.5, ha="center"):
    ax.text(x, y, text, fontsize=size, color=color, ha=ha, va="center", zorder=4,
            bbox=dict(fc="white", ec="none", pad=1.2, alpha=0.0))


# --- полосы
band(2.75, 3.75, 13.05, 3.7, BAND1, "Ночной конвейер — ежедневно, 22:00–06:00, без участия LLM-агента", BLUE)
band(2.75, 0.15, 13.05, 3.35, BAND2, "Агент — еженедельно, работает с темами, а не с обращениями", ORANGE)

# --- верхний ряд
W, H = 2.05, 1.0
yc = 5.25  # центр конвейера
box(0.15, yc - 0.75, 2.2, 1.5, "Тикет-система", "заявки · записи\nзвонков · вложения", fc=GREY, ec="#9AA7B4")
box(3.15, yc - H / 2, W, H, "Сборщик", "дельта за сутки", 1)
box(5.75, yc + 0.35, W + 0.15, 0.95, "Речь → текст", "Qwen-ASR", 2)
box(5.75, yc - 1.30, W + 0.15, 0.95, "Вложения → текст", "Qwen-VL", 3)
box(8.5, yc - H / 2, W, H, "Маскирование", "ПДн, единая схема", 4)
box(11.05, yc - H / 2, W, H, "Анализатор", "Qwen 3.8: карточка,\nпривязка к теме", 5)
box(13.55, yc - 0.65, 2.0, 1.3, "Реестр тем", "PostgreSQL: частоты,\nтренды, статусы", 6, fc="#FFFFFF", ec=NAVY, lw=2.2)

arrow((2.35, yc), (3.15, yc))
# сборщик -> ASR / VL / напрямую
line([(5.2, yc), (5.45, yc)])
line([(5.45, yc), (5.45, yc + 0.82)])
arrow((5.45, yc + 0.82), (5.75, yc + 0.82))
line([(5.45, yc), (5.45, yc - 0.82)])
arrow((5.45, yc - 0.82), (5.75, yc - 0.82))
arrow((5.45, yc), (8.5, yc))
label(6.85, yc + 0.0 + 0.13, "текст заявок", size=9.5)
# ASR/VL -> маскирование
line([(7.95, yc + 0.82), (8.2, yc + 0.82), (8.2, yc + 0.25)])
arrow((8.2, yc + 0.25), (8.5, yc + 0.25))
line([(7.95, yc - 0.82), (8.2, yc - 0.82), (8.2, yc - 0.25)])
arrow((8.2, yc - 0.25), (8.5, yc - 0.25))
arrow((10.55, yc), (11.05, yc))
arrow((13.1, yc), (13.55, yc))

# --- нижний ряд
yb = 1.55
box(10.75, yb - 0.6, 2.65, 1.2, "Агент-аналитик", "Qwen 3.8 + 12 инструментов", 7, ec=ORANGE, lw=2.2)
box(7.6, yb - 0.5, W, H, "Доставка", "черновики, дайджест,\nсбор реакций", 8, ec=ORANGE)
box(3.15, yb - 0.5, 3.3, H, "Трекер задач и мессенджер", "черновик задачи · сводка в канал", fc=GREY, ec="#9AA7B4")
box(0.15, yb - 0.75, 2.2, 1.5, "Продуктовые\nкоманды", "", fc=GREY, ec="#9AA7B4")
box(13.75, 0.4, 1.85, 0.95, "Справочник\nпродуктов", "", fc=GREY, ec="#9AA7B4")

# реестр -> агент (темы-кандидаты) и обратно (статусы)
line([(14.75, yc - 0.65), (14.75, 1.95), (13.6, 1.95)], color=NAVY)
arrow((13.6, 1.95), (13.4, 1.95), color=NAVY)
label(15.27, 2.9, "темы-\nкандидаты", size=9.5)
arrow((13.4, 1.15), (13.75, 0.95), color=LINE)
# агент -> доставка -> трекер -> команды
arrow((10.75, yb), (9.65, yb), color=ORANGE)
label(10.2, yb + 0.2, "сигналы", size=9.5)
arrow((7.6, yb), (6.45, yb), color=ORANGE)
arrow((3.15, yb), (2.35, yb), color=ORANGE)
# поиск в бэклоге
line([(11.6, yb - 0.6), (11.6, 0.55), (4.8, 0.55)], ls=(0, (4, 3)))
arrow((4.8, 0.55), (4.8, yb - 0.5), ls=(0, (4, 3)))
label(8.2, 0.37, "поиск существующих задач (только чтение)", size=9.5)
# обратная связь
line([(8.6, yb + 0.5), (8.6, 2.6), (13.95, 2.6)], color=BLUE, ls=(0, (4, 3)))
arrow((13.95, 2.6), (13.95, yc - 0.65), color=BLUE, ls=(0, (4, 3)))
label(11.25, 2.78, "реакции команд: взяли / уже известно / не актуально", color=BLUE, size=9.5)

fig.savefig(out, bbox_inches="tight", pad_inches=0.08, facecolor="white")
print("saved", out)
