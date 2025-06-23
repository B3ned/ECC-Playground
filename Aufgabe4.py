import ElliptischeKurve
E = ElliptischeKurve.EllipticCurve(
    16,
    20,
    31,
    42
)
G2 = (25,24)

Ich_pub = E.skalarmult(3,G2)
print(Ich_pub)


z = E.skalarmult(4,(8,3))
print(f"z:{z}")

print("///////////////////////////////////////////////")
for x in range(1,7):
    print(f"{x}{E.skalarmult(x,G2)}")