from __future__ import print_function
import sys
import json
from ortools.constraint_solver import pywrapcp


def main():
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)
        # print(d)
    # vegi_dish_list = [item["name"] for item in data if item["vegitable"]]
    # meet_dish_list = [item["name"] for item in data if item["pork"]]
    # soup_dish_list = [item["name"] for item in data if item["soup"]]

    # print(vegi_dish)

    # Creates the solver.
    solver = pywrapcp.Solver("meal_solver")

    num_meals = 4
    num_dishes = 3

    result_dishes = {}

    for i in range(num_meals):
      for j in range(num_dishes):
        result_dishes[(i,j)] = solver.IntVar(
          0, len(data) - 1, "result_dishes(%i,%i)" % (i,j))

    dishes_flat = [result_dishes[i,j] for i in range(num_meals) for j in range(num_dishes)]
    
    #Each dish can only be on menu once per week
    # dish_count = {}
    # for i in range(len(data)):
    #   dish_count[i] =  solver.IntVar('dish_count%i' % i)

    # for i in range(len(data)):
    #   solver.Add(dish_count[i]) = 

    for i in range(len(data)):
      solver.Add(solver.Sum([result_dishes[j,k] == i for j in range(num_meals) for k in range(num_dishes)]) <= 1)

    #Each week one dish is fish

    






  # Create the decision builder.
    decision_builder = solver.Phase(dishes_flat, solver.CHOOSE_FIRST_UNBOUND,
                    solver.ASSIGN_MIN_VALUE )
  # Create the solution collector.
    solution = solver.Assignment()
    solution.Add(dishes_flat)
    collector = solver.FirstSolutionCollector(solution)
    # collector = solver.AllSolutionCollector(solution)
    # collector = solver.LastSolutionCollector(solution)

    solver.Solve(decision_builder , [collector])
    print("Solutions found:", collector.SolutionCount())
    print("Time:", solver.WallTime(), "ms")
    print()


    # solver.Solve(decision_builder)
    # solver.NextSolution()
    # print(dishes_flat)
    for i in range(num_meals):
      print("Meal", i)
      for j in range(num_dishes):
        dish_index = collector.Value(0,result_dishes[(i,j)])
        print("Dish", data[dish_index]["name"])
      print()

    # solver.NextSolution()
    # print(dishes_flat)

if __name__ == "__main__":
    main()
