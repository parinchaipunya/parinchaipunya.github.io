from pyscipopt import Model, quicksum
import matplotlib.pyplot as plt

techs = ["Gas", "Coal", "Peaker"]

cost = {    # Eur/MWh
    "Gas": 20,
    "Coal": 40,
    "Peaker": 120,
}

pmax = {    # MW
    "Gas": 60,
    "Coal": 40,
    "Peaker": 100,
}

demand = 120

m = Model()

u = {}
for tech in techs:
    u[tech] = m.addVar(lb=0, ub=pmax[tech])

m.addCons( quicksum( u[tech] for tech in techs) == demand )

m.setObjective( quicksum(cost[tech]*u[tech] for tech in techs), sense="minimize" )

m.optimize()

gen = {tech: [] for tech in techs}
for tech in techs:
    gen[tech] = m.getVal(u[tech])
    print(f"u[{tech}] = {gen[tech]}")

plt.pie([gen[i] for i in techs], labels=techs)
plt.show()
