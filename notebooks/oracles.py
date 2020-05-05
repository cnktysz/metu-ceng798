from qiskit import *
import numpy as np
from math import pi

def dj_oracle(case, n):
    # We need to make a QuantumCircuit object to return
    # This circuit has n+1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = QuantumCircuit(n+1)
    
    # First, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        b = np.random.randint(1,2**n)
        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        b_str = format(b, '0'+str(n)+'b')
        # Next, we place the first X-gates. Each digit in our binary string 
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit 
        # as the target:
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Case in which oracle is constant
    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)
    
    return oracle_qc.to_gate()

def oracle1(qc):
	oracle_circuit = QuantumCircuit(2)
	if np.random.randint(2) == 1:
		oracle_circuit.x(0)

	qc.append(oracle_circuit.to_gate(), range(2))

def oracle2(qc, n):
    if np.random.randint(2) == 1:
        case = "constant"
    else:
        case = "balanced"

    oracle_gate = dj_oracle(case, n)
    qc.append(oracle_gate, range(n+1))
    return case

def simonOracle(qc, n):
    # Let us first generate a random bit string s with length n
    s = ""
    for i in range(n):
        if np.random.randint(2) == 1:
            s += '1'
        else:
            s += '0'

    # Now that we have our bitstring let us initialze a quantum circuit.
    oracle_circuit = QuantumCircuit(2*n)

    # The first thing we do is to copy the contents of †he first register
    # to the second register. We can achieve this easily by CNOT gates, for each
    # qubit.
    for i in range(n):
        oracle_circuit.cx(i, n+i)

    # Now, let us find the set of indices i at which s[i]=1
    setOfIndices = []
    for i in range(n):
        if (s[i] == "1"):
            setOfIndices.append(i)

    # We also need the least significant index at which s[i]=1
    if (len(setOfIndices)):
        least_significant_index = setOfIndices[-1]

    # What we want to do is apply CNOTS where the control qubit is always the qubit 
    # at the least_index position of the first register, and we will go over all indices
    # at which s[i] = 1.
    for target in setOfIndices:
        oracle_circuit.cx(least_significant_index, (n+target))

    # Don't forget the second register begins at index n. So if you want to go to index 
    # target on the second register, you should index it with n+target.

    # Just to make our mapping function a little more interesting we will apply X gates to
    # all the qubits in the second register. 
    # The only time we should avoid doing this operation is when s=00...0 bitstring. 
    # When s is in that form, setOfIndices will be an empty list.
    if (len(setOfIndices)):
        for i in range(n):
            oracle_circuit.x(n+i)

    # Our oracle is finished, let us convert it to a gate and append it to qc.
    oracle_gate = oracle_circuit.to_gate()
    qc.append(oracle_gate, range(2*n))

    return s

def stringDotProduct(str1, str2):
    result = 0
    for i in range(len(str1)):
        if (str1[i] == '1' and str2[i] == '1'):
            result += 1
    return (result%2)


def simonSolver(orthogonal_set):
    # This is basically the same as saying you have less equations than unknowns.
    if len(orthogonal_set) < len(orthogonal_set[0]):
        print("You need more strings!!!!!!!!")
        return ""

    # We define n to be the length of the strings. 
    # We assume all of them to be of the same length.
    n = len(orthogonal_set[0])

    # This basically goes over all possible integer values from 0 all the way
    # up to 2**n-1, the biggest number you can represent with n bits. For each
    # value, it converts it to binary form, padding the beginning with 0s to 
    # make its length n.
    setOfAllPossibleBitStrings = [ format(b, '0'+str(n)+'b') for b in range(2**n) ]

    # Our algorithm is a brute-force one, because I couldn't think of an 
    # easier way to do it. Although this is inefficient, I trust you not to run 
    # the code with big values of n :) 
    # That being said, the algorithm just goes over all possible bitstrings and checks
    # whether that particular string is orthogonal to each bitstring in the orthogonal_set.
    # If it is, it equates that to the result.
    # One important thing to notice is 000..0 bitstring is always orthonogal to any set
    # of bitstrings, and since setOfAllPossibleBitStrings contains the bitstrings in increasing
    # order, we return the latest one as our result.
    result = ""
    for string in setOfAllPossibleBitStrings:
        orthogonal_counter = 0
        for orthoElement in orthogonal_set:
            if (stringDotProduct(string, orthoElement) == 0):
                orthogonal_counter += 1

        if (orthogonal_counter == len(orthogonal_set)):
            result = string
    return result




# QFT FUNCTIONSS

def qft_rotations(circuit, n):
    if n == 0: # Exit function if circuit is empty
        return circuit
    n -= 1 # Indexes start from 0
    circuit.h(n) # Apply the H-gate to the most significant qubit
    for qubit in range(n):
        # For each less significant qubit, we need to do a
        # smaller-angled controlled rotation: 
        circuit.cu1(pi/2**(n-qubit), qubit, n)
    # At the end of our function, we call the same function again on
    # the next qubits (we reduced n by one earlier in the function)
    qft_rotations(circuit, n)
    
def swap_registers(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

def qft(circuit, n):
    """QFT on the first n qubits in circuit"""
    qft_rotations(circuit, n)
    swap_registers(circuit, n)
    return circuit

def qft_oracle(qc, n):
    oracle_circuit = QuantumCircuit(n)
    secret_string = ""
    for i in range(n):
        if np.random.randint(2) == 1:
            secret_string += '1'
        else:
            secret_string += '0'

    for i in range(n):
        if secret_string[i] == "1":
            oracle_circuit.x(i)

    qft(oracle_circuit, n)
    oracle_gate = oracle_circuit.to_gate()
    qc.append(oracle_gate, range(n))
    return secret_string
    
