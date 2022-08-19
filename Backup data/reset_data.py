import pickle

a={'gun': ['glock'], 'gold': 0, 'level': 1, 'kill': 0}

with open('stats.pickle', 'wb') as f:
    pickle.dump(a, f)

with open('stats.pickle', 'rb') as f:
     a = pickle.load(f)
 
print(a)

input()