import pickle

with open('tutors.pickle', 'rb') as handle:
    d = pickle.load(handle)
print([d[tutorPhone]["email"] for tutorPhone in d])
