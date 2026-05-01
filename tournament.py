
from teams import Echipa
from tie import DublaMansa
from stats import (
    calculeaza_statistici,
    formateaza_probabilitati,
    statistici_penalty_prelungiri,
    afiseaza_separator,
    afiseaza_header,
    cel_mai_probabil_finalist,
)


class Turneu:
    def __init__(
        self,
        sf1: tuple[Echipa, Echipa],
        sf2: tuple[Echipa, Echipa],
        nr_simulari: int = 10_000,
    ):
        self.sf1 = sf1        
        self.sf2 = sf2        
        self.nr_simulari = nr_simulari

    def simuleaza(self) -> None:
        print(f"\n  SEMIFINALA 1: {self.sf1[0].nume} vs {self.sf1[1].nume}")
        afiseaza_separator()
        sf1_rezultate, sf1_penalty, sf1_prel = self._simuleaza_semifinala(*self.sf1)
        sf1_stats = calculeaza_statistici(sf1_rezultate)
        print(formateaza_probabilitati(self.sf1[0], self.sf1[1], sf1_stats))
        print()
        print(statistici_penalty_prelungiri(sf1_penalty, sf1_prel, self.nr_simulari))

        finalist1 = cel_mai_probabil_finalist(sf1_stats)

        print(f"\n  SEMIFINALA 2: {self.sf2[0].nume} vs {self.sf2[1].nume}")
        afiseaza_separator()
        sf2_rezultate, sf2_penalty, sf2_prel = self._simuleaza_semifinala(*self.sf2)
        sf2_stats = calculeaza_statistici(sf2_rezultate)
        print(formateaza_probabilitati(self.sf2[0], self.sf2[1], sf2_stats))
        print()
        print(statistici_penalty_prelungiri(sf2_penalty, sf2_prel, self.nr_simulari))

        finalist2 = cel_mai_probabil_finalist(sf2_stats)

        print(f"\n  FINALA (meci unic): {finalist1} vs {finalist2}")
        afiseaza_separator()
        echipa_f1 = self.sf1[0] if self.sf1[0].nume == finalist1 else self.sf1[1]
        echipa_f2 = self.sf2[0] if self.sf2[0].nume == finalist2 else self.sf2[1]

        finala_rezultate, fin_penalty, fin_prel = self._simuleaza_finala(
            echipa_f1, echipa_f2
        )
        finala_stats = calculeaza_statistici(finala_rezultate)
        print(formateaza_probabilitati(echipa_f1, echipa_f2, finala_stats))
        print()
        print(statistici_penalty_prelungiri(fin_penalty, fin_prel, self.nr_simulari))

        campion = cel_mai_probabil_finalist(finala_stats)

        print()
        afiseaza_separator("═")
        print(f"  🏆  CAMPION PROBABIL: {campion.upper()}")
        afiseaza_separator("═")
        print()

    def _simuleaza_semifinala(
        self,
        echipa1: Echipa,
        echipa2: Echipa,
    ) -> tuple[list[str], int, int]:
        castigatori = []
        nr_penalty = 0
        nr_prelungiri = 0

        for _ in range(self.nr_simulari):
            dm = DublaMansa(echipa1, echipa2)
            castigator = dm.simuleaza()
            castigatori.append(castigator.nume)

            if dm.penalty_castigator:
                nr_penalty += 1
            if dm.scor_prelungiri is not None:
                nr_prelungiri += 1

        return castigatori, nr_penalty, nr_prelungiri

    def _simuleaza_finala(
        self,
        echipa1: Echipa,
        echipa2: Echipa,
    ) -> tuple[list[str], int, int]:
        from match import Meci, simuleaza_goluri
        import random

        castigatori = []
        nr_penalty = 0
        nr_prelungiri = 0

        for _ in range(self.nr_simulari):
            meci = Meci(echipa1, echipa2)
            g1, g2 = meci.simuleaza()

            if g1 > g2:
                castigatori.append(echipa1.nume)
            elif g2 > g1:
                castigatori.append(echipa2.nume)
            else:
                nr_prelungiri += 1
                factor = 30 / 90
                p1 = simuleaza_goluri(echipa1.lambda_contra(echipa2) * factor)
                p2 = simuleaza_goluri(echipa2.lambda_contra(echipa1) * factor)

                if p1 > p2:
                    castigatori.append(echipa1.nume)
                elif p2 > p1:
                    castigatori.append(echipa2.nume)
                else:
                    nr_penalty += 1
                    castigatori.append(
                        echipa1.nume if random.random() < 0.5 else echipa2.nume
                    )

        return castigatori, nr_penalty, nr_prelungiri
