
from teams import Echipa
from tournament import Turneu
from data import SEMIFINALE


def main():
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║                 UCL 2025/26 — SIMULATOR  "             )
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

    sf1 = (Echipa(SEMIFINALE[0][0]), Echipa(SEMIFINALE[0][1]))
    sf2 = (Echipa(SEMIFINALE[1][0]), Echipa(SEMIFINALE[1][1]))

    print(f"  Semifinala 1: {sf1[0]}  vs  {sf1[1]}")
    print(f"  Semifinala 2: {sf2[0]}  vs  {sf2[1]}")
    print()

    NR_SIMULARI = 10000

    turneu = Turneu(sf1=sf1, sf2=sf2, nr_simulari=NR_SIMULARI)
    turneu.simuleaza()


if __name__ == "__main__":
    main()
