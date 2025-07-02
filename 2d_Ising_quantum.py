from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

def Ising_2D(Lx, Ly, J, g, dt, r):

    N = Lx * Ly
    qc = QuantumCircuit(N, N)

    # 1) Initialize 
    for q in range(N):
        qc.h(q)
    qc.barrier()

    # 2) r Trotter slices
    for _ in range(r):
        # a) Horizontal ZZ couplings
        for x in range(Lx):
            for y in range(Ly - 1):
                i = x*Ly + y
                j = i + 1
                qc.cx(i, j)
                qc.rz(2 * J * dt, j)
                qc.cx(i, j)

        # b) Vertical   ZZ couplings
        for x in range(Lx - 1):
            for y in range(Ly):
                i = x*Ly + y
                j = (x+1)*Ly + y
                qc.cx(i, j)
                qc.rz(2 * J * dt, j)
                qc.cx(i, j)

        # c) Transverse-field
        for q in range(N):
            qc.rx(2 * g * dt, q)

        qc.barrier()

    # 3) Measurements
    qc.measure(range(N), range(N))
    return qc

# parameters
Lx, Ly = 3, 3     
J = 1.0
g = 0.5
t_total = 1.0
r = 2             
dt = t_total / r

# visualize
qc2d = Ising_2D(Lx, Ly, J, g, dt, r)
fig = qc2d.draw()


# simulate & plot
sim = AerSimulator()
job = sim.run(qc2d, shots=1000)
counts = job.result().get_counts()
print("Measurement counts:", counts)

plt.figure(figsize=(6,4))
plot_histogram(counts)
plt.title("2D Outcome Distribution (Qantum)")
plt.show()
