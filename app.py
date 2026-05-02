
import math
import random
import streamlit as st
from teams import Echipa
from tie import DublaMansa
from match import Meci, simuleaza_goluri
from stats import calculeaza_statistici

st.set_page_config(
    page_title="UCL 2025/26 Simulator",
    page_icon="🏆",
    layout="centered",
)

NR_SIMULARI = 10_000


def probabilitate_poisson(lambda_: float, k: int) -> float:
    if lambda_ <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lambda_) * (lambda_ ** k)) / math.factorial(k)


def scor_cel_mai_probabil(e1: Echipa, e2: Echipa) -> str:
    """Scorul cel mai probabil pentru un singur meci."""
    lambda_h = e1.lambda_contra(e2)
    lambda_a = e2.lambda_contra(e1)
    max_g = 6
    best_p = 0
    best_scor = (0, 0)
    for i in range(max_g + 1):
        for j in range(max_g + 1):
            p = probabilitate_poisson(lambda_h, i) * probabilitate_poisson(lambda_a, j)
            if p > best_p:
                best_p = p
                best_scor = (i, j)
    return f"{best_scor[0]} — {best_scor[1]}"


def scor_agregat_cel_mai_probabil(e1: Echipa, e2: Echipa) -> str:
    lh_tur = e1.lambda_contra(e2)
    la_tur = e2.lambda_contra(e1)
    lh_ret = e2.lambda_contra(e1)
    la_ret = e1.lambda_contra(e2)

    max_g = 5
    scoruri = {}

    for g1_tur in range(max_g + 1):
        for g2_tur in range(max_g + 1):
            p_tur = probabilitate_poisson(lh_tur, g1_tur) * probabilitate_poisson(la_tur, g2_tur)
            for g2_ret in range(max_g + 1):
                for g1_ret in range(max_g + 1):
                    p_ret = probabilitate_poisson(lh_ret, g2_ret) * probabilitate_poisson(la_ret, g1_ret)
                    total1 = g1_tur + g1_ret
                    total2 = g2_tur + g2_ret
                    cheie = (total1, total2)
                    scoruri[cheie] = scoruri.get(cheie, 0) + p_tur * p_ret

    best = max(scoruri, key=scoruri.get)
    return f"{best[0]} — {best[1]}"


def simuleaza_semifinala(e1: Echipa, e2: Echipa):
    castigatori = []
    nr_penalty = 0
    nr_prelungiri = 0
    for _ in range(NR_SIMULARI):
        dm = DublaMansa(e1, e2)
        c = dm.simuleaza()
        castigatori.append(c.nume)
        if dm.penalty_castigator:
            nr_penalty += 1
        if dm.scor_prelungiri is not None:
            nr_prelungiri += 1
    return castigatori, nr_penalty, nr_prelungiri


def simuleaza_finala(e1: Echipa, e2: Echipa):
    castigatori = []
    nr_penalty = 0
    nr_prelungiri = 0
    for _ in range(NR_SIMULARI):
        meci = Meci(e1, e2)
        g1, g2 = meci.simuleaza()
        if g1 > g2:
            castigatori.append(e1.nume)
        elif g2 > g1:
            castigatori.append(e2.nume)
        else:
            nr_prelungiri += 1
            factor = 30 / 90
            p1 = simuleaza_goluri(e1.lambda_contra(e2) * factor)
            p2 = simuleaza_goluri(e2.lambda_contra(e1) * factor)
            if p1 > p2:
                castigatori.append(e1.nume)
            elif p2 > p1:
                castigatori.append(e2.nume)
            else:
                nr_penalty += 1
                castigatori.append(e1.nume if random.random() < 0.5 else e2.nume)
    return castigatori, nr_penalty, nr_prelungiri


