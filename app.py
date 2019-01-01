from __future__ import print_function
from __future__ import division
from flask import Flask
from flask import jsonify
from flask import request
from foodList import getFoodList
from mealList import getMealList
from food import addFood
from food import updateFood
from food import removeFood


app = Flask(__name__)

@app.route('/foodList/get' , methods=['POST'])
def getFoodListWrapper():
    return jsonify(getFoodList(request.get_json()))

@app.route('/mealList/get' , methods=['POST'])
def getMealListWrapper():
    return jsonify(getMealList(request.get_json()))

@app.route('/food/add' , methods=['POST'])
def addFoodWrapper():
    return jsonify(addFood(request.get_json()))

@app.route('/food/update' , methods=['POST'])
def updateFoodWrapper():
    return jsonify(updateFood(request.get_json()))

@app.route('/food/remove' , methods=['POST'])
def removeFoodWrapper():
    return removeFood(removeFood(request.get_json()))
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)