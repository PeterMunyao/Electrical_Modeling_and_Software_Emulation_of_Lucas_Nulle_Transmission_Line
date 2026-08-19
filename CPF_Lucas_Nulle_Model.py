import numpy as np
import time
import matplotlib.pyplot as plt

# ============================================================
# LOAD MODEL (NORMALISED CPF SCALING)
# ============================================================

def build_S_lambda(S_base, lam, beta=0.35):
    """
    Normalised continuation:
    S(λ) = S_base * λ / (1 + βλ)
    """
    scale = lam / (1.0 + beta * lam)
    return scale * S_base


# ============================================================
# IWAMOTO-STABILISED NEWTON
# ============================================================

def newton_iwamoto(Y, V0, unknown, S_spec,
                   tol=1e-8, max_iter=15):

    V = V0.copy()

    for it in range(max_iter):

        F = residual(Y, V, unknown, S_spec)
        err = np.max(np.abs(F))

        if err < tol:
            return V, True, it + 1, err

        J = jacobian_numeric(Y, V, unknown, S_spec)

        try:
            dx = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            dx = np.linalg.lstsq(J, -F, rcond=None)[0]

        # Iwamoto damping
        alpha = 1.0 / (1.0 + err)
        dx = alpha * dx

        x = voltage_to_state(V, unknown)
        x = x + dx
        V = state_to_voltage(x, V, unknown)

    return V, False, max_iter, err


# ============================================================
# CPF MAIN ENGINE
# ============================================================

def cpf(Y, V0, S_base, unknown,
        lam_max=2.0,
        step=0.133,
        beta=0.35):

    print("\nCPF START (CLEAN STABLE VERSION)")
    print("=" * 60)

    lam = 0.0
    V = V0.copy()

    stable_lambdas = []
    stable_voltages = []

    while lam <= lam_max + 1e-12:

        S_spec = build_S_lambda(S_base, lam, beta)

        V, conv, it, err = newton_iwamoto(
            Y, V, unknown, S_spec
        )

        vmax = np.max(np.abs(V))

        print(f"λ={lam:.3f} | max|V|={vmax:.3f} | conv={conv}")

        # store ONLY stable solutions
        if conv:
            stable_lambdas.append(lam)
            stable_voltages.append(V.copy())
        else:
            print("CPF STOPPED (loss of convergence)")
            break

        lam += step

    return stable_lambdas, stable_voltages


# ============================================================
# RUN CPF
# ============================================================

S_base = S_spec.copy()

lam_hist, V_hist = cpf(
    Y,
    V0,
    S_base,
    unknown=unknown,
    lam_max=2.0,
    step=0.133,
    beta=0.35
)


# ============================================================
# LAST STABLE SOLUTION
# ============================================================

print("\nLAST STABLE CPF STATE")
print("=" * 60)

V_last = V_hist[-1]
lam_last = lam_hist[-1]

print(f"λ_last = {lam_last:.3f}")

for i, v in enumerate(V_last):
    print(f"{i:2d} {abs(v):10.4f} V {np.degrees(np.angle(v)):10.4f} deg")


# ============================================================
# PLOTTING (ONLY STABLE REGION)
# ============================================================

bus = 10  # choose bus to visualize

Vmag = [np.abs(v[bus]) for v in V_hist]

plt.figure()
plt.plot(lam_hist, Vmag, marker='o')
plt.xlabel("Load factor λ")
plt.ylabel(f"|V_bus {bus}|")
plt.title("CPF Voltage Profile (Stable Region Only)")
plt.grid(True)
plt.show()
