from pyscipopt import Model, quicksum
import matplotlib.pyplot as plt
import networkx as nx

# ============================================
# Data
# ============================================

# Buses
N = [1, 2, 3, 4, 5, 6, 7, 8]

# Reference bus
ref_bus = 1

# Demands d_i (MW)
d = {
    1: 50.0,
    2: 30.0,
    3: 20.0,
    4: 60.0,
    5: 40.0,
    6: 40.0,
    7: 20.0,
    8: 10.0,
}

# Net generation g_i (MW) – two generators
g = {
    1: 0.0,
    2: 0.0,
    3: 0.0,
    4: 0.0,
    5: 0.0,
    6: 0.0,
    7: 100.0,
    8: 150.0,
} 

# Quadratic shedding penalty coefficient (Eur/MW^2)
c_shed = {i: 10.0 for i in N}

# --------------------------------------------------
# Existing lines L_ex: (i, j, F_ell, B_ell)
L_ex = [
    (7, 5, 100.0, 5.0), 
    (8, 6, 80.0, 5.0),  
    (8, 5, 80.0, 5.0),
    (5, 1, 20.0, 5.0),  
    (5, 2, 20.0, 5.0),  
    (6, 3, 20.0, 5.0),  
    (6, 4, 20.0, 5.0),  
    (5, 6, 10.0, 8.0),  
    # (1, 2, 50.0, 5.0),
    # (3, 4, 50.0, 5.0),
    # (7, 8, 50.0, 5.0),
]

# --------------------------------------------------
# Candidate lines L_cand: (i, j, F_k, B_k, c_k^inv)
L_cand = [
    (5, 3, 40.0, 5.0, 800.0),    
    (6, 2, 40.0, 5.0, 800.0),    
    (5, 4, 40.0, 5.0, 4000.0),   
    (6, 1, 40.0, 5.0, 4000.0),   
    (1, 3, 40.0, 5.0, 100000.0), 
    (2, 4, 40.0, 5.0, 100000.0), 
]

# Index sets
Lex_index   = list(range(len(L_ex)))
Lcand_index = list(range(len(L_cand)))


# ============================================
# Model
# ============================================

m = Model("TransmissionExpansion_DC_quadratic_shedding")

# Voltage angles θ_i (rad)
theta = {i: m.addVar(vtype="C", name=f"theta_{i}") for i in N}

# Existing line flows
f_ex = {ell: m.addVar(vtype="C", lb=0.0, name=f"f_ex_{ell}") for ell in Lex_index}

# Candidate line flows
f_new = {k: m.addVar(vtype="C", lb=0.0, name=f"f_new_{k}") for k in Lcand_index}

# Shedding(+)/spillage(−) at bus i
shed = {i: m.addVar(vtype="C", lb=None, name=f"shed_{i}") for i in N}

# Auxiliary vars for quadratic cost: aux_i ≥ shed_i^2
aux = {i: m.addVar(vtype="C", lb=0.0, name=f"aux_{i}") for i in N}

# Investment binaries
inv = {k: m.addVar(vtype="B", name=f"inv_{k}") for k in Lcand_index}

# --------- Constraints ---------

# DC flow on existing lines
for ell, (i, j, F, B) in enumerate(L_ex):
    m.addCons(f_ex[ell] == B * (theta[i] - theta[j]),
              name=f"DC_ex_{ell}")

# DC flow on candidate lines
for k, (i, j, Fk, Bk, ck) in enumerate(L_cand):
    m.addCons(f_new[k] == Bk * (theta[i] - theta[j]),
              name=f"DC_new_{k}")

# Capacity existing
for ell, (i, j, F, B) in enumerate(L_ex):
    m.addCons(f_ex[ell] <=  F, name=f"Cap_ex_up_{ell}")
    # m.addCons(f_ex[ell] >= -F, name=f"Cap_ex_lo_{ell}")

