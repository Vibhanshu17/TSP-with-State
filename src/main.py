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
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite


def dict2AnsList(solutionsDict, citiesSize):

    orderList = []
    for i in range(citiesSize - 1):
        for j in range(citiesSize - 1):
            if solutionsDict["x[" + str(i) + "][" + str(j) + "]"] == 1:
                orderList.append(j)

    print("ORDER LIST:")
    print(orderList)

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


if __name__ == "__main__":
    cities = 5

    citiesLocation, paths = makeDemoData(citiesSize=cities)
    print("==== cities location ==================================")
    print(citiesLocation)

    print("\n==== paths array ==================================")
    print(paths)

    # hamiltonian = TSPHamiltonian(citiesSize=cities, pathsWeight=paths)
    feedDict = {"lamTime": 250.0, "lamVisit": 250.0}  # {"lamTime": 250.0, "lamVisit": 250.0}

    # model = hamiltonian.compile()
    model = makeHamiltonian(citiesSize=cities, pathsWeight=paths)
    qubo, _ = model.to_qubo(feed_dict=feedDict)

    sampler = EmbeddingComposite(DWaveSampler())
    sampleSet = sampler.sample_qubo(qubo, num_reads=5)

    print("RAW SAMPLE SET\n", sampleSet)

    Solution = sampleSet.first.sample
    print("\nSolution:")
    print(Solution)

    orderList = dict2AnsList(solutionsDict=Solution, citiesSize=cities)
    orderList = list(map(lambda x: x + 1, orderList))
    orderList.append(0)

    plotMap(citiesLocation=citiesLocation, orderList=orderList)

    sys.exit()
