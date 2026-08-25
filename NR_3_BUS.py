import numpy as np
import time

# ============================================================
# CONSTANT-POWER (PQ) LOADS
# ============================================================

S_spec = np.zeros(15, dtype=complex)

# Bus 3 measured loads (negative = load)

S_spec[10] = -(77 + 0j)      # Bus3 L1
S_spec[11] = -(80 + 0j)      # Bus3 L2
S_spec[12] = -(74 + 0j)      # Bus3 L3


# ============================================================
# UNKNOWN NODES
# ============================================================

unknown = [5,6,7,8,9,
           10,11,12,13,14]


# ============================================================
# INITIAL VOLTAGES
# ============================================================

V0 = initialize_voltages()


# ============================================================
# STATE VECTOR CONVERSION
# ============================================================

def voltage_to_state(V, unknown):

    x = []

    for node in unknown:

        x.append(V[node].real)
        x.append(V[node].imag)

    return np.array(x)


def state_to_voltage(x, Vbase, unknown):

    V = Vbase.copy()

    k = 0

    for node in unknown:

        V[node] = x[k] + 1j*x[k+1]

        k += 2

    return V


# ============================================================
# CONSTANT POWER CURRENT
# ============================================================

def load_current(V, S_spec):

    I = np.zeros(len(V), dtype=complex)

    for i in range(len(V)):

        if abs(S_spec[i]) > 0:

            if abs(V[i]) < 1e-9:

                continue

            I[i] = np.conj(S_spec[i]/V[i])

    return I


# ============================================================
# CURRENT MISMATCH
# ============================================================

def residual(Y, V, unknown, S_spec):

    Inet = Y @ V

    Iload = load_current(V, S_spec)

    R = Inet - Iload

    F = []

    for node in unknown:

        F.append(R[node].real)
        F.append(R[node].imag)

    return np.array(F)


# ============================================================
# NUMERICAL JACOBIAN
# ============================================================

def jacobian_numeric(Y,
                     V,
                     unknown,
                     S_spec,
                     h=1e-6):

    x = voltage_to_state(V, unknown)

    n = len(x)

    J = np.zeros((n,n))

    F0 = residual(Y,
                  V,
                  unknown,
                  S_spec)

    for i in range(n):

        x2 = x.copy()

        x2[i] += h

        V2 = state_to_voltage(x2,
                              V,
                              unknown)

        F2 = residual(Y,
                      V2,
                      unknown,
                      S_spec)

        J[:,i] = (F2 - F0)/h

    return J


# ============================================================
# NEWTON-RAPHSON
# ============================================================

def newton_raphson(Y,
                   V0,
                   unknown,
                   S_spec,
                   tol=1e-8,
                   max_iter=30):

    V = V0.copy()

    history = []

    start = time.perf_counter()

    converged = False

    for it in range(max_iter):

        F = residual(Y,
                     V,
                     unknown,
                     S_spec)

        error = np.max(np.abs(F))

        history.append(error)

        if error < tol:

            converged = True

            break

        J = jacobian_numeric(Y,
                             V,
                             unknown,
                             S_spec)

        dx = np.linalg.solve(J,
                             -F)

        x = voltage_to_state(V,
                             unknown)

        x += dx

        V = state_to_voltage(x,
                             V,
                             unknown)

    elapsed = time.perf_counter() - start

    return {

        "V":V,

        "iterations":it+1,

        "history":history,

        "time":elapsed,

        "converged":converged,

        "error":error

    }


# ============================================================
# RUN NEWTON-RAPHSON
# ============================================================

nr = newton_raphson(
        Y,
        V0,
        unknown,
        S_spec
)

Vnr = nr["V"]


print("\n==============================")
print("NEWTON-RAPHSON RESULTS")
print("==============================")
print("Converged :", nr["converged"])
print("Iterations:", nr["iterations"])
print("Final Error:", nr["error"])
print("Time (s):", nr["time"])


print("\nNode        Voltage(V)      Angle(deg)")

for i in range(len(Vnr)):

    print(f"{i:2d}    "
          f"{abs(Vnr[i]):10.4f}    "
          f"{np.degrees(np.angle(Vnr[i])):10.3f}")


print("\nCurrent Injection")

I = Y @ Vnr

for i in range(len(I)):

    print(f"{i:2d}    "
          f"{abs(I[i]):10.4f} A    "
          f"{np.degrees(np.angle(I[i])):10.3f}")


print("\nComplex Power")

S = Vnr*np.conj(I)

for i in range(len(S)):

    print(f"{i:2d}    "
          f"P={S[i].real:10.3f} W    "
          f"Q={S[i].imag:10.3f} VAR")
