# -*- coding: utf-8 -*-
import sys

import nptyping
import pyqubo


def pathsWeightChecker(citiesSize: int, pathsWeight: nptyping.NDArray[int]) -> bool:

    if len(pathsWeight) == citiesSize and len(pathsWeight[0]) == citiesSize:
        return True

    else:
        print(
            """
            There is something wrong!
            Cities: {0}
            Correct Array Size: {0} x {0}
            Passed Array Size: {1} x {2}
        """.format(
                citiesSize, len(pathsWeight), len(pathsWeight[0])
            )
        )
        return False


def TSPHamiltonian(citiesSize: int, pathsWeight: nptyping.NDArray[int]):

    if pathsWeightChecker(citiesSize, pathsWeight):
        pass
    else:
        sys.exit()

    timeSteps = citiesSize
    x = pyqubo.Array.create("x", (citiesSize - 1, citiesSize - 1), "BINARY")

    # goal -> start
    costHamiltonian = sum(pathsWeight[citiesSize - 1, start] * x[start][0] for start in range(0, citiesSize - 1))
    # print("goal -> start Hamiltonian:")
    # print(costHamiltonian)

    # on the way
    costHamiltonian += sum(
        pathsWeight[i, j] * x[i][time] * x[j][time + 1]
        for time in range(0, timeSteps - 2)
        for i in range(0, citiesSize - 2)
        for j in range(i + 1, citiesSize - 1)
    )
    # print("on the way Hamiltonian:")
    # print(costHamiltonian)

    # on the way -> goal
    costHamiltonian += sum(pathsWeight[j, citiesSize - 1] * x[j][timeSteps - 2] for j in range(0, citiesSize - 1))
    # print("on the way to goal Hamiltonian:")
    # print(costHamiltonian)

    ## Constrain
    time_constrain_val = sum(
        (x[i][time] - 1) ** 2 for i in range(0, citiesSize - 1) for time in range(0, timeSteps - 1)
    )

    timeConstrain = pyqubo.Constraint(time_constrain_val, label="time")

    visit_constrain_val = sum((x[i][time]) ** 2 for time in range(0, timeSteps - 1) for i in range(0, citiesSize - 1))

    visitConstrain = pyqubo.Constraint(visit_constrain_val, label="city")

    # print("timeConstrain:", timeConstrain)
    # print("visitConstrain:", visitConstrain)

    hamiltonian = (
        costHamiltonian
        + pyqubo.Placeholder("lamTime") * timeConstrain
        + pyqubo.Placeholder("lamVisit") * visitConstrain
    )
    # print("Hamiltonian:")
    # print(hamiltonian)

    return hamiltonian


def makeHamiltonian(citiesSize: int, pathsWeight: nptyping.NDArray[int]):
    costFunction = TSPHamiltonian(citiesSize, pathsWeight)

    return costFunction.compile()


if __name__ == "__main__":
    pass
