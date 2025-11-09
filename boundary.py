import argparse
import ElliptischeKurve
    

def stringtointList(l: list[str]) -> list[int]:
    return [int(x) for x in l]


def main():
    ap = argparse.ArgumentParser(
        description="Elliptische Kurve, die CLI Argumente parst.",
        epilog="Copyright (c) 2025 Bene. All Rights Reserved."
    )
    # Per default prime256v1 values
    ap.add_argument(
        "--a",
        type=float,
        default=0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc,
        dest="a")
    ap.add_argument(
        "--b",
        type=float,
        default=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
        dest="b"
    )

    ap.add_argument(
        "--p",
        type=float,
        default=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
        dest="p"
    )
    ap.add_argument(
        "--n",
        type=float,
        default=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
        dest="n"
    )
    G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

    args = ap.parse_args()

    # TODO Validieren der Params
    e = ElliptischeKurve.EllipticCurve(args.a, args.b, args.p, args.n)
    mainloop(e)


def mainloop(ec: ElliptischeKurve.EllipticCurve):
    while True:

        inp = input(
            f"Was möchtest du machen? Möglichkeiten:\n1.xDBL\n2.xADD\n3.getY\n4.exit\n").split()
        if not validateInput(inp):
            return

        if inp[0] == "xADD": xADD_loop(ec)
        if inp[0] == "xDBL":xDBL_loop(ec)
        if inp[0] == "getY": getY_loop(ec)


def validateInput(input: list):
    if input[0] == "exit":
        return False
    if len(input) > 1:
        raise ValueError("Genau 1 Möglichkeit auswählen")
    if not (input[0] == "xDBL" or input[0] == "xADD" or input[0] == "getY"):
        raise ValueError(
            "Bitte eine der eben genannten Möglichkeiten auswählen")
    return True


def xADD_loop(ec: ElliptischeKurve.EllipticCurve):
    inp = input(f"Gib die beiden Punkte in der Form an: x_1,y_1 x2,y2\n").split()
    if not len(inp) == 2:
        raise ValueError("Punkte nicht in der Form x_1,y_1 x_2,y_2 angegeben")
    g_1 = tuple(stringtointList(inp[0].split(',')))
    g_2 = tuple(stringtointList(inp[1].split(',')))
    pg_1 = ec.affintoproj(g_1)
    pg_2 = ec.affintoproj(g_2)
    print(ec.projtoaffin(ec.proj_add(pg_1, pg_2)))
 
def xDBL_loop(ec: ElliptischeKurve.EllipticCurve):
    inp = input(f"Gib den Punkt in der Form an: x_1,y_1\n").split()
    if not len(inp) == 1:
        raise ValueError("Punkt nicht in der Form x_1,y_1 angegeben")
    g = tuple(stringtointList(inp[0].split(',')))
    print(ec.projtoaffin(ec.proj_dbl(ec.affintoproj(g))))

def getY_loop(ec: ElliptischeKurve.EllipticCurve):
    inp = input(f"Gib eine x Koordinate in Hexadezimal mit Paritätsbit ein, zu der du eine y Koordinate möchtest. Example:030D\n").split()
    if not len(inp) == 1:
        raise ValueError("Whitespace gefunden!")
    print(ec.aff_getY("0x" + inp[0]))


if __name__ == "__main__":
    main()
