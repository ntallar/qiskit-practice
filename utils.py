from qiskit import QuantumRegister, ClassicalRegister
from qiskit import execute, Aer
from random import randint
import matplotlib.pyplot as plt

##############################################################
## Constructors
##############################################################

# IsZero  => |0>
# !IsZero => |1>
# Requires phi to be initially on zero
def constructComputationalBase(qc, phi, isZero):
    if not isZero:
        qc.x(phi)

# IsZero  => |+>
# !IsZero => |->
# Requires phi to be initially on zero
def constructSuperpositionBase(qc, phi, isZero):
    constructComputationalBase(qc, phi, isZero)
    transformCompToSuperposition(qc, phi)

# IsFirstZero && IsSecondZero    -> |shi+>
# IsFirstZero && !IsSecondZero   -> |tri+>
# !IsFirstZero && IsSecondZero   -> |shi->
# !IsFirstZero && !IsSecondZero  -> |tri->
# Requires phi and rho to be initially on zero
def constructBellBase(qc, phi, rho, isFirstZero, isSecondZero):
    constructComputationalBase(qc, phi, isFirstZero)
    constructComputationalBase(qc, rho, isSecondZero)
    transformCompToBell(qc, phi, rho)

# Returns 0.5|0><0| + 0.5|1><1|
# Requires phi to be initially on zero
def constructMixedState(qc, phi):
    randomName = str(randint(0, 100))

    random = QuantumRegister(1, 'random' + randomName)
    randomMeasurement = ClassicalRegister(1, 'random' + randomName + 'Measurement')
    qc.add_register(random)
    qc.add_register(randomMeasurement)

    qc.h(random)
    qc.measure(random[0], randomMeasurement[0])
    qc.x(phi[0]).c_if(randomMeasurement, 1)


##############################################################
## Base transformers
##############################################################

# Transforms computational base to +/- base
#  |0> -> |+>
#  |1> -> |->
def transformCompToSuperposition(qc, q):
    qc.h(q)

# Transforms +/- base to computational base
#  |+> -> |0>
#  |-> -> |1>
def transformSuperpositionToComp(qc, q):
    transformCompToSuperposition(qc, q)

# Transforms computational base to bell base
#  |00> -> |shi+>
#  |01> -> |tri+>
#  |10> -> |shi->
#  |11> -> |tri->
def transformCompToBell(qc, q1, q2):
    qc.h(q1)
    qc.cx(q1, q2)

# Transforms bell base to computational base
#  |shi+> -> |00>
#  |tri+> -> |01>
#  |shi-> -> |10>
#  |tri-> -> |11>
def transformBellToComp(qc, q1, q2):
    qc.cx(q1, q2)
    qc.h(q1)

##############################################################
## Simulator helpers
##############################################################

# Parses the result of an experiment, showing only the distribution of the result classical register
# @param gc: the result of get_counts
# @param resultIndex: the index on the gc keys string that is the result
def parseGetCounts(gc, resultIndex):
    parsedGetCounts = {}

    for classicalRegisterValues in gc:
        classicalRegisterResult = classicalRegisterValues.split(" ")[resultIndex]
        if classicalRegisterResult in parsedGetCounts:
            parsedGetCounts[classicalRegisterResult] += gc[classicalRegisterValues]
        else:
            parsedGetCounts[classicalRegisterResult] = gc[classicalRegisterValues]
    return parsedGetCounts

def drawCircuit(qc):
    print(qc)

    #qc.draw(output='mpl')
    #plt.show()

def executeQuantumCircuit(backendName, numberOfRepetitions, qc):
    backend = Aer.get_backend(backendName)
    job = execute(qc, backend=backend, shots=numberOfRepetitions)
    job_result = job.result()
    return job_result.get_counts(qc)