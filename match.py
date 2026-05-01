
import math
import random
from teams import Echipa


def probabilitate_poisson(lambda_: float, k: int) -> float:
    if lambda_ <= 0:
        return 1.0 if k == 0 else 0.0
    return (math.exp(-lambda_) * (lambda_ ** k)) / math.factorial(k)


def simuleaza_goluri(lambda_: float, max_goluri: int = 10) -> int:
    rand = random.random()
    cumul = 0.0
    for k in range(max_goluri + 1):
        cumul += probabilitate_poisson(lambda_, k)
        if rand <= cumul:
            return k
    return max_goluri


class Meci:
    def __init__(self, acasa: Echipa, deplasare: Echipa):
        self.acasa = acasa
        self.deplasare = deplasare
        self.goluri_acasa: int | None = None
        self.goluri_deplasare: int | None = None

    def simuleaza(self) -> tuple[int, int]:
        lambda_acasa = self.acasa.lambda_contra(self.deplasare)
        lambda_deplasare = self.deplasare.lambda_contra(self.acasa)

        self.goluri_acasa = simuleaza_goluri(lambda_acasa)
        self.goluri_deplasare = simuleaza_goluri(lambda_deplasare)

        return self.goluri_acasa, self.goluri_deplasare

    def rezultat_text(self) -> str:
        if self.goluri_acasa is None:
            return "Meci nesimulat"
        return (
            f"{self.acasa.nume} {self.goluri_acasa}"
            f" - "
            f"{self.goluri_deplasare} {self.deplasare.nume}"
        )

    def __str__(self) -> str:
        return (
            f"{self.acasa.nume} vs {self.deplasare.nume}"
            if self.goluri_acasa is None
            else self.rezultat_text()
        )
