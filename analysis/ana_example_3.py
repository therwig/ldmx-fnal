import numpy as np
import EventTree
import os
import math

from cppyy.gbl import ldmx

"""
Exploring more branches in the trees
"""

tree = EventTree.EventTree("data/out_1k_neu_1GeV_ECalFace.root")

var_names = [
    "event_hcalrechit_sumenergy",
    "hcalrechit_energy",
    "event_ecalrechit_sumenergy",
    "event_neutron_e",
    "event_neutron_pz",
    "event_neutron_kine", # kinetic energy

]

variables = dict.fromkeys(var_names, [])

for ie,event in enumerate(tree):

    # Hcal RecHits
    hcal_sumenergy = 0
    for hit in event.HcalRecHits:
        hit_energy = hit.getEnergy()
        hcal_sumenergy += hit.getEnergy()
        variables["hcalrechit_energy"].append(hit_energy)
    variables["event_hcalrechit_sumenergy"].append(hcal_sumenergy)  

    # Ecal RecHits
    ecal_sumenergy = 0
    for hit in event.EcalRecHits: ecal_sumenergy += hit.getEnergy()
    variables["event_ecalrechit_sumenergy"].append(ecal_sumenergy)

    # "Truth" or Generated Hits (not assuming detector effects)
    # this neutron is shot at the face of the Ecal, so we will look at the EcalScoringPlaneHits
    truth_hit = ldmx.SimTrackerHit()
    found_neutron = False
    for t in event.EcalScoringPlaneHits:
        if t.getTrackID()!=1: continue # get first hit 
        if t.getPdgID()!=2112: continue # neutron particle id = 2112
        position = t.getPosition()
        z = position[2] # z is 3rd component of position
        # find truth track hit between 0 and 1
        # print(z)
        if z<690.5: continue
        truth_hit = t
        found_neutron = True
        break
            
    if found_neutron:
        truth_e = truth_hit.getEnergy()
        truth_p = truth_hit.getMomentum()
        truth_ke = math.sqrt(pow(truth_p[0],2)+pow(truth_p[1],2)+pow(truth_p[2],2))
    else:
        truth_e = 0
        truth_p = [0,0,0]
        truth_ke = 0
    variables["event_neutron_e"].append(truth_e)
    variables["event_neutron_pz"].append(truth_p[2])
    variables["event_neutron_kine"].append(truth_ke)
        
for key,arr in variables.items():
    variables[key] = np.array(arr)
    
print(variables)
