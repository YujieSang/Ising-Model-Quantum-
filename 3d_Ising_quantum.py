from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

def Ising_3D(Lx, Ly, Lz, J, g, dt, r):
    """
    3-D Transverse-Field Ising Model (TFIM) on an Lx×Ly×Lz cubic lattice.

    H = -J Σ_<n,n'> Z_n Z_n'  - g Σ_n X_n
        nearest neighbours <n,n'> along x, y, z.

    Parameters
    ----------
    Lx, Ly, Lz : int
        Linear dimensions of the lattice.
    J, g       : float
        Coupling (ZZ) and transverse-field strengths.
    dt         : float
        Duration of one Trotter slice (total time / r).
    r          : int
        Number of Trotter slices.
    """
    N = Lx * Ly * Lz
    qc = QuantumCircuit(N, N)

    # 1) Prepare |+>^⊗N
    for q in range(N):
        qc.h(q)
    qc.barrier()

    # 2) r Trotter slices
    for _ in range(r):
        # ---- X-direction neighbours ----
        for x in range(Lx - 1):
            for y in range(Ly):
                for z in range(Lz):
                    i =  x      *Ly*Lz + y*Lz + z
                    j = (x + 1) *Ly*Lz + y*Lz + z
                    qc.cx(i, j)
                    qc.rz(2 * J * dt, j)
                    qc.cx(i, j)

        # ---- Y-direction neighbours ----
        for x in range(Lx):
            for y in range(Ly - 1):
                for z in range(Lz):
                    i = x*Ly*Lz +  y     *Lz + z
                    j = x*Ly*Lz + (y + 1)*Lz + z
                    qc.cx(i, j)
                    qc.rz(2 * J * dt, j)
                    qc.cx(i, j)

        # ---- Z-direction neighbours ----
        for x in range(Lx):
            for y in range(Ly):
                for z in range(Lz - 1):
                    i = x*Ly*Lz + y*Lz +  z
                    j = x*Ly*Lz + y*Lz + (z + 1)
                    qc.cx(i, j)
                    qc.rz(2 * J * dt, j)
                    qc.cx(i, j)

        # ---- Transverse-field RX gates ----
        for q in range(N):
            qc.rx(2 * g * dt, q)

        qc.barrier()

    # 3) Measurements
    qc.measure(range(N), range(N))
    return qc


# ---------- Example run ----------
Lx, Ly, Lz = 3, 3, 3          # 2×2×2 lattice → 8 qubits
J, g       = 1.0, 0.5
t_total    = 1.0
r          = 2                # Trotter slices
dt         = t_total / r

qc3d = Ising_3D(Lx, Ly, Lz, J, g, dt, r)

# Visualisation (may get tall for larger lattices)
fig = qc3d.draw(output='mpl', fold=100)
plt.title(f"3D Ising Circuit ({Lx}×{Ly}×{Lz}, r={r})")
plt.show()

# Simulation (optional)
sim = AerSimulator()
job = sim.run(qc3d, shots=1024)
counts = job.result().get_counts()
print("3-D TFIM measurement counts:", counts)

plt.figure(figsize=(6,4))
plot_histogram(counts)
plt.title("3-D Ising model Outcome Distribution")
plt.show()
