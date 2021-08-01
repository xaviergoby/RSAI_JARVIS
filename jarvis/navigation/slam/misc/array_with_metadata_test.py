import numpy as np
# import h5py
#
# somearray = np.random.random(100)
#
# f = h5py.File('test.hdf', 'w')
#
# dataset = f.create_dataset('my_data', data=somearray)
#
# # Store attributes about your dataset using dictionary-like access
# dataset.attrs['git id'] = 'yay this is a string'
#
# f.close()


import h5py
filename = "test.hdf"

with h5py.File(filename, "r") as f:
    # List all groups
    print(f['git id'])
    print(f"keys: {f.keys()}")
    # print("Keys: %s" % f.keys())
    # a_group_key = list(f.keys())[0]

    # Get the data
    # data = list(f[a_group_key])