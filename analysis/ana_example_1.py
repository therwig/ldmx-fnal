import numpy as np
import EventTree
import os

tree = EventTree.EventTree("data/ngun_870mm_0.80_gev.root")

#print(tree)

array_rechitenergy = []
array_sumenergy = []

for ie,event in enumerate(tree):
    # event number
    #print(ie)
    # event
    #print(event)

    sumenergy = 0
    # loop over collection
    for hit in event.HcalRecHits:
        array_rechitenergy.append(hit.getEnergy())
        sumenergy += hit.getEnergy()

    array_sumenergy.append(sumenergy)

    
# transform array
rechitenergy = np.array(array_rechitenergy)
sumenergy = np.array(array_sumenergy)

my_dict = {
    "rechitenergy": rechitenergy,
    "sumenergy": sumenergy,
}

# print dictionary
print(my_dict)

import pickle
os.system(f"mkdir -p output/")
with open("output/example_1.pkl", "wb") as pickle_file:
    pickle.dump(my_dict,pickle_file)
