import numpy as np
import EventTree
import os,sys
import math
import argparse
import pickle
import ROOT as r

from cppyy.gbl import ldmx

"""
Exploring more branches in the trees
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
        "hcalrechit_pe",

        "event_neutron_e",  # energy of the neutron in each event
        "event_neutron_pz",  # momentum of the neutron in the z direction of each event
        "event_neutron_kine",  # neutron kinetic energy in each event
        "event_neutron_theta",  # angle of the event

        "2d_cluster_strips",
        "2d_cluster_energy",
        "2d_cluster_nHits",
        "2d_cluster_layer",
        "2d_cluster_centroidX",
        "2d_cluster_centroidY",
        "2d_cluster_centroidZ",
        "2d_cluster_rmsX",
        "2d_cluster_rmsY",
        "2d_cluster_rmsZ",
        "2d_cluster_time",
        "2d_cluster_depth",
        "2d_cluster_nclusters",  # number of clusters per event
        "2d_cluster_maxenergy",  # energy of highest energy cluster per event
        "2d_cluster_sumenergy",
        "2d_cluster_seedenergy",

        "3d_cluster_strips",
        "3d_cluster_energy",
        "3d_cluster_nHits",
        "3d_cluster_n2D", # number of 2d clusters
        "3d_cluster_layer", # number of seed layer
        "3d_cluster_centroidX",
        "3d_cluster_centroidY",
        "3d_cluster_centroidZ",
        "3d_cluster_rmsX",
        "3d_cluster_rmsY",
        "3d_cluster_rmsZ",
        "3d_cluster_time",
        "3d_cluster_depth", #depth of 3d cluster
        "3d_cluster_nclusters",  # number of clusters per event
        "3d_cluster_maxenergy",  # energy of highest energy cluster per event
        "3d_cluster_sumenergy",
        "3d_cluster_seedenergy",
    ]

    variables_by_filename = {}

    for filename,tree in trees_by_filename.items():

        variables = dict.fromkeys(var_names, [])
        for key in variables.keys():
            variables[key] = []

        for ie,event in enumerate(tree):

            # if ie!=42: continue  # uncomment these lines to analyze clusters for just one event
            # if ie>42: break  # you can change the number in between runs to look at a differnet event

            if arg.max_events!=-1 and ie>arg.max_events: continue

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

            # 2D-Clusters
            clusters = dict.fromkeys([
                "strips", "energy",
                "nHits", "n2d", "layer",
                "centroidX", "centroidY", "centroidZ",
                "rmsX", "rmsY", "rmsZ",
                "seedenergy", "time", "depth",
            ])
            for key in clusters.keys():
                clusters[key] = []

            ic = 0
            for ic,cluster in enumerate(event.Hcal2DClusters):
                # print(dir(cluster))  # uncomment and run with one event to print attributes you can get
                strips = cluster.getStrips()
                # print(list(strips))
                clusters["strips"].extend(list(strips))

                clusters["energy"].append(cluster.getEnergy())
                clusters["nHits"].append(cluster.getNHits())
                clusters["layer"].append(cluster.getLayer())

                clusters["centroidX"].append(cluster.getCentroidX())
                clusters["centroidY"].append(cluster.getCentroidY())
                clusters["centroidZ"].append(cluster.getCentroidZ())
                clusters["rmsX"].append(cluster.getRMSX())
                clusters["rmsY"].append(cluster.getRMSY())
                clusters["rmsZ"].append(cluster.getRMSZ())

                clusters["seedenergy"].append(cluster.getSeedEnergy())
                clusters["time"].append(cluster.getTime())
                clusters["depth"].append(cluster.getDepth())

            # 3D-Clusters
            clusters_3d = dict.fromkeys([
                "strips", "energy",
                "nHits", "n2d", "layer",
                "centroidX", "centroidY", "centroidZ",
                "rmsX", "rmsY", "rmsZ",
                "seedenergy", "time", "depth",
            ])
            for key in clusters_3d.keys():
                clusters_3d[key] = []

            ic = 0
            for ic,cluster in enumerate(event.Hcal3DClusters):
                # print(dir(cluster))  # uncomment and run with one event to print attributes you can get
                # for this dir, you might have to keep guessing event numbers as some won't have any 3d clusters
                strips = cluster.getStrips()
                # print(list(strips))
                clusters_3d["strips"].extend(list(strips))

                clusters_3d["energy"].append(cluster.getEnergy())
                clusters_3d["nHits"].append(cluster.getNHits())
                clusters_3d["layer"].append(cluster.getLayer())

                clusters_3d["centroidX"].append(cluster.getCentroidX())
                clusters_3d["centroidY"].append(cluster.getCentroidY())
                clusters_3d["centroidZ"].append(cluster.getCentroidZ())
                clusters_3d["rmsX"].append(cluster.getRMSX())
                clusters_3d["rmsY"].append(cluster.getRMSY())
                clusters_3d["rmsZ"].append(cluster.getRMSZ())

                clusters_3d["seedenergy"].append(cluster.getSeedEnergy())
                clusters_3d["time"].append(cluster.getTime())
                clusters_3d["depth"].append(cluster.getDepth())

            nclusters = ic
            nhits=ih

            variables["event_nhcalrechit"].append(nhits)
            variables["hcalrechit_x"].extend(hits["xpos"])
            variables["hcalrechit_y"].extend(hits["ypos"])
            variables["hcalrechit_z"].extend(hits["zpos"])
            variables["hcalrechit_energy"].extend(hits["energy"])
            variables["hcalrechit_layer"].extend(hits["layer"])
            variables["hcalrechit_strip"].extend(hits["strip"])
            variables["hcalrechit_section"].extend(hits["section"])
            variables["hcalrechit_pe"].extend(hits["pe"])

            variables["2d_cluster_strips"].extend(clusters["strips"])
            variables["2d_cluster_energy"].extend(clusters["energy"])
            variables["2d_cluster_nHits"].extend(clusters["nHits"])
            variables["2d_cluster_layer"].extend(clusters["layer"])
            variables["2d_cluster_centroidX"].extend(clusters["centroidX"])
            variables["2d_cluster_centroidY"].extend(clusters["centroidY"])
            variables["2d_cluster_centroidZ"].extend(clusters["centroidZ"])
            variables["2d_cluster_rmsX"].extend(clusters["rmsX"])
            variables["2d_cluster_rmsY"].extend(clusters["rmsY"])
            variables["2d_cluster_rmsZ"].extend(clusters["rmsZ"])
            variables["2d_cluster_seedenergy"].extend(clusters["seedenergy"])
            variables["2d_cluster_time"].extend(clusters["time"])
            variables["2d_cluster_depth"].extend(clusters["depth"])

            variables["3d_cluster_strips"].extend(clusters_3d["strips"])
            variables["3d_cluster_energy"].extend(clusters_3d["energy"])
            variables["3d_cluster_nHits"].extend(clusters_3d["nHits"])
            variables["3d_cluster_layer"].extend(clusters_3d["layer"])
            variables["3d_cluster_centroidX"].extend(clusters_3d["centroidX"])
            variables["3d_cluster_centroidY"].extend(clusters_3d["centroidY"])
            variables["3d_cluster_centroidZ"].extend(clusters_3d["centroidZ"])
            variables["3d_cluster_rmsX"].extend(clusters_3d["rmsX"])
            variables["3d_cluster_rmsY"].extend(clusters_3d["rmsY"])
            variables["3d_cluster_rmsZ"].extend(clusters_3d["rmsZ"])
            variables["3d_cluster_seedenergy"].extend(clusters_3d["seedenergy"])
            variables["3d_cluster_time"].extend(clusters_3d["time"])
            variables["3d_cluster_depth"].extend(clusters_3d["depth"])

            for key,item in hits.items(): hits[key] = np.array(item)

            if nhits > 0:
                variables["event_nhcalrechit_1pe"].append((hits["pe"]>1).sum())
                variables["event_nhcalrechit_5pe"].append((hits["pe"]>5).sum())

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

            for key,item in clusters.items(): clusters[key] = np.array(item)

            nclusters_3d = len(event.Hcal3DClusters)
            nclusters_2d = len(event.Hcal2DClusters)
            if nclusters_2d>0:
                variables["2d_cluster_maxenergy"].append(np.max(clusters["energy"]))
                variables["2d_cluster_sumenergy"].append(np.sum(clusters["energy"]))
            else:
                variables["2d_cluster_maxenergy"].append(float(0))
                variables["2d_cluster_sumenergy"].append(float(0))
            if nclusters_3d>0:
                variables["3d_cluster_maxenergy"].append(np.max(clusters_3d["energy"]))
                variables["3d_cluster_sumenergy"].append(np.sum(clusters_3d["energy"]))
            else:
                variables["3d_cluster_maxenergy"].append(float(0))
                variables["3d_cluster_sumenergy"].append(float(0))

        for key,arr in variables.items():
            variables[key] = np.array(arr)

        variables_by_filename[filename] = variables

        # print(variables)

    os.system(f"mkdir -p output/")
    with open(f"output/{arg.output}.pkl", "wb") as pickle_file:
        pickle.dump(variables_by_filename, pickle_file)
        pickle.dump(variables_by_filename, pickle_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(f'ldmx python3 {sys.argv[0]}')
    parser.add_argument('input_files', nargs='+')
    parser.add_argument('--output',required=True,help='Output name of pickle file (without extension)')
    parser.add_argument('--max_events',default=-1,type=int)
    arg = parser.parse_args()

    main(arg)
