from qiskit_aer import Aer
from qiskit import transpile
from qiskit import QuantumCircuit
from matplotlib import pyplot as plt
qc = QuantumCircuit(2, 1)
qc.h(0)
qc.cx(0, 1)
qc.measure(1, 0)

from qiskit.quantum_info import Statevector
import numpy as np
initial_state = Statevector([np.sqrt(0.2), np.sqrt(0.8)])
qc.initialize(initial_state, 0)

backend = Aer.get_backend('aer_simulator')
qc_transpiled = transpile(qc, backend)
result = backend.run(qc_transpiled, shots=100).result()
counts_simulator = result.get_counts()

from qiskit.visualization import plot_histogram

from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
service = QiskitRuntimeService()
backend = service.backend('ibm_rensselaer')
job = service.run(qc_transpiled, shots=100)
result = job.result()
counts_ibm = result.get_counts()
plot_histogram([counts_simulator, counts_ibm], legend=['Simulator', 'IBM'])
plt.show()