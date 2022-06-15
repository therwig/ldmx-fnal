import argparse
import EventTree
import sys,os
import numpy as np
import pickle

"""
Example configuration file to save useful arrays using EventTree for a given number of variables
"""

parser = argparse.ArgumentParser(f'ldmx python3 {sys.argv[0]}')
parser.add_argument('input_files',nargs='+')
parser.add_argument('--output',required=True,help='Output name of pickle file (without extension)')
parser.add_argument('--max_events',default=-1,type=int)
arg = parser.parse_args()

# EventTree is a class that reads out LDMX Events and loads the different collections
# here, read all the input files into `trees`
print(arg.input_files)
trees_by_filename = dict.fromkeys(arg.input_files)
for filename in trees_by_filename.keys():
    trees_by_filename[filename] = EventTree.EventTree(filename)

# the convention to name arrays is the following: collection_variablename
# for example:
#  the hcalsumenergy is per event, so the collection=event,variable=hcalsumenergy
#  the rechit energy is per rechit so the collection=hcalrechit,variable=energy
var_names = [
    "event_hcalsumenergy",
    "hcalrechit_energy",
]

# save a dictionary with all variables
variables_by_filename = {}

# loop over each of the input files and their TTree content
for filename,tree in trees_by_filename.items():

    # for each variable name, create an array
    # each of these arrays will be saved in the `variables` dictionary
    # the keys of this dictionary will be the variable names
    variables = dict.fromkeys(var_names, [])
    
    for ie, event in enumerate(tree):

        # define the sumenergy for each event (start from 0)
        hcalsumenergy = 0
        # if needed, loop over one collection
        for h in event.HcalRecHits:
            hcalsumenergy += h.getEnergy()

            # for the rechit collection we append the variable value to the list
            variables["hcalrechit_energy"].append(h.getEnergy())

        #for each collection we append the variable value to the list
        variables["event_hcalsumenergy"].append(hcalsumenergy)

    # convert the lists to numpy arrays
    for key,arr in variables.items():
        variables[key] = np.array(arr)

    # print the arrays (for debugging)
    # print(variables)
        
    # append this dictionary to the other dictionaries
    variables_by_filename[filename] = variables

#save the arrays in a pickle file in output/ directory
os.system(f"mkdir -p output/")
with open(f"output/{arg.output}.pkl", "wb") as pickle_file:
    pickle.dump(variables_by_filename,pickle_file)
