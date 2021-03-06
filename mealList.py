from __future__ import print_function
from __future__ import division
from ortools.sat.python import cp_model
import sys
import json
import random
import uuid

def getMealList(request):
    with open('data.json', encoding='utf8') as json_data:
        data = json.load(json_data)

    # Creates the model.
    model = cp_model.CpModel()

    num_meals = request['num_meals']
    num_dishes = request['num_dishes']
    num_fish_per_week = request['num_fish_per_week']
    num_bean_per_week = request['num_bean_per_week']
    num_vegi = request['num_vegi']
    num_soup = request['num_soup']
    num_food_interval = request['num_food_interval']
    num_seafood_interval = request['num_seafood_interval']

    num_food = len(data)
    shuffling = True
    # shuffling = False
    # debug = True
    debug = False

    # add rules counter
    rule_counter = 0

    #shuffle json data
    if shuffling:
      random.shuffle(data)
    #write data to file
    if debug:
      for i in range(len(data)):
        data[i]["id"] = i
        # data[i]["uuid"] = str(uuid.uuid4())
        
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
        rule_counter += 1

    #Each dish can only be on menu once per week
    for i in range(num_food):
      model.Add(sum(result_dishes[j,k,i] for j in range(num_meals) for k in range(num_dishes)) <= 1)
      rule_counter += 1

    #Each week "num_fish_per_week" dish is fish
    fish_dish_list = [i for i in range(len(data)) if data[i]["fish"]]

    model.Add(sum(result_dishes[j,k,fish_dish_list[i]] for i in range(len(fish_dish_list)) for j in range(num_meals) for k in range(num_dishes)) == num_fish_per_week)
    rule_counter += 1

    #Each week "num_bean_per_week" dish is bean

    bean_dish_list = [i for i in range(len(data)) if data[i]["bean"]]

    model.Add(sum(result_dishes[j,k,bean_dish_list[i]] for i in range(len(bean_dish_list)) for j in range(num_meals) for k in range(num_dishes)) == num_bean_per_week)
    rule_counter += 1


    #Each day "num_soup" dish is soup
    soup_dish_list = [i for i in range(len(data)) if data[i]["soup"]]

    for j in range(num_meals):
      model.Add(sum(result_dishes[j,k,soup_dish_list[i]] for i in range(len(soup_dish_list)) for k in range(num_dishes)) == num_soup)
      rule_counter += 1

    #Each day "num_vegi" dish is pure vegi (not soup, not pork, egg, chicken, beef, fish, seafood)
    pure_vegi_dish_list = [i for i in range(len(data)) if data[i]["vegitable"] and i not in soup_dish_list]
    
    for j in range(num_meals):
      model.Add(sum(result_dishes[j,k,pure_vegi_dish_list[i]] for i in range(len(pure_vegi_dish_list)) for k in range(num_dishes)) == num_vegi)
      rule_counter += 1

    #Same incredient appear only once in "num_food_interval" days 
    
    ingredient = {} #ingredient["排骨"]=[0,2,5,23]
    for i in range(len(data)):
      for item in data[i]["ingredient"]:
        if item == "":
          continue
        if item not in ingredient:
          ingredient[item] = []
        ingredient[item].append(i)
    
    if debug:
      for index, item in ingredient.items():
        print (index, end=":")
        for food in item:
          print (data[food]["name"].split(" -- ")[0], end=" ")
        print()

    for foodList in ingredient.values():
      for j in range(num_meals - (num_food_interval - 1)):
        model.Add(sum(result_dishes[day,k,foodList[i]] for i in range(len(foodList)) for k in range(num_dishes) for day in range(j, j+num_food_interval) ) <= 1)
        rule_counter += 1

    #Seafood (include fish) appear only once in "num_seafood_interval" days
    seafood_dish_list = [i for i in range(len(data)) if data[i]["seafood"]]

    for j in range(num_meals - (num_seafood_interval - 1)):
      model.Add(sum(result_dishes[day,k,seafood_dish_list[i]] for i in range(len(seafood_dish_list)) for k in range(num_dishes) for day in range(j, j+num_seafood_interval) ) <= 1)
      rule_counter += 1

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    output = []
    if status == cp_model.FEASIBLE:
      for i in range(num_meals):
          if debug: print("Meal", i+1)
          print_vegi_dish = []
          print_meat_dish = []
          print_soup_dish = []
          for j in range(num_dishes):
            for k in range(num_food):
              if solver.Value(result_dishes[i,j,k]):
                if k in pure_vegi_dish_list:
                  print_vegi_dish.append(k)
                elif k in soup_dish_list:
                  print_soup_dish.append(k)
                else:
                  print_meat_dish.append(k)
                break
          dishes = []
          for m in print_vegi_dish:
            if debug: print("Vegi", data[m]["name"])
            dishes.append({"type": "Vegi", "name": data[m]["name"], "uuid": data[m]["uuid"], "shoppingList": data[m]["shoppingList"]})
          for m in print_meat_dish:
            if debug: print("Meat", data[m]["name"])
            dishes.append({"type": "Meat", "name": data[m]["name"], "uuid": data[m]["uuid"], "shoppingList": data[m]["shoppingList"]})
          for m in print_soup_dish:
            if debug: print("Soup", data[m]["name"])
            dishes.append({"type": "Soup", "name": data[m]["name"], "uuid": data[m]["uuid"], "shoppingList": data[m]["shoppingList"]})
          if debug: print()
          output.append(dishes)
          

          
    if debug:
      print()
      print('Statistics')
      print('  - number of rules : %i' % rule_counter)
      print('  - conflicts       : %i' % solver.NumConflicts())
      print('  - branches        : %i' % solver.NumBranches())
      print('  - wall time       : %f ms' % solver.WallTime())
    return output


