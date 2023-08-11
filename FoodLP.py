from pulp import *
import csv

serving = dict()
energy = dict()
carbohydrates = dict()
protein = dict()
calcium = dict()
iron =dict()
cost = dict()
food = []


# ------------------------- Data ---------------------------------#
with open('Food List.csv', 'r') as food_data:  # opens the food list file created from original data for reading
    csv_read = csv.DictReader(food_data)  # reads data as ordered dictionary
    for foods in csv_read:
        serving[foods['Food']] = float(foods['Serving Size(g)'])
        energy[foods['Food']] = float(foods['Energy (Kcal)'])
        carbohydrates[foods['Food']] = float(foods['Carbohydrates(g)'])
        protein[foods['Food']] = float(foods['Protein(g)'])
        calcium[foods['Food']] = float(foods['Calcium(mg)'])
        iron[foods['Food']] = float(foods['Iron(mg)'])
        cost[foods['Food']] = float(foods['Cost per Serving($)'])
        food.append(foods['Food'])

# Create model
model = LpProblem("FoodProblem", LpMinimize)

## ---------------- Variables -------------------------#
FOODS_EATEN = LpVariable.dicts("SERVINGSIZE",food,lowBound=0)

## ---------------- Objective Function -------------------------#
model += lpSum([FOODS_EATEN[f] * cost[f] for f in food])

## ------------------ Constraints ------------------------------#
model += lpSum([energy[f] * FOODS_EATEN[f] for f in food]) <= 2000
model += lpSum([carbohydrates[f] * FOODS_EATEN[f] for f in food]) <= 130
model += lpSum([protein[f] * FOODS_EATEN[f] for f in food]) >= 60
model += lpSum([iron[f] * FOODS_EATEN[f] for f in food]) >= 8
model += lpSum([iron[f] * FOODS_EATEN[f] for f in food]) <= 9
model += lpSum([calcium[f] * FOODS_EATEN[f] for f in food]) >= 1000
model += lpSum([calcium[f] * FOODS_EATEN[f] for f in food]) <= 1200

for f in food:
    model += lpSum([serving[f] * FOODS_EATEN[f]]) <= (2.5 * serving[f])
    model += lpSum([serving[f] * FOODS_EATEN[f]]) >= (1 * serving[f])

model.solve()

if model.status != 1:
    print("Modeled failed to solve")
else:
    print("Objective function value at optimal = $%.2f" %  float(value(model.objective)))
    for f in food:
        print("\t" + f + ": " + str(FOODS_EATEN[f].value()))


