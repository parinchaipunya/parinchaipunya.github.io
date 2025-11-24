from pyscipopt import Model, quicksum
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. DATA
# ============================================================

techs = ["Gas", "Coal", "Peaker"]

cost = {"Gas": 20.0, "Coal": 40.0, "Peaker": 120.0}
pmax = {"Gas": 60.0, "Coal": 40.0, "Peaker": 100.0}

# Stochastic scenarios (same as before)
demands = [80.0, 100.0, 120.0, 140.0, 160.0]
probs   = [0.10, 0.20, 0.40, 0.20, 0.10]

Scen = list(range(len(demands)))
w = {s: demands[s] for s in Scen}
pi = {s: probs[s]   for s in Scen}

# Penalty cost
C_plus = 500.0
C_minus = 5.0


# ============================================================
# 2. HELPER: Build and solve model given demand scenarios + probabilities
# ============================================================

def solve_stochastic(w, pi):
    scen_list = list(w.keys())   # <---- use local scenario set
    m = Model("sto")

    # first-stage variables
    u = {i: m.addVar(lb=0, ub=pmax[i], vtype="C", name=f"u_{i}")
         for i in techs}

    # recourse variables for these scenarios only
    y_plus  = {s: m.addVar(lb=0, vtype="C", name=f"yplus_{s}") for s in scen_list}
    y_minus = {s: m.addVar(lb=0, vtype="C", name=f"yminus_{s}") for s in scen_list}

    # objective
    m.setObjective(
        quicksum(cost[i] * u[i] for i in techs) +
        quicksum(pi[s] * (C_plus * y_plus[s] + C_minus * y_minus[s])
                 for s in scen_list),
        "minimize",
    )

    # constraints
    for s in scen_list:
        m.addCons(quicksum(u[i] for i in techs) +
                  y_plus[s] - y_minus[s] == w[s])

    m.optimize()
    sol = m.getBestSol()

    return {i: sol[u[i]] for i in techs}


# ============================================================
# 3. Solve stochastic model (baseline)
# ============================================================

u_sto = solve_stochastic(w, pi)
print("\n=== Stochastic solution (u_i) ===")
for i in techs:
    print(f"{i}: {u_sto[i]:.2f} MW")


# ============================================================
# 4. Solve deterministic model using expected demand
# ============================================================

expected_w = sum(w[s] * pi[s] for s in Scen)
print("\nExpected demand =", expected_w)

# Deterministic is just one scenario with probability 1
u_det = solve_stochastic({0: expected_w}, {0: 1.0})
print("\n=== Deterministic solution (u_i) ===")
for i in techs:
    print(f"{i}: {u_det[i]:.2f} MW")


# ============================================================
# 5. COST FUNCTION FOR FUTURE MONTE CARLO TESTING
# ============================================================

def realized_cost(demand, u_policy):
    """ Given a realized demand, compute actual cost. """
    G = sum(u_policy[i] for i in techs)
    shortage = max(demand - G, 0)
    surplus = max(G - demand, 0)
    return (
        sum(cost[i] * u_policy[i] for i in techs)
        + C_plus * shortage
        + C_minus * surplus
    )


# ============================================================
# 6. MONTE CARLO comparison (single batch)
# ============================================================

N = 5000
mu, sigma = 120.0, 25.0

dem_samples = np.clip(np.random.normal(mu, sigma, N), 0, None)

cost_sto = np.array([realized_cost(d, u_sto) for d in dem_samples])
cost_det = np.array([realized_cost(d, u_det) for d in dem_samples])

print("\n=== Monte Carlo Comparison ===")
print(f"Mean cost (STO) = {cost_sto.mean():.2f}")
print(f"Mean cost (DET) = {cost_det.mean():.2f}")


# ============================================================
# 7. REPEATED sampling & accumulated (cumulative) cost plot
# ============================================================

K = 2000  # number of realizations for cumulative visualization
dem_k = np.clip(np.random.normal(mu, sigma, K), 0, None)

cum_cost_sto = np.cumsum([realized_cost(d, u_sto) for d in dem_k])
cum_cost_det = np.cumsum([realized_cost(d, u_det) for d in dem_k])

# ============================================================
# 8. Plot comparison
# ============================================================

plt.figure(figsize=(7,5))
plt.plot(cum_cost_sto, label="Stochastic policy", linewidth=2)
plt.plot(cum_cost_det, label="Deterministic policy", linewidth=2)
plt.xlabel("Sample index")
plt.ylabel("Accumulated cost (€)")
plt.title("Cumulative realized cost under random demand")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("SEP_accum.png")
# plt.show()

# ------------------------------------------------------------
# Additional plot: distributions of cost
# ------------------------------------------------------------

plt.figure(figsize=(7,5))
plt.hist(cost_sto, bins=40, alpha=0.6, label="Stochastic dispatch")
plt.hist(cost_det, bins=40, alpha=0.6, label="Deterministic dispatch")
plt.xlabel("Realized cost (€)")
plt.ylabel("Density")
plt.title("Cost distribution comparison")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("SEP_cost_dist.png")
# plt.show()

