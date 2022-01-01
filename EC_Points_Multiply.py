import EC_Points_Generator as ECPtsGen

# Extended Euclidean algorithm
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# calculate `modular inverse`
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g == 1:
        return x % m
    else:
        return None

    # double function


def ecc_double(x1, y1, p, a):
    if modinv(2 * y1, p) is None: return None

    s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    x3 = (s ** 2 - x1 - x1) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


# add function
def ecc_add(x1, y1, x2, y2, p, a):
    s = 0
    if (x1 == x2):
        if modinv(2 * y1, p) is None : return None
        s = ((3 * (x1 ** 2) + a) * modinv(2 * y1, p)) % p
    else:
        if modinv(x2 - x1, p) is None: return None
        s = ((y2 - y1) * modinv(x2 - x1, p)) % p
    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p
    return (x3, y3)


def double_and_add(multi, generator, p, a):
    (x3, y3) = (0, 0)
    (x1, y1) = generator
    (x_tmp, y_tmp) = generator
    init = 0
    for i in str(bin(multi)[2:]):
        if (i == '1') and (init == 0):
            init = 1
        elif (i == '1') and (init == 1):
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            if ecc_add(x1, y1, x3, y3, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x3, y3) = ecc_add(x1, y1, x3, y3, p, a)
            (x_tmp, y_tmp) = (x3, y3)
        else:
            if ecc_double(x_tmp, y_tmp, p, a) is None: return None
            (x3, y3) = ecc_double(x_tmp, y_tmp, p, a)
            (x_tmp, y_tmp) = (x3, y3)
    return (x3, y3)


def scale_point_set(a, b, p, generator):
    ec_curve_points = ECPtsGen.ec_gen_points_set(a, b, p)
    scaled_points_set = {}
    i = 1
    scaled_points_set[str(i) + "P"] = generator

    while True:
        i += 1
        scaled_point = double_and_add(i, generator, p, a)

        if scaled_point is None or scaled_point not in ec_curve_points:
            scaled_points_set[str(i) + "P"] = "O"
            break

        elif scaled_point in ec_curve_points:
            scaled_points_set[str(i) + "P"] = scaled_point
            if str(i) + "P" != "2P" and scaled_points_set["2P"] == scaled_points_set[str(i) + "P"]:  # the current index is not 2P and no other duplicate point exists
                scaled_points_set[str(i) + "P"] = "O"
                break    #if duplicate P exists then stop

    return scaled_points_set

# Testing Purposes
# a = 2
# b = 3
# p = 97
# generator = (0,10)

# a = 2
# b = 9
# p = 23
# generator = (0, 3)
# sc = scale_point_set(a, b, p, generator)
# print((sc),"\n")
#
# for key in sc:
#     print(key, sc[key])



