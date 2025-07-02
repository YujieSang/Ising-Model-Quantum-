
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

def Ising_1D(N, J, g, dt, r):

    qc = QuantumCircuit(N, N)
    # init state
    for i in range(N):
        qc.h(i)
    qc.barrier()
    
    # Trotterization
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
N = 10           # number of spins/qubits
J = 1.0         
g = 0.5         
t_total = 1.0   # total time
r = 4           # # of Trotter slices
dt = t_total / r

qc = Ising_1D(N, J, g, dt, r)

# Visual 
fig = qc.draw(output='mpl', fold=100)
sim = AerSimulator()
job = sim.run(qc, shots=1024)
counts = job.result().get_counts()
print("Measurement counts:", counts)
plt.figure(figsize=(6,4))
plot_histogram(counts)
plt.title("Outcome Distribution")
plt.show()