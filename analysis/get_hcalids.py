import numpy as np
import EventTree
import os

"""
This script needs python bindings installed in ldmx.
"""
import libDetDescr as DD

tree = EventTree.EventTree("data/ngun_870mm_0.80_gev.root")

array_hcalrechit_layer = []
array_hcalrechit_strip = []

for ie,event in enumerate(tree):
    # loop over collection
    for hit in event.HcalRecHits:
        hit_id = hit.getID()
        hit_hcalid = DD.HcalID(hit_id)
        print(hit_id)
        raw_id = hit.raw()
        section = hit.section() 
        layer = hit.layer()
        strip = hit.strip()

