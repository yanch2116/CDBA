import pickle
path = '/Users/yanch/Downloads/results.pkl'
f = open(path, 'rb')
data = pickle.load(f)['pred_numpy_save']
print(data[0][0][:72])
