# def find_N(B,maxp):
#     ret = []
#     for p in prime_range(20,maxp):
#         for q in prime_range(20,maxp):
#             lp = (p+1).prime_divisors()[-1]
#             lq = (q+1).prime_divisors()[-1]
#             if (lp != lq) and (max(lp,lq)<B):
#                 ret.append(p*q)
#     return ret

# ll = find_N(10,100)


# NN = ll[ZZ.random_element(len(ll))]

# print(NN)
# set_random_seed(42)

# NN = 91
# p = 7

# a = ZZ.random_element(1,NN-1)
# b = ZZ.random_element(1,NN-1)

# while True:
#     d = ZZ.random_element(1,NN-1)
#     if not d.is_square():
#         break

# print(a,b,d)

# R = QuadraticField(d, 'sqrtd') # make the field Q(sqrtd)
# G = R.automorphisms() # find the automorphisms of this field (one will be the identity and other other will swap sqrtd with -sqrtd)
# t = a+b*R.0 
# tbar = G[1](t) #find \bar{t}, G[1] is the automorphism that swaps sqrtd with -sqrtd
# x = tbar/t # you can check at this point that x*G[1](x)=1

# ZZN = IntegerModRing(NN)  # make the integers mod N
# z = polygen(ZZN, 'z') # make the polynomial ring ZZ/(N)[z]

# # I do several things in the next line.  Take ZZN and extend it by adding a root of z^2-d.  Next I coerce the x I found above to be in that extension ring.  Then I raise it to the E=p+1 power
# xN =(ZZN.extension(z^2-d,'a')(x))^(p+1) # this only works this reliably because I know p+1
# print(t)
# print(x)
# print(ZZN.extension(z^2-d,'a')(x))
# u = xN.list()[0] #this is the rational part of this power
# v = xN.list()[1] # this is the sqrtd part of this power
# print(gcd([u-1,v,NN]))

# print((ZZN.extension(z^2-d,'a')(x))^(p+1))
'''
3086 1441 11
t = 1441*sqrtd + 3086
x = 8893852/13317895*sqrtd - 32364687/13317895
ZZN.extension(z^2-d, 'a')(x) = 2933*a + 1390
xN = 564*a + 3009
47
'''

# Williams p+1 method using your Sage syntax
def williams_method(NN, B):

        # Step 1: pick random a, b
        a = randint(1, NN-1)
        b = randint(1, NN-1)
        
        # Step 2: pick random d not a square mod NN
        while True:
            d = randint(2, NN-1)
            if not is_square(Mod(d, NN)):
                break
        
        # Step 3: define quadratic field Q(sqrt(d))
        R = QuadraticField(d, 'sqrtd')
        G = R.automorphisms()
        t = a + b*R.0
        tbar = G[1](t)   # automorphism that swaps sqrt(d) -> -sqrt(d)
        
        # Step 4: x = tbar / t
        x = tbar / t
        # check: x * G[1](x) should be 1
        assert x * G[1](x) == 1
        print("d = ", d)

        # Step 5: define integers mod N
        ZZN = IntegerModRing(NN)
        z = polygen(ZZN, 'z')
        xN = (ZZN.extension(z^2 - d, 'a')(x))
        print(f"xN = {xN}")

        # iterate over primes <= B
        primes_list = [p for p in prime_range(2, B+1)]
        for p in primes_list:
            # find e such that p^(e-1) < NN <= p^e
            e = 1
            while p**e < NN:
                e += 1
            E = p**e

            # extend ZZN by adding root of z^2 - d and coerce x
            xN = (ZZN.extension(z^2 - d, 'a')(x))**E

            # print t, x, and xN for debugging
            print(f"t = {t}")
            print(f"x = {x}")
            print(f"xN = {xN}")
            print(f"l^e={p}^{e}")

            # extract coefficients
            u = xN.list()[0]  # rational part
            v = xN.list()[1]  # sqrt(d) part
            print(f"b mod N = {u} + {v}*sqrt({d})")

            # check gcd for factor
            g = gcd([u-1, v, NN])
            if g != 1 and g != NN:
                print(f"Nontrivial factor found: {g}")
                return g

        # if no factor found
        return "failure"

# Example usage
NN = 91  # number to factor
B = 3     # smoothness bound
williams_method(NN, B)
