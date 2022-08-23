import numpy as np
import os,math,sys
import argparse
import pickle

import EventTree
from cppyy.gbl import ldmx
# import libDetDescr as DD
import ROOT as r

"""
Neutron analysis
"""

def main(arg):
    print(arg.input_files)
    trees_by_filename = dict.fromkeys(arg.input_files)
    for filename in trees_by_filename.keys():
        trees_by_filename[filename] = EventTree.EventTree(filename)
        
    var_names = [
        "hcalsimhit_Edep",  # Edep of each simhit
        "hcalsimhit_Position",  # Position of each simhit
    ]

    variables_by_filename = {}

    for filename,tree in trees_by_filename.items():

        variables = dict.fromkeys(var_names)
        for key in variables.keys():
            variables[key] = []
            
        for ie,event in enumerate(tree):
            if ie!=23: continue
            if ie>23: break

            if arg.max_events!=-1 and ie>=arg.max_events: continue
            
            # Hcal SimHits
            hits = dict.fromkeys([
                "Edep",
                "Position",
            ])
            for key in hits.keys(): hits[key] = []

            ih = 0
            for ih,hit in enumerate(event.HcalSimHits):
                hits["Edep"].append(hit.getEdep())
                hits["Position"].append(hit.getPosition())

            nhits = ih
            variables["hcalsimhit_Edep"].extend(hits["Edep"])
            variables["hcalsimhit_Position"].extend(hits["Position"])
            for key,item in hits.items(): hits[key] = np.array(item)
            

        # print(variables)
        for key,arr in variables.items():
            variables[key] = np.array(arr)

        variables_by_filename[filename] = variables

    os.system(f"mkdir -p output/")
    with open(f"output/{arg.output}.pkl", "wb") as pickle_file:
        pickle.dump(variables_by_filename,pickle_file)

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(f'ldmx python3 {sys.argv[0]}')
    parser.add_argument('input_files',nargs='+')
    parser.add_argument('--output',required=True,help='Output name of pickle file (without extension)')
    parser.add_argument('--max_events',default=-1,type=int)
    arg = parser.parse_args()

    main(arg)
