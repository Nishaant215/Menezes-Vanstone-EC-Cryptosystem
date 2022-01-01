import EC_Points_Multiply as ECPtsMult


def KeyGen(key, pointSet):
    order = len(pointSet)
    if key > order:
        key = key % order

        if key == 0: return pointSet[str(order) + "P"]  # if the modulo is zero return the last element in list

        key = pointSet[str(key) + "P"]  # User Public Key
    else:
        key = pointSet[str(key) + "P"]  # User Public Key

    return key

# Extended Euclidean algorithms that takes two coprime nums and finds and find inverse mod
def Inverse_Mod(e, m):
    m0 = m
    y = 0
    x = 1

    if (m == 1):
        return 0

    while (e > 1):
        q = int(e / m)  # q is quotient

        temp = m

        m = e % m
        e = temp
        temp = y

        # Update x and y
        y = x - q * y
        x = temp

    # Make x positive
    if (x < 0): x = x + m0

    return x


print("Menzezaes-Vanstones EC Cryptosystem")

print("Elliptic Curve: y^2 = x^3 + a*x + b (mod p)")
a = int(input("Enter the coefficient a: ").strip())
b = int(input("Enter the coefficient b: ").strip())
p = int(input("Enter the p mod value: ").strip())

print("Elliptic Curve: y^2 = x^3 + " + str(a) + "*x + " + str(b) + " (mod" + str(p) + ")")

gx = int(input("Enter generator x value: ").strip())
gy = int(input("Enter generator y value: ").strip())
generator = (gx, gy)

Nb = int(input("User B enter private keyB Nb<p: ").strip())  # User B Private Key

publicKeyB = KeyGen(Nb, ECPtsMult.scale_point_set(a, b, p, generator))
print("User B public KeyB Yb:", publicKeyB)

Ka = int(input("User A enter secret keyA k<p: ").strip())  # User B Private Key
hint_clue = KeyGen(Ka, ECPtsMult.scale_point_set(a, b, p, generator))
print("Hint/Clue y0:",hint_clue)

mask = KeyGen(Ka, ECPtsMult.scale_point_set(a, b, p, publicKeyB))
print("Mask:", mask)
print("C1:", mask[0]," C2:", mask[1])

m = input("Enter plaintext m1<p and m2<p: ")
m1 = int(m[:len(m)//2])
print("m1:",m1)
m2 = int(m[len(m)//2:])
print("m2:",m2)

y1 = (mask[0]*m1)%p
y2 = (mask[1]*m2)%p

print("y1:",y1)
print("y2:",y2)

print("A sends cipher text",hint_clue,";",y1,";",y2)

print("\nDecryption by B")

Nb_hint= KeyGen(Nb, ECPtsMult.scale_point_set(a, b, p, hint_clue))
print("Nb*hint:", Nb_hint)

inv_c1 = Inverse_Mod(Nb_hint[0],p)
print("inverse_C1",inv_c1)

decrypt_m1 = (inv_c1*y1)%p
print("Message M1 Decrypted:", decrypt_m1)

inv_c2 = Inverse_Mod(Nb_hint[1],p)
print("inverse_C2",inv_c2)

decrypt_m2 = (inv_c2*y2)%p
print("Message M2 Decrypted:", decrypt_m2)

full_m = str(decrypt_m1) + str(decrypt_m2)
print("Full Message:", full_m)