# Capacity candidate
for k, (i, j, Fk, Bk, ck) in enumerate(L_cand):
    m.addCons(f_new[k] <=  Fk * inv[k], name=f"Cap_new_up_{k}")
    # m.addCons(f_new[k] >= -Fk * inv[k], name=f"Cap_new_lo_{k}")

# Power balance at each bus:
for i in N:
    out_ex = quicksum(
        f_ex[ell] for ell, (u, v, F, B) in enumerate(L_ex) if u == i
    )
    in_ex = quicksum(
        f_ex[ell] for ell, (u, v, F, B) in enumerate(L_ex) if v == i
    )
    out_new = quicksum(
        f_new[k] for k, (u, v, Fk, Bk, ck) in enumerate(L_cand) if u == i
    )
    in_new = quicksum(
        f_new[k] for k, (u, v, Fk, Bk, ck) in enumerate(L_cand) if v == i
    )

    m.addCons(
        g[i] - d[i] + shed[i] == (out_ex - in_ex) + (out_new - in_new),
        name=f"Balance_{i}",
    )

# Reference angle
m.addCons(theta[ref_bus] == 0.0, name="RefAngle")


# Obj

# Quad trick
for i in N:
    m.addCons(aux[i] >= shed[i] * shed[i], name=f"QuadShed_{i}")

obj = quicksum(
    ck * inv[k] for k, (i, j, Fk, Bk, ck) in enumerate(L_cand)
) + quicksum(
    c_shed[i] * aux[i] for i in N
)

m.setObjective(obj, "minimize")


# ============================================
# Solve and report
# ============================================

m.optimize()

status = m.getStatus()
print("SCIP status:", status)
if status not in ["optimal", "bestsollimit"]:
    print("Warning: model not proven optimal.\n")

sol = m.getBestSol()

print("\n=== Voltage angles θ_i (rad) ===")
for i in N:
    print(f"theta[{i}] = {sol[theta[i]]:8.4f}")

print("\n=== Shedding(+)/Spillage(−) (MW) and aux ===")
for i in N:
    print(f"bus {i}: shed = {sol[shed[i]]:8.4f}, aux = {sol[aux[i]]:8.4f}")

print("\n=== Existing line flows (MW) ===")
for ell, (i, j, F, B) in enumerate(L_ex):
    print(f"({i}->{j}) f_ex[{ell}] = {sol[f_ex[ell]]:8.4f}  (cap ±{F})")

print("\n=== Candidate line decisions & flows ===")
for k, (i, j, Fk, Bk, ck) in enumerate(L_cand):
    built = int(round(sol[inv[k]]))
    print(
        f"({i}->{j}) inv[{k}] = {built}, "
        f"f_new[{k}] = {sol[f_new[k]]:8.4f}  (cap ±{Fk})"
    )

# print("\nObjective value =", m.getObjVal())

# Investment cost = sum_k c_k * inv_k
investment_cost = sum(
    ck * sol[inv[k]]
    for k, (i, j, Fk, Bk, ck) in enumerate(L_cand)
)

# Quadratic shedding cost = sum_i c_shed[i] * aux_i
shedding_cost = sum(
    c_shed[i] * sol[aux[i]]
    for i in N
)

print("\n=== Cost components ===")
print(f"Investment cost       = {investment_cost:12.4f}")
print(f"Quadratic shedding cost = {shedding_cost:12.4f}")
print(f"Total objective value = {m.getObjVal():12.4f}")


# ============================================
# Visualization: digraph before / after
# ============================================


# Much better geometry — reduces edge overlap
pos = {
    # Load buses (top arc)
    1: (0.0,  1.5),
    2: (1.0,  2.0),
    3: (2.0,  2.0),
    4: (3.0,  1.5),

    # Hubs (middle)
    5: (0.8,  0.5),
    6: (2.2,  0.5),

    # Generators (lower arc)
    7: (0.6, -0.8),
    8: (2.4, -0.8),
}

