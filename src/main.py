# -*- coding: utf-8 -*-

import os
import sys

import pyqubo
from demo.fakeData import makeDemoData
from plot.plotMap import plotMap
from pyquboSolver.tsp.costHamiltonian import TSPHamiltonian, makeHamiltonian

# additional import
from deprecated import deprecated
import neal


def dict2AnsList(solutionsDict, citiesSize):
    ansDicts = [solutionsDict["x"][i] for i in range(citiesSize - 1)]
    orderList = [key for i in range(citiesSize - 1) for key, value in ansDicts[i].items() if value == 1]

    if len(orderList) != (citiesSize - 1):
        print(
            """
            Solutions doesn't fulfill requirements.
            There are cities you don't visit.
        """
        )
        sys.exit()

    for i in range(citiesSize - 1):
        if i not in orderList:
            print(
                """
                Solutions doesn't fulfill requirements.
                There are cities you visit more than once.
            """
            )
            sys.exit()

    return orderList


"""
if __name__ == "__main__":
    cities = 5

    citiesLocation, paths = makeDemoData(citiesSize=cities)

    hamiltonian = TSPHamiltonian(citiesSize=cities, pathsWeight=paths)
    feedDict = {"lamTime": 250.0, "lamVisit": 250.0}

    qubo, offset = hamiltonian.compile().to_qubo(feed_dict=feedDict)
    rawSolution = pyqubo.solve_qubo(qubo)
    decodeSolution, broken, energy = hamiltonian.compile().decode_solution(
        rawSolution, vartype="BINARY", feed_dict=feedDict
    )

    orderList = dict2AnsList(solutionsDict=decodeSolution, citiesSize=cities)
    orderList = list(map(lambda x: x + 1, orderList))
    orderList.append(0)

    plotMap(citiesLocation=citiesLocation, orderList=orderList)

    sys.exit()
"""

if __name__ == "__main__":
    cities = 5

    citiesLocation, paths = makeDemoData(citiesSize=cities)

    hamiltonian = TSPHamiltonian(citiesSize=cities, pathsWeight=paths)

    feedDict = {"lamTime": 250.0, "lamVisit": 250.0}

    qubo, offset = hamiltonian.compile().to_qubo(feed_dict=feedDict)
    rawSolution = pyqubo.solve_qubo(qubo)

    print("RAW SAMPLE\n", rawSolution)
    decodeSolution = hamiltonian.compile().decode_sample(rawSolution, vartype="BINARY", feed_dict=feedDict)

    print("Decoded Sample\n")
    print(decodeSolution.sample)

    ## Some problems with dict2AnsList function
    ## Try defining a custom dict2Ans function and uncomment the lines below

    # orderList = dict2AnsList(solutionsDict=decodeSolution.sample, citiesSize=cities)
    # orderList = list(map(lambda x: x + 1, orderList))
    # orderList.append(0)

    # plotMap(citiesLocation=citiesLocation, orderList=orderList)

    sys.exit()
