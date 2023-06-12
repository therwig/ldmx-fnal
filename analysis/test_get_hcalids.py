import numpy as np
import EventTree
import os

"""
This script needs python bindings installed in ldmx.
"""
import libDetDescr as DD

tree = EventTree.EventTree("data/2ngun_690.60mm_2.00_gev.root")

array_hcalrechit_layer = []
array_hcalrechit_strip = []

for ie,event in enumerate(tree):
    # loop over collection
    for hit in event.HcalRecHits:
        hit_id = hit.getID()
        hit_hcalid = DD.HcalID(hit_id)
        raw_id = hit_hcalid.raw()
        section = hit_hcalid.section()
        layer = hit_hcalid.layer()
        print(layer)
        strip = hit_hcalid.strip()

