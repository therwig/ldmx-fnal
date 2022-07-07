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
        "event_nhcalrechit",  # number of rechits
        "event_nhcalrechit_1pe",  # number of rechits with 
        "event_nhcalrechit_5pe",  # number of rechits with
        "event_hcalrechit_sumenergy",  # summed energy of the event
        "event_hcalrechit_maxenergy",  # max energy of the event
        "event_hcalrechit_maxlayer",  # maximum layer reached in the event
        "event_hcalrechit_maxlayer_nhits",  # maximum layer with number of hits
        "event_hcalrechit_maxlayer_z",  # maximum layer reached in the z direction
        "event_hcalrechit_maxpe",  # maximum potential energy 
        "event_hcalrechit_maxpe_layer",  # layer where the maximum potential energy occured (?)
        "event_hcalrechit_sumpe",  # sum of the potential energies of the event
        "event_hcalrechit_isback", # determines if the hit occurs at the back of the Hcal
        "event_hcalrechit_nuniquelayers",  # number of unique layers interacted with in the event
        "hcalrechit_uniquelayer",  # unique layer of each hit
        "hcalrechit_uniquelayer_nhits",  # number of hits in each unique hit
        "hcalrechit_uniquelayer_nstrips",  # number of strips interacted with in each unique layer in each event
        "hcalrechit_uniquelayer_sumenergy",  # summed energy in each unique layer for each event

        "hcalrechit_x",  # x position of each rechit
        "hcalrechit_y",  # y position of each rechit
	"hcalrechit_z",  # z position of each rechit
        "hcalrechit_energy",  # energy of each rechit
        "hcalrechit_layer",  # layer of each rechit
        "hcalrechit_section",  # section of each rechit
        "hcalrechit_strip",  # strip of each rechit
        "hcalrechit_pe",  # 
        
        "event_neutron_e",  # energy of the neutron in each event
        "event_neutron_pz",  # momentum of the neutron in the z direction of each event
        "event_neutron_kine",  # neutron kinetic energy in each event
        "event_neutron_theta",  # angle of the event

        "event_hcalrechit_minPEover1_zval",  # z value of the lowest-PE recHit with over 1 PE of reco energy
    ]

    variables_by_filename = {}

    for filename,tree in trees_by_filename.items():

        variables = dict.fromkeys(var_names)
        for key in variables.keys():
            variables[key] = []
            
        for ie,event in enumerate(tree):

            if arg.max_events!=-1 and ie>=arg.max_events: continue
            
            # Hcal RecHits
            hits = dict.fromkeys([
                "energy","xpos","ypos","zpos",
                "layer","strip","section","pe",
            ])
            for key in hits.keys(): hits[key] = []

            ih = 0
            for ih,hit in enumerate(event.HcalRecHits):
                hits["energy"].append(hit.getEnergy())
                hits["xpos"].append(hit.getXPos())
                hits["ypos"].append(hit.getYPos())
                hits["zpos"].append(hit.getZPos())
                hits["pe"].append(hit.getPE())
                
                #hit_id = hit.getID()
                #hit_hcalid = DD.HcalID(hit_id)
                #hits["section"].append(hit_hcalid.section())
                #hits["layer"].append(hit_hcalid.layer())
                #hits["strip"].append(hit_hcalid.strip())

                hits["section"].append(hit.getSection())
                hits["layer"].append(hit.getLayer())
                hits["strip"].append(hit.getStrip())
                
            nhits = ih
            variables["event_nhcalrechit"].append(nhits)
            
            variables["hcalrechit_x"].extend(hits["xpos"])
            variables["hcalrechit_y"].extend(hits["ypos"])
            variables["hcalrechit_z"].extend(hits["zpos"])
            variables["hcalrechit_energy"].extend(hits["energy"])
            variables["hcalrechit_layer"].extend(hits["layer"])
            variables["hcalrechit_strip"].extend(hits["strip"])
            variables["hcalrechit_section"].extend(hits["section"])
            variables["hcalrechit_pe"].extend(hits["pe"])

            for key,item in hits.items(): hits[key] = np.array(item)
                        
            if nhits > 0:
                variables["event_nhcalrechit_1pe"].append((hits["pe"]>1).sum())
                variables["event_nhcalrechit_5pe"].append((hits["pe"]>5).sum())

                if (hits["pe"]>1).sum() > 0:
                    pes = hits["pe"]
                    highPE_indices = np.where(pes>1)
                    minPE_Val = np.min(pes[highPE_indices])
                    minPE_Index = np.argmin(pes[highPE_indices])
                    minPE_Z = hits["zpos"][minPE_Index]
                    print(pes, highPE_indices, pes[highPE_indices], minPE_Val, minPE_Index, minPE_Z)
                    variables["event_hcalrechit_minPEover1_zval"].append(minPE_Z)
                    
                variables["event_hcalrechit_sumenergy"].append(np.sum(hits["energy"]))
                variables["event_hcalrechit_maxenergy"].append(np.max(hits["energy"]))
            
                maxlayer = np.max(hits["layer"])
                mask_maxlayer = hits["layer"]==maxlayer
                hits_maxlayer = np.where(mask_maxlayer)
                z_maxlayer = np.unique(hits["zpos"][mask_maxlayer])[0]
                variables["event_hcalrechit_maxlayer"].append(maxlayer)
                variables["event_hcalrechit_maxlayer_nhits"].append(len(list(hits_maxlayer)))
                variables["event_hcalrechit_maxlayer_z"].append(z_maxlayer)

                variables["event_hcalrechit_maxpe"].append(np.max(hits["pe"]))
                variables["event_hcalrechit_maxpe_layer"].append(np.unique(hits["layer"][hits["pe"]==np.max(hits["pe"])])[0])

                variables["event_hcalrechit_sumpe"].append(np.sum(hits["pe"]))

                isback = 0
                if (hits["section"]==0).sum()>0: isback = 1
                variables["event_hcalrechit_isback"].append(isback)
                
                uniquelayer = np.unique(hits["layer"])
                sumenergy = []
                nhits = []
                strips = []
                nstrips = []
                for layer in uniquelayer:
                    masklayer = (hits["layer"] == layer)
                    sumenergy.append(np.sum(hits["energy"][masklayer]))
                    nhits.append(masklayer.sum())                    
                    strips.extend(list(hits["strip"][masklayer]))
                    nstrips.append(len(list(hits["strip"][masklayer])))

                variables["event_hcalrechit_nuniquelayers"].append(len(list(uniquelayer)))
                variables["hcalrechit_uniquelayer"].extend(list(uniquelayer))
                variables["hcalrechit_uniquelayer_nhits"].extend(list(nhits))
                variables["hcalrechit_uniquelayer_nstrips"].extend(nstrips)
                variables["hcalrechit_uniquelayer_sumenergy"].extend(sumenergy)
                
            # "Truth" neutrons
            for id_particle in event.SimParticles:
                part = id_particle.second
                if part.getPdgID()==2112:
                    energy = part.getEnergy()
                    momentum = part.getMomentum()
                    mass = part.getMass()
                    variables["event_neutron_e"].append(energy)
                    variables["event_neutron_pz"].append(momentum[2])
                    variables["event_neutron_kine"].append(energy - mass)
                    neutron = r.TLorentzVector()
                    neutron.SetPxPyPzE(momentum[0],momentum[1],momentum[2],energy)
                    variables["event_neutron_theta"].append(neutron.Theta())

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
