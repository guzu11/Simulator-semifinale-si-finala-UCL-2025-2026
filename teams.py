
from data import ECHIPE, MEDIA_LIGA


class Echipa:
    def __init__(self, nume: str):
        if nume not in ECHIPE:
            raise ValueError(f"Echipa '{nume}' nu exista in baza de date.")

        self.nume = nume
        date = ECHIPE[nume]
        self.nume_complet = date["nume"]
        self.liga = date["liga"]
        self.gf = date["gf"]   
        self.ga = date["ga"]   
        self.emoji = date["emoji"]

    def forta_atac(self) -> float:
        return self.gf / MEDIA_LIGA

    def forta_aparare(self) -> float:
        return self.ga / MEDIA_LIGA

    def lambda_contra(self, adversar: "Echipa") -> float:
        return self.forta_atac() * adversar.forta_aparare() * MEDIA_LIGA

    def __str__(self) -> str:
        return f"{self.emoji}  {self.nume_complet} ({self.liga})"

    def __repr__(self) -> str:
        return f"Echipa('{self.nume}')"
