#!/usr/bin/env python3
import ROOT, argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("input", help="Input ROOT file path")
parser.add_argument("-o", "--output", default='ntuple.root', help="Output file path")
parser.add_argument("--check", action='store_true', default=False, help="Run checks")
args = parser.parse_args()
if args.check: print('running checks')

isH5 = args.output.endswith('.h5') or args.output.endswith('.hdf5')

df = ROOT.RDataFrame("LDMX_Events", args.input)

#
# load the column names, and select a few to save
columnNames = list(map(str,df.GetColumnNames()))
processTag = columnNames[0].split('_')[-1] # can infer from the first collection
columnSelector = lambda n: n.startswith('PF') and n.endswith('_')
selectedNames = list(filter(columnSelector, columnNames))
# for x in list(set([n.split('_')[0] for n in columnNames])): print(x)

#
# Cleanup the names from ROOT classes
def makeName(oldName):
    ''' e.g. "PFTracks_test.z_" to "PFTracks_z" '''
    return (oldName[:-1]).replace(processTag+'.','')

remap = {n:makeName(n) for n in selectedNames}
columnsToWrite = list(remap.values())

# a few (unused) columns are filled in a way that causes problems
badColumns = ['PFEcalClusters_hitIDs','PFHcalClusters_hitIDs']
for c in columnsToWrite:
    if c in badColumns: columnsToWrite.remove(c)
collectionsToWrite = list(set([n.split('_')[0] for n in columnsToWrite]))
columnsByCollection = { collName : [c for c in columnsToWrite if c.split('_')[0]==collName] for collName in collectionsToWrite }
oldColumnsByCollection = { collName : [c for c in selectedNames if c.split('_')[0]==collName] for collName in collectionsToWrite }

# rename the old columns
for oldName in selectedNames:
    if isH5:
        df = df.Define(remap[oldName], oldName+'[0]')
    else:
        df = df.Define(remap[oldName], oldName)
    # df = df.Define(remap[oldName], oldName+'[0]')

# ... and define some new ones
#df = df.Define('Truth_pdgId','')

    
# write
if args.output.endswith('.root'):
    df.Snapshot('Events', args.output, columnsToWrite)
elif args.output.endswith('.h5') or args.output.endswith('.hdf5'):
    # exit('h5 not supported for ragged arrays')
    import h5py
    import numpy as np
    f = h5py.File(args.output, 'w')
    arrs = df.AsNumpy( filter(lambda n: n.startswith('PFCandidate'),columnsToWrite) )
    for n in arrs:
        f[n] = np.array(arrs[n], dtype=np.float32)
    f.close()
    
    # can also check the h5 dataset
    if args.check:
        print('Checking the created dataset')
        import numpy as np
        hf = h5py.File(args.output, 'r')
        for k in hf.keys():
            print( k, np.array(hf[k]) )
        hf.close()

# This is one way to find bad columns
# for cn in columnsToWrite:
#     print (cn)
#     a = df.AsNumpy([cn])
#     print(a)

