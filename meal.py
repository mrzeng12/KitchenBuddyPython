from __future__ import print_function
from __future__ import division
from ortools.sat.python import cp_model
import sys
import json
import random

def main():
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)

    # Creates the model.
    model = cp_model.CpModel()

    num_meals = 7
    num_dishes = 3
    num_food = len(data)
    shuffling = False

    #shuffle json data
    if shuffling:
      random.shuffle(data)
    #write data to file
    for i in range(len(data)):
      data[i]["id"] = i
      
    with open('shuffled_data.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
    #result_dishes is true if meal i dish j uses food k
    result_dishes = {}

    for i in range(num_meals):
      for j in range(num_dishes):
        for k in range(num_food):
          result_dishes[(i,j,k)] = model.NewBoolVar("result_dishes(%i,%i,%i)" % (i,j,k))

    #Each meal, each dish can have only one food
    for i in range(num_meals):
      for j in range(num_dishes):
        model.Add(sum(result_dishes[i,j,k] for k in range(num_food)) == 1)

    #Each dish can only be on menu once per week
    for i in range(num_food):
      model.Add(sum(result_dishes[j,k,i] for j in range(num_meals) for k in range(num_dishes)) <= 1)

    #Each week one dish is fish
    fish_dish_list = [i for i in range(len(data)) if data[i]["fish"]]

    model.Add(sum(result_dishes[j,k,fish_dish_list[i]] for i in range(len(fish_dish_list)) for j in range(num_meals) for k in range(num_dishes)) == 1)

    #Each week one dish is bean

    bean_dish_list = [i for i in range(len(data)) if data[i]["bean"]]

    model.Add(sum(result_dishes[j,k,bean_dish_list[i]] for i in range(len(bean_dish_list)) for j in range(num_meals) for k in range(num_dishes)) == 1)


    #Each day one dish is soup
    soup_dish_list = [i for i in range(len(data)) if data[i]["soup"]]

    for j in range(num_meals):
      model.Add(sum(result_dishes[j,k,soup_dish_list[i]] for i in range(len(soup_dish_list)) for k in range(num_dishes)) == 1)

    #Each day one dish is pure vegi (not soup, not pork, egg, chicken, beef, fish, seafood)
    meat_dish_list = [i for i in range(len(data)) if data[i]["egg"] or data[i]["pork"] or data[i]["chicken"] or data[i]["beef"] or data[i]["fish"] or data[i]["seafood"]]
    pure_vegi_dish_list = [i for i in range(len(data)) if data[i]["vegitable"] and i not in meat_dish_list and i not in soup_dish_list]
    
    for j in range(num_meals):
      model.Add(sum(result_dishes[j,k,pure_vegi_dish_list[i]] for i in range(len(pure_vegi_dish_list)) for k in range(num_dishes)) == 1)

    #Same incredient only appears no more than 2 times a week
    
    ingredient = {} #ingredient["排骨"]=[0,2,5,23]
    for i in range(len(data)):
      ingredient_list = data[i]["ingredient"].split("，")
      for item in ingredient_list:
        if item == "":
          continue
        if item not in ingredient:
          ingredient[item] = []
        ingredient[item].append(i)
    
    for index, item in ingredient.items():
      print (index, end=":")
      for food in item:
        print (data[food]["name"], end=" ")
      print()

    for foodList in ingredient.values():
      model.Add(sum(result_dishes[j,k,foodList[i]] for i in range(len(foodList)) for j in range(num_meals) for k in range(num_dishes)) <= 2)

    #Same incredient two not appear in two consecutive days 
    #todo

    
    #Same incredient only appears once in a day
    for foodList in ingredient.values():
      for j in range(num_meals):
        model.Add(sum(result_dishes[j,k,foodList[i]] for i in range(len(foodList)) for k in range(num_dishes)) <= 1)


    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinterWithLimit(result_dishes, data, num_meals, num_dishes, pure_vegi_dish_list, soup_dish_list, 1)
    solver.SearchForAllSolutions(model, solution_printer)
    
    print()
    print('Statistics')
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f ms' % solver.WallTime())

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, result_dishes, data, num_meals, num_dishes, pure_vegi_dish_list, soup_dish_list, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._result_dishes = result_dishes
        self._data = data
        self._num_meals = num_meals
        self._num_dishes = num_dishes
        self._num_food = len(data)
        self._pure_vegi_dish_list = pure_vegi_dish_list
        self._soup_dish_list = soup_dish_list
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print()
        for i in range(self._num_meals):
          print("Meal", i+1)
          print_vegi_dish = []
          print_meat_dish = []
          print_soup_dish = []
          for j in range(self._num_dishes):
            for k in range(self._num_food):
              if self.Value(self._result_dishes[i,j,k]):
                if k in self._pure_vegi_dish_list:
                  print_vegi_dish.append(k)
                elif k in self._soup_dish_list:
                  print_soup_dish.append(k)
                else:
                  print_meat_dish.append(k)
                break
          for i in print_vegi_dish:
            print("Vegi", self._data[i]["name"])
          for i in print_meat_dish:
            print("Meat", self._data[i]["name"])
          for i in print_soup_dish:
            print("Soup", self._data[i]["name"])
          print()

        if self._solution_count >= self._solution_limit:
            print('Stop search after %i solutions' % self._solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self.__solution_count

if __name__ == "__main__":
    main()
