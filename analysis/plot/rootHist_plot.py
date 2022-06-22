import pickle
import argparse
import sys
import hist
import uproot3
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 32})

"""
Example plotting script from saved ROOT histograms.
"""

# So far, I have only tested this with a single input (root) file
parser = argparse.ArgumentParser(f'python3 {sys.argv[0]}')
parser.add_argument('input_files',nargs='+')
arg = parser.parse_args()

# get input files from arguments
input_files = arg.input_files

# load a dictionary of these files with the histograms within each file
rootHists_by_files = {}
hists_by_files = {}

for filename in input_files:
    # load each input root file with histograms
    hist_file = uproot3.open(filename)
    for key in hist_file:
        h = hist_file[key]
        name = key.decode("utf-8").split(';')[0]
        # for each histogram, convert it to the "Hist" format
        if 'TH1' in h.classname:
            contents, edges = hist_file[key].numpy()
            hh = hist.Hist(hist.axis.Variable(edges))
            hh.view()[:]=contents
            hists_by_files[(filename,name)] = hh
        elif 'TH2' in h.classname:
            contents, edges = hist_file[key].numpy()
            ax1 = hist.axis.Variable(edges[0][0])
            ax2 = hist.axis.Variable(edges[0][1])
            hh = hist.Hist(ax1, ax2)
            hh.view()[:] = contents
            hists_by_files[(filename,name)] = hh
        else:
            print('Skipping unsuported type:',h.classname)

# make some simple plots to test that we read the histograms OK
for fn in input_files:
    h1 = hists_by_files[(fn,'h1')]
    fig, axs = plt.subplots(1, 1, figsize=(8, 8))
    hep.histplot(
        h1, ax=axs,
        density=False,
        label='Temp',
    )
    fig.savefig('example_h1.png')
    
    h2 = hists_by_files[(fn,'h2')]
    fig, axs = plt.subplots(1, 1, figsize=(8, 8))
    hep.hist2dplot(
        h2, ax=axs,
    )
    fig.savefig('example_h2.png')

    hprof = h2.profile(1) # profile over the 1st axis
    fig, axs = plt.subplots(1, 1, figsize=(8, 8))
    hep.histplot(
        hprof, ax=axs,
        density=False,
        label='Temp',
    )
    fig.savefig('example_hprof.png')
