#!flask/bin/python
from __future__ import print_function
from flask import Flask
from flask import jsonify
from ortools.linear_solver import pywraplp

app = Flask(__name__)
@app.route('/')
def main():
    solver = pywraplp.Solver('SolveSimpleSystem',
                           pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    # Create the variables x and y.
    x = solver.NumVar(0, 1, 'x')
    y = solver.NumVar(0, 2, 'y')
    # Create the objective function, x + y.
    objective = solver.Objective()
    objective.SetCoefficient(x, 1)
    objective.SetCoefficient(y, 1)
    objective.SetMaximization()
    # Call the solver and display the results.
    solver.Solve()
    print('Solution:')
    print('x = ', x.solution_value())
    print('y = ', y.solution_value())
    result = {}
    result["x"] = x.solution_value()
    result["y"] = y.solution_value()
    return jsonify(result)
    # return 'x = ' + str(x.solution_value()) + 'y = ' + str(y.solution_value())
if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(host='192.168.1.21', port=5010)
