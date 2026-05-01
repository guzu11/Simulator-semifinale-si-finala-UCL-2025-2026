
from collections import defaultdict
from teams import Echipa


def calculeaza_statistici(rezultate: list[str]) -> dict[str, float]:
    contor = defaultdict(int)
    total = len(rezultate)

    for castigator in rezultate:
        contor[castigator] += 1

    return {
        echipa: round((count / total) * 100, 2)
        for echipa, count in contor.items()
    }


def cel_mai_probabil_finalist(statistici: dict[str, float]) -> str:
    return max(statistici, key=lambda e: statistici[e])


def formateaza_probabilitati(
    echipa1: Echipa,
    echipa2: Echipa,
    statistici: dict[str, float]
) -> str:
    p1 = statistici.get(echipa1.nume, 0)
    p2 = statistici.get(echipa2.nume, 0)

    bara_lungime = 30
    bara1 = "█" * int(bara_lungime * p1 / 100)
    bara2 = "█" * int(bara_lungime * p2 / 100)

    return (
        f"\n  {echipa1.nume:<15} {bara1:<30} {p1:.1f}%"
        f"\n  {echipa2.nume:<15} {bara2:<30} {p2:.1f}%"
    )


def statistici_penalty_prelungiri(
    nr_penalty: int,
    nr_prelungiri: int,
    total: int
) -> str:
    p_prel = round((nr_prelungiri / total) * 100, 1)
    p_pen = round((nr_penalty / total) * 100, 1)
    return (
        f"  S-a ajuns la prelungiri in {p_prel}% din cazuri\n"
        f"  S-a ajuns la penalty-uri in {p_pen}% din cazuri"
    )


def afiseaza_separator(caracter: str = "─", lungime: int = 55) -> None:
    print(caracter * lungime)


def afiseaza_header(titlu: str) -> None:
    afiseaza_separator("═")
    print(f"  {titlu.upper()}")
    afiseaza_separator("═")
