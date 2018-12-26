from __future__ import print_function
import sys
import json
from ortools.constraint_solver import pywrapcp


def main():
    with open('data.json') as json_data:
        data = json.load(json_data)
        # print(d)
    vegi_dish_list = [item["name"] for item in data if item["vegitable"]]
    # print(vegi_dish)

    # Creates the solver.
    solver = pywrapcp.Solver("meal_solver")

    num_meals = 3

    vegi_dish = {}

    for i in range(num_meals):
      vegi_dish[i] = solver.IntVar(
          0, len(vegi_dish_list) - 1, "vegi_dish(%i)" % i)

    vegi_dish_flat = [vegi_dish[i] for i in range(num_meals)]

  # Create the decision builder.
    db = solver.Phase(vegi_dish_flat, solver.CHOOSE_FIRST_UNBOUND,
                    solver.ASSIGN_MIN_VALUE)
  # Create the solution collector.
    solution = solver.Assignment()
    solution.Add(vegi_dish_flat)
    collector = solver.AllSolutionCollector(solution)

    solver.Solve(db, [collector])
    print("Solutions found:", collector.SolutionCount())
    print("Time:", solver.WallTime(), "ms")
    print()


if __name__ == "__main__":
    main()
