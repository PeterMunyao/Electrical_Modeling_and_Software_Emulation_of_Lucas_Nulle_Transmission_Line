import numpy as np

# ==========================================================
# SYSTEM PARAMETERS
# ==========================================================

f = 50.0
w = 2*np.pi*f

# ---------------- Phase conductor -------------------------

R = 7.2
L = 230e-3

Zp = R + 1j*w*L
Yp = 1/Zp

# ---------------- Neutral conductor -----------------------

Rn = 15.0
Ln = 200e-3

Zn = Rn + 1j*w*Ln
Yn = 1/Zn

# ---------------- Grounding impedance ---------------------

# Neutral connected to Earth through grounding reactor
Yg = Yn

# ---------------- Capacitances ----------------------------

Ce = 1.1e-6       # phase-earth
Cm = 300e-9       # phase-phase

Ye = 1j*w*Ce
Ym = 1j*w*Cm

# ==========================================================
# NODE NUMBERING
# ==========================================================

"""
Bus1
0  L1
1  L2
2  L3
3  N
4  PE

Bus2
5  L1
6  L2
7  L3
8  N
9  PE

Bus3
10 L1
11 L2
12 L3
13 N
14 PE
"""

Y = np.zeros((15,15),dtype=complex)

# ==========================================================
# STAMP FUNCTIONS
# ==========================================================

def stamp_series(Y, n1, n2, y):
    """Series branch"""
    Y[n1,n1] += y
    Y[n2,n2] += y
    Y[n1,n2] -= y
    Y[n2,n1] -= y


def stamp_shunt(Y, n1, n2, y):
    """Generic shunt branch"""
    Y[n1,n1] += y
    Y[n2,n2] += y
    Y[n1,n2] -= y
    Y[n2,n1] -= y


def stamp_mutual(Y, n1, n2, y):
    """Phase-phase capacitance"""
    Y[n1,n1] += y
    Y[n2,n2] += y
    Y[n1,n2] -= y
    Y[n2,n1] -= y


# ==========================================================
# TRANSMISSION LINE
# ==========================================================

def stamp_line(Y, busA, busB):

    # ------------------------
    # Phase conductors
    # ------------------------

    for k in range(3):
        stamp_series(Y,
                     busA+k,
                     busB+k,
                     Yp)

    # ------------------------
    # Neutral conductor
    # ------------------------

    stamp_series(Y,
                 busA+3,
                 busB+3,
                 Yn)

    # ------------------------
    # π-model shunt
    # ------------------------

    for bus in [busA, busB]:

        PE = bus + 4
        N  = bus + 3

        # Phase-earth capacitance
        for phase in range(3):
            stamp_shunt(
                Y,
                bus+phase,
                PE,
                Ye/2
            )

        # Neutral grounding reactor
        stamp_shunt(
            Y,
            N,
            PE,
            Yg
        )

        # Phase-phase capacitance
        stamp_mutual(
            Y,
            bus+0,
            bus+1,
            Ym/2
        )

        stamp_mutual(
            Y,
            bus+0,
            bus+2,
            Ym/2
        )

        stamp_mutual(
            Y,
            bus+1,
            bus+2,
            Ym/2
        )


# ==========================================================
# BUILD NETWORK
# ==========================================================

# Bus indices
BUS1 = 0
BUS2 = 5
BUS3 = 10

stamp_line(Y, BUS1, BUS2)
stamp_line(Y, BUS2, BUS3)
stamp_line(Y, BUS3, BUS1)

# ==========================================================
# PRINT
# ==========================================================

np.set_printoptions(
    precision=6,
    suppress=True,
    linewidth=220
)

print("="*80)
print("15 x 15 Y-BUS MATRIX")
print("="*80)
print(Y)

print("\nNode numbering")
print("----------------------------")
print("0  : Bus1 L1")
print("1  : Bus1 L2")
print("2  : Bus1 L3")
print("3  : Bus1 Neutral")
print("4  : Bus1 Earth")
print("5  : Bus2 L1")
print("6  : Bus2 L2")
print("7  : Bus2 L3")
print("8  : Bus2 Neutral")
print("9  : Bus2 Earth")
print("10 : Bus3 L1")
print("11 : Bus3 L2")
print("12 : Bus3 L3")
print("13 : Bus3 Neutral")
print("14 : Bus3 Earth")
