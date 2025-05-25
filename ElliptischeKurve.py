INF = (0,1,0)
class EllipticCurve:
    def __init__(self, ec_a, ec_b, ec_p):
        self.ec_a = ec_a
        self.ec_b = ec_b
        self.ec_p = ec_p

        '''
        ECC like y**2 = x**3 + ax + b
        :param x: x value of ECC in int or hex in str
        :param ec_a: steigung der ECC in int or hex in str
        :param ec_b: Const of ECC in int or hex in str
        :param ec_p: GF of ECC in int or hex in str
        '''

    def proj_add(self, P: (int,int,int), Q: (int,int,int)):
        '''
        :input: Proj Point on ECC
        :return: Aff Point on ECC
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
        return self.projtoaffin((X3, Y3, Z3))


    def proj_dbl(self, P: (int,int,int)):
        '''
        :param P: Proj Point on ECC
        :return: Aff Point on ECC
        '''
        X, Y, Z = P
        W = (3 * X**2 + self.ec_a * Z**2) % self.ec_p
        S = (Y * Z) % self.ec_p
        B = (X * Y * S) % self.ec_p
        H = (W**2 - 8 * B) % self.ec_p
        X2 = (2 * H * S) % self.ec_p
        Y2 = (W * (4 * B - H) - 8 * Y**2 * S**2) % self.ec_p
        Z2 = (8 * S**3) % self.ec_p
        return self.projtoaffin((X2, Y2, Z2))

    # Transformationen
    def projtoaffin(self, P: (int, int, int)):
        X, Y, Z = P
        return modDivision(X, Z, self.ec_p), modDivision(Y, Z, self.ec_p), 1

    def affintoproj(self, P: (int, int), Z = 1):
        X, Y= P
        return modDivision(X,Z,self.ec_p), modDivision(Y,Z,self.ec_p), Z

    def affintoprojScaled(self, P: (int, int), Z):
        return self.affintoproj(P, Z)

    # Methoden für affinen Raum
    def aff_getY(self, ec_x: str):
        # TODO Vielleicht falsch impl nochmal drüber gucken
        """
        :param ec_x: X in komprimierter Form mit prefix 0x in str
        :return: y Value if exists
        """
        prefix, x = hexTransformer(ec_x)
        y2 = pow(x, 3, self.ec_p) + self.ec_a * x + self.ec_b
        if not isResidue(y2, self.ec_p):
            print("Punkt liegt nicht auf der Kurve")
            return None
        if y2 % 4 == 3:
            y = pow(y2, modDivision(self.ec_p + 1, 4, self.ec_p), self.ec_p)
            if prefix % 2 == 0 and y % 2 == 0:
                print(y)
                return y
            else:
                return (self.ec_p - y) % self.ec_p
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
    return (z ** modDivision(p-1, 2, p)) % p == 1
print(pow(1, modDivision(17+1, 4, 17), 17))


def transformer(s):
    if type(s) == int:
        return s
    if s.startswith('0x'):
        return int(s, 16)

    raise Exception("Falscher Eingabewert")

def hexTransformer(s: str):
    if type(s) == int:
        return s
    if not s.startswith('0x'):
        print("Falscher Eingabewert")
        return None
    s = s.replace('0x', '')
    prefix = s[2:4]
    s = s[:2] + s[4:]
    return int(prefix), int(s,16)



