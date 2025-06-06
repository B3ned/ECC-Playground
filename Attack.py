import ElliptischeKurve
from MitM import MitM

E = ElliptischeKurve.EllipticCurve(
    0x7D5A0975FC2C3057EEF67530417AFFE7FB8055C126DC5C6CE94A4B44F330B5D9,
    0x26DC5C6CE94A4B44F330B5D9BBD77CBF958416295CF7E1CE6BCCDC18FF8C07B6,
    0xA9FB57DBA1EEA9BC3E660A909D838D726E3BF623D52620282013481D1F6E5377,
    0xA9FB57DBA1EEA9BC3E660A909D838D718C397AA3B561A6F7901E0E82974856A7
)

G = (
    0x8BD2AEB9CB7E57CB2C4B482FFC81B7AFB9DE27E1E3BD23C23A4453BD9ACE3262,
    0x547EF835C3DAC4FD97F8461A14611DC9C27745132DED8E545C1D54C72F046997
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
