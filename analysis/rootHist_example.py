import argparse
import EventTree
import sys,os
import numpy as np
import pickle
import ROOT

"""
Example configuration file to save useful arrays using EventTree for a given number of variables
"""

parser = argparse.ArgumentParser(f'ldmx python3 {sys.argv[0]}')
parser.add_argument('input_files',nargs='+')
parser.add_argument('--output',required=True,help='Output name of pickle file (without extension)')
parser.add_argument('--max_events',default=-1,type=int)
arg = parser.parse_args()

#EventTree is a class that reads out LDMX Events and loads the different collections
#here, read all the input files into `trees`
trees = [EventTree.EventTree(f) for f in arg.input_files]

# here we are going to add an EXTRA output file containing ROOT histograms
histFile = ROOT.TFile(f"output/{arg.output}.root", "recreate")
h1 = ROOT.TH1D("h1","",40,0,40)
h2 = ROOT.TH2D("h2","",20,-2000,2000,40,0,40)
prof = ROOT.TProfile("prof","",20,-2000,2000,0,40)

#the convention to name arrays is the following: collection_variablename
#for example:
#  the hcalsumenergy is per event, so the collection=event,variable=hcalsumenergy
#  the rechit energy is per rechit so the collection=hcalrechit,variable=energy
var_names = [
    "event_hcalsumenergy",
    "hcalrechit_energy",
]

#for each variable name, create an array
#each of these arrays will be saved in the `variables` dictionary
#the keys of this dictionary will be the variable names
variables = dict.fromkeys(var_names, [])

#loop over each of the input files and their TTree content
for tree in trees:
    for ie, event in enumerate(tree):

        #define the sumenergy for each event (start from 0)
        hcalsumenergy = 0
        #if needed, loop over one collection
        for h in event.HcalRecHits:
            hcalsumenergy += h.getEnergy()
            h1.Fill(h.getEnergy())
            h2.Fill(h.getXPos(), h.getEnergy())
            prof.Fill(h.getXPos(), h.getEnergy())
            
            #for the rechit collection we append the variable value to the list
            variables["hcalrechit_energy"].append(h.getEnergy())

        #for each collection we append the variable value to the list
        variables["event_hcalsumenergy"].append(hcalsumenergy)

#convert the list to numpy arrays
for key,arr in variables.items():
    variables[key] = np.array(arr)
        
# write out the ROOT histogram file
histFile.Write()
histFile.Close()

#save the arrays in a pickle file in output/ directory
os.system(f"mkdir -p output/")
with open(f"output/{arg.output}.pkl", "wb") as pickle_file:
    pickle.dump(variables,pickle_file)
