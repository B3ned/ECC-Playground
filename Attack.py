import ElliptischeKurve
from MitM import MitM

E = ElliptischeKurve.EllipticCurve(
    0x7d5a0975fc2c3057eef67530417affe7fb8055c126dc5c6ce94a4b44f330b5d9,
    0x26dc5c6ce94a4b44f330b5d9bbd77cbf958416295cf7e1ce6bccdc18ff8c07b6,
    0xa9fb57dba1eea9bc3e660a909d838d726e3bf623d52620282013481d1f6e5377,
    0xa9fb57dba1eea9bc3e660a909d838d718c397aa3b561a6f7901e0e82974856a7
)

G = (
    0x8bd2aeb9cb7e57cb2c4b482ffc81b7afb9de27e1e3bd23c23a4453bd9ace3262,
    0x547ef835c3dac4fd97f8461a14611dc9c27745132ded8e545c1d54c72f046997
)

alice_priv = E.privkeygen()
alice_pub = E.skalarmult(alice_priv, G)

bob_priv = E.privkeygen()
bob_pub = E.skalarmult(bob_priv, G)

mitm = MitM()

fake_pub_to_bob = mitm.intercept_from_alice(alice_pub)
fake_pub_to_alice = mitm.intercept_from_bob(bob_pub)

shared_alice = E.skalarmult(alice_priv, fake_pub_to_alice)
shared_bob = E.skalarmult(bob_priv, fake_pub_to_bob)

secrets = mitm.get_secrets()

print("Alice shared:", shared_alice)
print("Bob shared:", shared_bob)
print("MitM shared with Alice:", secrets["MitM <-> Alice"])
print("MitM shared with Bob:", secrets["MitM <-> Bob"])