def afiseaza_semifinala(titlu: str, e1: Echipa, e2: Echipa) -> Echipa:
    st.markdown(f"### {titlu}")
    st.markdown(f"**{e1.nume}** vs **{e2.nume}**")

    lambda_h = e1.lambda_contra(e2)
    lambda_a = e2.lambda_contra(e1)
    scor = scor_agregat_cel_mai_probabil(e1, e2)

    col1, col2, col3 = st.columns(3)
    col1.metric(f"λ {e1.nume}", f"{lambda_h:.2f}", "goluri asteptate")
    col2.metric(f"λ {e2.nume}", f"{lambda_a:.2f}", "goluri asteptate")
    col3.metric("Scor agregat probabil", scor)

    castigatori, nr_pen, nr_prel = simuleaza_semifinala(e1, e2)
    stats = calculeaza_statistici(castigatori)

    p1 = stats.get(e1.nume, 0)
    p2 = stats.get(e2.nume, 0)
    p_prel = round((nr_prel / NR_SIMULARI) * 100, 1)
    p_pen  = round((nr_pen  / NR_SIMULARI) * 100, 1)

    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{e1.nume} se califica", f"{p1:.1f}%")
        st.progress(p1 / 100)
    with col2:
        st.metric(f"{e2.nume} se califica", f"{p2:.1f}%")
        st.progress(p2 / 100)

    st.caption(
        f"Prelungiri in {p_prel}% din simulari · "
        f"Penalty-uri in {p_pen}% din simulari"
    )

    finalist = e1 if p1 >= p2 else e2
    st.success(f"Favorit la calificare: **{finalist.nume}**")
    st.divider()
    return finalist


st.title("UCL 2025/26 — Simulator")
st.caption(f"Semifinale & Finala · Distributie Poisson · {NR_SIMULARI:,} simulari")
st.divider()

arsenal  = Echipa("Arsenal")
atletico = Echipa("Atletico")
psg      = Echipa("PSG")
bayern   = Echipa("Bayern")

finalist1 = afiseaza_semifinala("Semifinala 1", atletico, arsenal)
finalist2 = afiseaza_semifinala("Semifinala 2", psg, bayern)

st.markdown("### Finala")
st.markdown(f"**{finalist1.nume}** vs **{finalist2.nume}** · Budapesta, 30 mai 2026")

lambda_fh = finalist1.lambda_contra(finalist2)
lambda_fa = finalist2.lambda_contra(finalist1)
scor_finala = scor_cel_mai_probabil(finalist1, finalist2)

col1, col2, col3 = st.columns(3)
col1.metric(f"λ {finalist1.nume}", f"{lambda_fh:.2f}", "goluri asteptate")
col2.metric(f"λ {finalist2.nume}", f"{lambda_fa:.2f}", "goluri asteptate")
col3.metric("Scor probabil", scor_finala)

fin_castigatori, fin_pen, fin_prel = simuleaza_finala(finalist1, finalist2)
fin_stats = calculeaza_statistici(fin_castigatori)

pf1 = fin_stats.get(finalist1.nume, 0)
pf2 = fin_stats.get(finalist2.nume, 0)
p_prel_f = round((fin_prel / NR_SIMULARI) * 100, 1)
p_pen_f  = round((fin_pen  / NR_SIMULARI) * 100, 1)

col1, col2 = st.columns(2)
with col1:
    st.metric(f"{finalist1.nume} castiga", f"{pf1:.1f}%")
    st.progress(pf1 / 100)
with col2:
    st.metric(f"{finalist2.nume} castiga", f"{pf2:.1f}%")
    st.progress(pf2 / 100)

st.caption(
    f"Prelungiri in {p_prel_f}% din simulari · "
    f"Penalty-uri in {p_pen_f}% din simulari"
)

campion = finalist1 if pf1 >= pf2 else finalist2
st.divider()
st.markdown(
    f"<h2 style='text-align:center; color:#c9a84c;'>Campion probabil: {campion.nume}</h2>",
    unsafe_allow_html=True
)
st.divider()
st.caption("Proiect Python · Distributie Poisson · UCL 2025/26")