import numpy as np
import EventTree
import os

"""
Exploring more branches in the trees
"""

tree = EventTree.EventTree("data/ngun_870mm_0.80_gev.root")

var_names = [
    "event_hcalsumenergy",
    "hcalrechit_energy",
]

variables = dict.fromkeys(var_names, [])

for ie,event in enumerate(tree):

    hcal_sumenergy = 0
    for hit in event.HcalRecHits:
        hit_energy = hit.getEnergy()
        hcal_sumenergy += hit.getEnergy()

        variables["hcalrechit_energy"].append(hit_energy)

    variables["event_hcalsumenergy"].append(hcal_sumenergy)

    ecal_sumenergy = 0
    for hit in event.EcalRecHits: ecal_sumenergy += hit.getEnergy()
    variables["event_ecalsumenergy"].append(ecal_sumenergy)

    
