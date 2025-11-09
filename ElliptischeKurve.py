import random
import numpy as np




INF = (0,1,0)
class EllipticCurve:
    def __init__(self, ec_a, ec_b, ec_p, ec_n):
        self.ec_a = ec_a
        self.ec_b = ec_b
        self.ec_p = ec_p
        self.ec_n = ec_n
        self.privKey = self.privkeygen()
        '''
        ECC like y**2 = x**3 + ax + b
        :param x: x value of ECC in int or hex
        :param ec_a: steigung der ECC in int or hex 
        :param ec_b: Const of ECC in int or hex
        :param ec_p: GF of ECC in int or hex
        '''

    def proj_add(self, P: (int,int,int), Q: (int,int,int)):
        '''
        :input: Proj Point on ECC
        :return: Proj Point on ECC
        '''
        if P == INF:
            return Q
        if Q == INF:
            return P

        X1, Y1, Z1 = P
        X2, Y2, Z2 = Q
        U1 = (Y2 * Z1) % self.ec_p
        U2 = (Y1 * Z2) % self.ec_p
        V1 = (X2 * Z1) % self.ec_p
        V2 = (X1 * Z2) % self.ec_p
        U = (U1 - U2) % self.ec_p
        V = (V1 - V2) % self.ec_p

        if V == 0:
            # check if Q is invers to P
            if U != 0:
                return INF
            # check if P is Q
            return self.proj_dbl(P)

        W = (Z1 * Z2) % self.ec_p
        A = (U**2 * W - V**3 - 2 * V**2 * V2) % self.ec_p
        X3 = (V * A) % self.ec_p
        Y3 = (U * (V**2 * V2 - A) - V**3 * U2) % self.ec_p
        Z3 = (V**3 * W) % self.ec_p
        return X3, Y3, Z3


    def proj_dbl(self, P: (int,int,int)):
        '''
        :param P: Proj Point on ECC
        :return: Proj Point on ECC
        '''
        X, Y, Z = P
        W = (3 * X**2 + self.ec_a * Z**2) % self.ec_p
        S = (Y * Z) % self.ec_p
        B = (X * Y * S) % self.ec_p
        H = (W**2 - 8 * B) % self.ec_p
        X2 = (2 * H * S) % self.ec_p
        Y2 = (W * (4 * B - H) - 8 * Y**2 * S**2) % self.ec_p
        Z2 = (8 * S**3) % self.ec_p
        return X2, Y2, Z2

    def skalarmult(self, k, P):
        """
        Double-and-add (MSB first, links-nach-rechts) in projektiven Koordinaten.
        Gibt den Punkt in affinen Koordinaten zurück.
        """
        if k <= 0:
            raise ValueError("k muss positiv sein")
        xX, yY = P
        if xX == 0 or yY == 0:
            raise ValueError("Punkt darf keine 0 Elemente haben")

        #  Nimm hier die Ordnung der Kurve (ec_n)
        k %= self.ec_n
        bin_k = bin(k)[3:]
        R = self.affintoproj(P)  # laufende Basis
        Q = R  # Akkumulator (startet mit neutralem Element)

        for x in bin_k:
            Q = self.proj_dbl(Q)
            if x == "1":
                Q = self.proj_add(Q, R)
        return self.projtoaffin(Q)

    def privkeygen(self):
        return random.randint(1, self.ec_n - 1)

    # Transformationen
    def projtoaffin(self, P: (int, int, int)):
        X, Y, Z = P
        return modDivision(X, Z, self.ec_p), modDivision(Y, Z, self.ec_p)


    def affintoproj(self, P, Z = None):
        if Z is None:
            Z = 1
        X, Y= P
        return modDivision(X,Z,self.ec_p), modDivision(Y,Z,self.ec_p), Z
 
    # Methoden für affinen Raum
    def aff_getY(self, ec_x: str):
        # TODO Vielleicht falsch impl nochmal drüber gucken
        """
        :param ec_x: X in komprimierter Form mit paritybit 0x in str
        :return: y Value if exists
        """
        paritybit, x = hexTransformer(ec_x)
        isEven = paritybit % 2 == 0
        y2 = (pow(x, 3, self.ec_p) + self.ec_a * x + self.ec_b) % self.ec_p
        if not isResidue(y2, self.ec_p):
            print("Punkt liegt nicht auf der Kurve")
            return None
        if y2 % 4 == 3:
            y = pow(y2, modDivision(self.ec_p + 1, 4, self.ec_p), self.ec_p)
            if isEven:
                if y % 2 == 0:
                    return y
                else:
                    return (self.ec_p - y) % self.ec_p
            else:
                if y % 2 == 0:
                    return (self.ec_p - y) % self.ec_p
                else:
                    return y
        else:
            raise NotImplementedError("Tonelli-Shanks nicht implementiert bro")

    def aff_add(self, P, Q):
        if P == "neutral" or Q == "neutral":
            return "neutral"
        x1, y1 = P
        x2, y2 = Q
        if x1 == x2 and (y1 + y2) % self.ec_p == 0:
            return "neutral"
        if x1 == x2 and y1 == y2:
            s = modDivision(3 * pow(x1, 2) + self.ec_a, 2 * y1, self.ec_p)
            x3 = (pow(s, 2) - 2 * x1) % self.ec_p
            y3 = (s * (x1 - x3) - y1) % self.ec_p
        else:
            s = modDivision(y2 - y1, x2 - x1, self.ec_p)
            x3 = (pow(s, 2) - x1 - x2) % self.ec_p
            y3 = (s * (x1 - x3) - y1) % self.ec_p
        return x3, y3

    def aff_sub(self, P, Q):
        x1, y1 = P
        x2, y2 = Q
        return self.aff_add((x1,y1),(x2,-y2))


#Hilfsmethoden

def modinv(ec_a, p):
        return pow(ec_a, -1, p)

def modDivision(x, y, p):
    return ((x % p) * pow(y, -1, p)) % p

def isResidue(z, p):
    # Euler Kriterium
    return pow(z,modDivision(p-1, 2, p),p) == 1

def hexTransformer(s: str):
    if type(s) == int:
        return s
    if not s.startswith('0x'):
        print("Falscher Eingabewert")
        return None
    paritybit = s[2:4]
    s = s[:2] + s[4:]
    return int(paritybit,16), int(s,16)

def stringtointList(l:list[str]) -> list[int]:
    return [int(x) for x in l]