# Node colors: all blue, except generators 7 & 8
node_colors = ["tab:red" if b in (7,8) else "tab:blue" for b in N]


# Helper: add edge following flow direction
def add_flow_edge(G, i, j, flow, etype):
    """Adds the edge in the direction of the flow (if negative flow reverse)."""
    if flow >= 0:
        G.add_edge(i, j, flow=flow, type=etype)
    else:
        G.add_edge(j, i, flow=-flow, type=etype)


# ============================================
# BEFORE GRAPH (existing lines only)
# ============================================
G_before = nx.DiGraph()
G_before.add_nodes_from(N)

for ell, (i, j, F, B) in enumerate(L_ex):
    add_flow_edge(G_before, i, j, sol[f_ex[ell]], "existing")

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
nx.draw_networkx_nodes(G_before, pos, node_color=node_colors, node_size=700)
nx.draw_networkx_labels(G_before, pos)

nx.draw_networkx_edges(
    G_before, pos, arrows=True, arrowstyle='-|>', arrowsize=20,
    edge_color="black", width=1.8
)

labels_before = {(u,v): f"{d['flow']:.1f}" for u,v,d in G_before.edges(data=True)}
nx.draw_networkx_edge_labels(G_before, pos, edge_labels=labels_before, font_size=8)

plt.title("Before (existing network)")
plt.axis("off")


# ============================================
# AFTER GRAPH (existing + built + unbuilt candidates)
# ============================================
G_after = nx.DiGraph()
G_after.add_nodes_from(N)

# First: existing lines
for ell, (i, j, F, B) in enumerate(L_ex):
    add_flow_edge(G_after, i, j, sol[f_ex[ell]], "existing")

# Candidates: built and unbuilt
for k, (i, j, Fk, Bk, ck) in enumerate(L_cand):
    inv_k = sol[inv[k]]

    if inv_k > 0.5:
        # BUILT: show real flow (green dashed arrow)
        add_flow_edge(G_after, i, j, sol[f_new[k]], "built")
    else:
        # UNBUILT: show grey dashed line (NO arrows, NO flow direction)
        G_after.add_edge(i, j, flow=None, type="unbuilt")


plt.subplot(1,2,2)
nx.draw_networkx_nodes(G_after, pos, node_color=node_colors, node_size=700)
nx.draw_networkx_labels(G_after, pos)

# Separate by type
ex_edges     = [(u,v) for u,v,d in G_after.edges(data=True) if d['type']=="existing"]
built_edges  = [(u,v) for u,v,d in G_after.edges(data=True) if d['type']=="built"]
unbuilt_edges= [(u,v) for u,v,d in G_after.edges(data=True) if d['type']=="unbuilt"]

# Existing: black arrows
nx.draw_networkx_edges(
    G_after, pos, edgelist=ex_edges,
    arrows=True, arrowstyle='-|>', arrowsize=20,
    edge_color="black", width=1.8
)

# Built candidates: green dashed arrows
nx.draw_networkx_edges(
    G_after, pos, edgelist=built_edges,
    arrows=True, arrowstyle='-|>', arrowsize=20,
    edge_color="tab:green", style="dashed", width=2.4
)

# Unbuilt candidates: grey dashed, no arrows
nx.draw_networkx_edges(
    G_after, pos, edgelist=unbuilt_edges,
    arrows=False, style="dashed",
    edge_color="lightgrey", width=1.5
)

# Label flows ONLY for existing + built candidates
labels_after = {}
for u, v, d in G_after.edges(data=True):
    if d["flow"] is not None:       # built or existing
        labels_after[(u,v)] = f"{d['flow']:.1f}"

nx.draw_networkx_edge_labels(G_after, pos, edge_labels=labels_after, font_size=8)

plt.title("After (optimal extension)")
plt.axis("off")

plt.tight_layout()
# plt.savefig("transmission_expansion.png")
plt.show()

