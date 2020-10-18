from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
import numpy as np
from utils import *
from swaptest import initSwapTest, runSwapTest
from teleport import initTeleport, runTeleport

def teleportOneQubitAndCheckEquality(qubitBuilder):
    qc = QuantumCircuit()

    # State to teleport
    phi = QuantumRegister(1, 'phi')
    qc.add_register(phi)
    qubitBuilder(qc, phi)

    # Create states required for teleport + equality check
    (alice, bob, phiMeasurement, aliceMeasurement) = initTeleport(qc, phi, "")
    (aux, auxMeasurement) = initSwapTest(qc)

    # State to check equality with
    expectedBob = QuantumRegister(1, 'expected_bob')
    qc.add_register(expectedBob)
    qubitBuilder(qc, expectedBob)

    qc.barrier()

    # Teleport
    _ = runTeleport(qc, phi, alice, bob, phiMeasurement, aliceMeasurement)
    qc.barrier()

    # Check equality
    runSwapTest(qc, [bob], [expectedBob], aux, auxMeasurement)

    # Show the quantum circuit before executing
    drawCircuit(qc)

    # Execute the circuit
    classicalValuesResult = executeQuantumCircuit('qasm_simulator', 1024, qc)
    print(parseGetCounts(classicalValuesResult, 0))

def teleportOneOfTwoQubitsAndCheckEquality(qubitsBuilder):
    qc = QuantumCircuit()

    # State to teleport
    phi = QuantumRegister(1, 'phi')
    rho = QuantumRegister(1, 'rho')
    qc.add_register(phi)
    qc.add_register(rho)
    qubitsBuilder(qc, phi, rho)

    # Create states required for teleport + equality check
    (alice, bob, phiMeasurement, aliceMeasurement) = initTeleport(qc, phi, "")
    (aux, auxMeasurement) = initSwapTest(qc)

    # State to check equality with
    expectedBob1 = QuantumRegister(1, 'expected_bob1')
    expectedBob2 = QuantumRegister(1, 'expected_bob2')
    qc.add_register(expectedBob1)
    qc.add_register(expectedBob2)
    qubitsBuilder(qc, expectedBob1, expectedBob2)

    qc.barrier()

    # Teleport
    _ = runTeleport(qc, phi, alice, bob, phiMeasurement, aliceMeasurement)
    qc.barrier()

    # Check equality
    runSwapTest(qc, [bob, rho], [expectedBob1, expectedBob2], aux, auxMeasurement)

    # Show the quantum circuit before executing
    drawCircuit(qc)

    # Execute the circuit
    classicalValuesResult = executeQuantumCircuit('qasm_simulator', 1024, qc)
    print(parseGetCounts(classicalValuesResult, 0))

def teleportTwoQubitsAndCheckEquality(qubitsBuilder):
    qc = QuantumCircuit()

    # State to teleport
    phi = QuantumRegister(1, 'phi')
    rho = QuantumRegister(1, 'rho')
    qc.add_register(phi)
    qc.add_register(rho)
    qubitsBuilder(qc, phi, rho)

    # Create states required for teleport + equality check
    (alice1, bob1, phiMeasurement1, aliceMeasurement1) = initTeleport(qc, phi, "1")
    (alice2, bob2, phiMeasurement2, aliceMeasurement2) = initTeleport(qc, phi, "2")
    (aux, auxMeasurement) = initSwapTest(qc)

    # State to check equality with
    expectedBob1 = QuantumRegister(1, 'expected_bob1')
    expectedBob2 = QuantumRegister(1, 'expected_bob2')
    qc.add_register(expectedBob1)
    qc.add_register(expectedBob2)
    qubitsBuilder(qc, expectedBob1, expectedBob2)

    qc.barrier()

    # Teleport
    _ = runTeleport(qc, phi, alice1, bob1, phiMeasurement1, aliceMeasurement1)
    qc.barrier()
    _ = runTeleport(qc, rho, alice2, bob2, phiMeasurement2, aliceMeasurement2)
    qc.barrier()

    # Check equality
    runSwapTest(qc, [bob1, bob2], [expectedBob1, expectedBob2], aux, auxMeasurement)

    # Show the quantum circuit before executing
    drawCircuit(qc)

    # Execute the circuit
    classicalValuesResult = executeQuantumCircuit('qasm_simulator', 1024, qc)
    print(parseGetCounts(classicalValuesResult, 0))

if __name__ == "__main__":

    # Teleporting computational base
    teleportOneQubitAndCheckEquality(lambda qc, phi : constructComputationalBase(qc, phi, True))
    teleportOneQubitAndCheckEquality(lambda qc, phi : constructComputationalBase(qc, phi, False))

    # Teleporting |+> and |->
    teleportOneQubitAndCheckEquality(lambda qc, phi : constructSuperpositionBase(qc, phi, True))
    teleportOneQubitAndCheckEquality(lambda qc, phi : constructSuperpositionBase(qc, phi, False))

    # Teleporting one of the qubits from bell base
    teleportOneOfTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, True, True))
    teleportOneOfTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, True, False))
    teleportOneOfTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, False, True))
    teleportOneOfTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, False, False))

    # Teleporting bell base
    teleportTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, True, True))
    teleportTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, True, False))
    teleportTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, False, True))
    teleportTwoQubitsAndCheckEquality(lambda qc, phi, rho : constructBellBase(qc, phi, rho, False, False))
