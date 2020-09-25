from scipy.spatial import distance
import numpy as np



# distance.euclidean([1, 0, 0], [0, 1, 0])

P0 = [4, 3]
P1 = [9, 3]
P2 = [9, 8]
P3 = [7, 9]
P4 = [4, 9]

PX = np.array([4, 9, 9, 7, 4])
PY = np.array([3, 3, 8, 9, 9])

# coords_mat = np.array([P0, P1, P2, P3, P4])
# print(f"coords.shape: {coords.shape}")
print(f"PX.shape: {PX.shape}")
print(f"PY.shape: {PY.shape}")
# coords = np.array([P1, P2, P3, P4])


# Find the Euclidean distances between 5 2-D coordinates:
# coords = np.array([P0, P1, P2, P3, P4])
coords = np.array([P1, P2, P3, P4])
print(f"coords.shape: {coords.shape}")
euc_ds = distance.cdist(coords, coords, 'euclidean')
print(f"Points Coordinates: \n{coords}")
print(f"coords.shape: \n{coords.shape}")
print("~"*20)
print(f"Euclidian distance between 2D points: \n{euc_ds}")

sq_euc_ds = distance.sqeuclidean(PX, PY)
print(f"\n"*3)
print(f"The 2 1D arrays (vectors) \n{PX, PY}")
print("~"*20)
print(f"The Squared Euclidean distance between the 2 1D arrays (vectors): \n{sq_euc_ds}")

from scipy.spatial.distance import pdist
std_euc_ds = pdist(coords, metric='seuclidean')
print(f"\n"*3)
print(f"The Standardized Euclidean distance between the 2 1D arrays (vectors): \n{std_euc_ds}")


from sklearn.metrics.pairwise import euclidean_distances
# get distance to origin
# sk_euc_ds_2_origin = euclidean_distances(X, [[0, 0]])
print(f"\n"*3)

# X = [P0, P1, P2, P3, P4]
# sk_euc_ds_2_origin_00 = euclidean_distances(X, [[0, 0]])
# print(f"Origin point: \n{[0, 0]}")
# print(f"X: \n{X}")
# print(f"sk_euc_ds_2_origin: \n{sk_euc_ds_2_origin_00}")

X = [P1, P2, P3, P4]
sk_euc_ds_2_origin_P0 = euclidean_distances(X, [P0])
print(f"Origin point: \n{P0}")
print(f"X: \n{X}")
print(f"sk_euc_ds_2_origin: \n{sk_euc_ds_2_origin_P0}")
print(f"\n"*3)


np.cov(euc_ds)