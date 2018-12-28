from __future__ import print_function
import sys
import json
from ortools.constraint_solver import pywrapcp


def main():
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)

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

    for i in range(len(data)):
      solver.Add(solver.Sum([result_dishes[j,k] == i for j in range(num_meals) for k in range(num_dishes)]) <= 1)

    #Each week one dish is fish
    fish_dish_list = [i for i in range(len(data)) if data[i]["fish"]]

    solver.Add(solver.Sum([result_dishes[j,k] == fish_dish_list[i] for i in range(len(fish_dish_list)) for j in range(num_meals) for k in range(num_dishes)]) == 1)

    #Each week one dish is bean

    bean_dish_list = [i for i in range(len(data)) if data[i]["bean"]]

    solver.Add(solver.Sum([result_dishes[j,k] == bean_dish_list[i] for i in range(len(bean_dish_list)) for j in range(num_meals) for k in range(num_dishes)]) == 1)


    #Each day one dish is soup
    soup_dish_list = [i for i in range(len(data)) if data[i]["soup"]]

    for j in range(num_meals):
      solver.Add(solver.Sum([result_dishes[j,k] == soup_dish_list[i] for i in range(len(soup_dish_list)) for k in range(num_dishes)]) == 1)

    #Each day one dish is meat (pork, chicken, beef, fish, seafood)
    meat_dish_list = [i for i in range(len(data)) if data[i]["pork"] or data[i]["chicken"] or data[i]["beef"] or data[i]["fish"] or data[i]["seafood"]]

    # for j in range(num_meals):
      # solver.Add(solver.Sum([result_dishes[j,k] == meat_dish_list[i] for i in range(len(meat_dish_list)) for k in range(num_dishes)]) == 1)

    #Each day one dish is pure vegi
    pure_vegi_dish_list = [i for i in range(len(data)) if data[i]["vegitable"] and i not in meat_dish_list and i not in soup_dish_list]
    
    for j in range(num_meals):
      solver.Add(solver.Sum([result_dishes[j,k] == pure_vegi_dish_list[i] for i in range(len(pure_vegi_dish_list)) for k in range(num_dishes)]) == 1)

    #Each day up to one dish is pork
    pork_dish_list = [i for i in range(len(data)) if data[i]["pork"]]
    for j in range(num_meals):
      solver.Add(solver.Sum([result_dishes[j,k] == pork_dish_list[i] for i in range(len(pork_dish_list)) for k in range(num_dishes)]) == 1)

    #Each day up to one dish is chicken
    egg_dish_list = [i for i in range(len(data)) if data[i]["egg"]]
    for j in range(num_meals):
      solver.Add(solver.Sum([result_dishes[j,k] == egg_dish_list[i] for i in range(len(egg_dish_list)) for k in range(num_dishes)]) == 1)  

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
      print("Meal", i+1)
      print_vegi_dish = -1
      print_meat_dish = -1
      print_soup_dish = -1
      for j in range(num_dishes):
        dish_index = collector.Value(0,result_dishes[(i,j)])
        if dish_index in pure_vegi_dish_list:
          print_vegi_dish = dish_index
        elif dish_index in soup_dish_list:
          print_soup_dish = dish_index
        else:
          print_meat_dish = dish_index
        
      print("Vegi", data[print_vegi_dish]["name"])
      print("Meat", data[print_meat_dish]["name"])
      print("Soup", data[print_soup_dish]["name"])
      print()

    # solver.NextSolution()
    # print(dishes_flat)

if __name__ == "__main__":
    main()
