# Finding the points (x,y) that satisfies y^2 = x^3 + a*x + b in Z(n)

def legendre(a, p):
    return pow(a, (p - 1) // 2, p)


def tonelli_algo(n, p):
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r


def ec_gen_points_set(a, b, p):
    ec_points_on_curve = []
    for x in range(p):
        y2 = x ** 3 + a * x + b
        lengdre_val = legendre(y2, p)

        if lengdre_val != 0:
            if lengdre_val != 1:  # (y2 | p) must be ≡ 1 to have a square if not continue to next num
                continue
        elif lengdre_val == 0:
            y_root1 = 0
            gen1 = (x, y_root1)
            ec_points_on_curve.append(gen1)
            continue

        y_root1 = tonelli_algo(y2, p)  # one possible root
        y_root2 = p - y_root1

        if y_root2 < y_root1:
            gen1 = (x, y_root2)
            gen2 = (x, y_root1)
        else:
            gen1 = (x, y_root1)
            gen2 = (x, y_root2)

        ec_points_on_curve.append(gen1)
        ec_points_on_curve.append(gen2)
    return ec_points_on_curve


# a = 2
# b = 3
# p = 97
# print("Elliptic Curve: y^2 = x^3 + " + str(a) + "*x + " + str(b) + " (mod" + str(p) + ")")
# ec_points = ec_gen_points_set(a, b, p)
# count = 1
# for x in ec_points:
#     print( x)
#     count += 1
