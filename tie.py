
import random
from teams import Echipa
from match import Meci, simuleaza_goluri


class DublaMansa:
    
    def __init__(self, echipa1: Echipa, echipa2: Echipa):
        self.echipa1 = echipa1
        self.echipa2 = echipa2

        self.scor_tur: tuple[int, int] | None = None       # (gol_e1, gol_e2)
        self.scor_retur: tuple[int, int] | None = None     # (gol_e2, gol_e1)
        self.scor_prelungiri: tuple[int, int] | None = None
        self.penalty_castigator: Echipa | None = None
        self.calificata: Echipa | None = None

    def simuleaza(self) -> Echipa:
        tur = Meci(acasa=self.echipa1, deplasare=self.echipa2)
        g1_tur, g2_tur = tur.simuleaza()
        self.scor_tur = (g1_tur, g2_tur)

        retur = Meci(acasa=self.echipa2, deplasare=self.echipa1)
        g2_ret, g1_ret = retur.simuleaza()
        self.scor_retur = (g2_ret, g1_ret)

        total1 = g1_tur + g1_ret
        total2 = g2_tur + g2_ret

        if total1 > total2:
            self.calificata = self.echipa1
        elif total2 > total1:
            self.calificata = self.echipa2
        else:
            self.calificata = self._prelungiri()

        return self.calificata

    def _prelungiri(self) -> Echipa:
        factor = 30 / 90 

        lambda1 = self.echipa1.lambda_contra(self.echipa2) * factor
        lambda2 = self.echipa2.lambda_contra(self.echipa1) * factor

        g1 = simuleaza_goluri(lambda1)
        g2 = simuleaza_goluri(lambda2)
        self.scor_prelungiri = (g1, g2)

        if g1 > g2:
            return self.echipa1
        elif g2 > g1:
            return self.echipa2
        else:
            # Tot egal -> penalty-uri
            return self._penalty()

    def _penalty(self) -> Echipa:
        if random.random() < 0.5:
            self.penalty_castigator = self.echipa1
        else:
            self.penalty_castigator = self.echipa2
        return self.penalty_castigator

    def rezumat(self) -> str:
        if self.scor_tur is None:
            return "Dubla mansa nesimulata."

        g1_tur, g2_tur = self.scor_tur
        g2_ret, g1_ret = self.scor_retur

        total1 = g1_tur + g1_ret
        total2 = g2_tur + g2_ret

        linii = [
            f"  Tur:    {self.echipa1.nume} {g1_tur} - {g2_tur} {self.echipa2.nume}",
            f"  Retur:  {self.echipa2.nume} {g2_ret} - {g1_ret} {self.echipa1.nume}",
            f"  Agregat: {self.echipa1.nume} {total1} - {total2} {self.echipa2.nume}",
        ]

        if self.scor_prelungiri:
            g1p, g2p = self.scor_prelungiri
            linii.append(f"  Prelungiri: {g1p} - {g2p}")

        if self.penalty_castigator:
            linii.append(f"  Departajare la penalty-uri!")

        linii.append(f"  ✅ Calificata: {self.calificata.nume}")
        return "\n".join(linii)
