# -*- coding: utf-8 -*-
"""Финансовая модель ИИ-агента «Сигнал»: сколько можно вложить, чтобы проект окупился за 3 года.

Расходную часть по условию кейса не считаем, поэтому считаем приведённую стоимость (PV)
эффекта за 3 года — это и есть потолок вложений с окупаемостью за 3 года.

Запуск: python finance_model.py
"""

TICKETS_PER_YEAR = 250_000      # ≈1 000 обращений в день (40 менеджеров × 25 в смену), допущение
HOURS_PER_TICKET = 0.25         # 15 минут на обращение, допущение
MANAGERS = 40
WEEKS = 47                      # рабочих недель в году
HOUR_COST_Y1 = 1_200            # ₽: 110 тыс. ₽ × 1,302 × 1,15 / 1 650 ч
INDEXATION = 0.07               # рост стоимости часа в год
RATE = 0.18                     # ключевая ставка 14 % + 4 п. п. за риск

SCENARIOS = {
    "Пессимистичный": {"drop": [0.04, 0.06, 0.08], "manual_hours": 0.5},
    "Базовый":        {"drop": [0.08, 0.12, 0.15], "manual_hours": 1.0},
    "Оптимистичный":  {"drop": [0.12, 0.18, 0.22], "manual_hours": 2.0},
}


def hour_cost(year: int) -> float:
    return HOUR_COST_Y1 * (1 + INDEXATION) ** year


def yearly_effect(drop: list, manual_hours: float) -> list:
    """Эффект по годам, млн ₽: снижение потока + высвобождение ручной аналитики."""
    out = []
    for y in range(3):
        c = hour_cost(y)
        fewer_tickets = TICKETS_PER_YEAR * drop[y] * HOURS_PER_TICKET * c
        manual = MANAGERS * manual_hours * WEEKS * c
        out.append((fewer_tickets + manual) / 1e6)
    return out


def pv(flows: list, rate: float = RATE) -> float:
    return sum(v / (1 + rate) ** (i + 1) for i, v in enumerate(flows))


def fmt(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


if __name__ == "__main__":
    print(f"{'Сценарий':<16}{'Год 1':>8}{'Год 2':>8}{'Год 3':>8}{'PV, млн ₽':>12}")
    for name, s in SCENARIOS.items():
        e = yearly_effect(s["drop"], s["manual_hours"])
        print(f"{name:<16}{fmt(e[0]):>8}{fmt(e[1]):>8}{fmt(e[2]):>8}{fmt(pv(e)):>12}")

    base = yearly_effect(**{"drop": SCENARIOS["Базовый"]["drop"], "manual_hours": 1.0})
    lo, hi = pv(base, RATE + 0.03), pv(base, RATE - 0.03)
    print(f"\nЧувствительность базового сценария к ставке ±3 п. п.: ±{fmt((hi - lo) / 2)} млн ₽")
    one_pp = TICKETS_PER_YEAR * 0.01 * HOURS_PER_TICKET * HOUR_COST_Y1 / 1e6
    print(f"Один процентный пункт снижения потока: {one_pp:.2f} млн ₽ в год".replace(".", ","))
