import numpy as np

def normalize(_d, to_sum=True, copy=True):
	# d is a (n x dimension) np array
	d = _d if not copy else np.copy(_d)
	d -= np.min(d, axis=0)
	d /= (np.sum(d, axis=0) if to_sum else np.ptp(d, axis=0))
	return d

a = np.random.random((5, 3))
a1 = np.array([390, 133, 295, 358, 60, 106, 93, 123])
a2 = np.array([390, 143, 304, 238, 46, 107, 120, 132])
a3 = np.array([[390, 133, 295, 358, 60, 106, 93, 123],
              [390, 143, 304, 238, 46, 107, 120, 132]])

a3t = a3.T

normalized_a1 = a1 / np.sqrt(np.sum(a1**2))
normalized_a2 = a2 / np.sqrt(np.sum(a2**2))
normalized_a3 = a3 / np.sqrt(np.sum(a3**2))
normalized_a3t = a3t / np.sqrt(np.sum(a3t**2))
# an = normalize(a, to_sum=False, copy=False)
# a1n = normalize(a1, to_sum=False, copy=False)
# a1n = normalize(a1, to_sum=False, copy=False)
# a3n = normalize(a3, to_sum=False, copy=False)
# a3n = normalize(a3, copy=False)
# a2n = normalize(a2)

print(a3t)
print(normalized_a3t)