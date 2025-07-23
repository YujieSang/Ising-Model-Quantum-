from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import Aer
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.visualization import plot_histogram
import numpy as np
import matplotlib.pyplot as plt 

# Logical circuit
def Ising_1D(N, J, g, dt, r):

    qc = QuantumCircuit(N, N)
    # H
    for i in range(N):
        qc.h(i)
    qc.barrier()
    
    # Trotterization of time evo operator
    for _ in range(r):
        # ZZ
        for i in range(N - 1):
            qc.cx(i, i + 1)
            qc.rz(2 * J * dt, i + 1)
            qc.cx(i, i + 1)
        # Transverse-field
        for i in range(N):
            qc.rx(2 * g * dt, i)
        qc.barrier()
    
    qc.measure(range(N), range(N))
    return qc

# parameters
N = 5           # number of spins/qubits
J = 1.0         
g = 0.5         
t_total = 1.0   # total time
r = 4           # # of Trotter slices
dt = t_total / r

qc = Ising_1D(N, J, g, dt, r)
fig = qc.draw(output='mpl', fold=100)
# Local simulator
sim_counts = Aer.get_backend("aer_simulator").run(
    transpile(qc, Aer.get_backend("aer_simulator")), shots=1024
).result().get_counts()

# Choose backend
service = QiskitRuntimeService()
backend = service.backend("ibm_rensselaer")

# ISA circuit
isa_circuit = generate_preset_pass_manager(
    optimization_level=2, backend=backend
).run(qc)


print()


# run
sampler = Sampler(backend)
opts = sampler.options
opts.dynamical_decoupling.enable = True  # suppress decoherence
opts.twirling.enable_gates = True 
job = sampler.run([isa_circuit], shots=1024)
result = job.result()
counts_hw = result[0].data.c.get_counts()

# Visualise
plot_histogram([sim_counts, counts_hw],
               legend=["Simulator", backend.name],
               sort="desc")
plt.show()
