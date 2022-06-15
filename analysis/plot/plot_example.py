import pickle
import argparse
import sys
import hist

import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 32})

"""
Example plotting script from pickled files.
Should be run in an environment (or jup notebook) with boost histogram and mplhep
https://boost-histogram.readthedocs.io/en/latest/notebooks/aghast.html
"""

# this example uses neutronguns.pkl as input file

parser = argparse.ArgumentParser(f'python3 {sys.argv[0]}')
parser.add_argument('input_file')
arg = parser.parse_args()

# get input files from arguments
input_file = arg.input_file

# load each input pickle file
with open(input_file,"rb") as pickle_file:
    variables = pickle.load(pickle_file)

# print dictionary keys (for debugging)
print(variables.keys())

# declare some axis that we are interested in plotting
# a regular axis will have
#  (number_of_bins, start_range, stop_range, name_of_axis, label_of_axis)
hcalenergy_axis = hist.axis.Regular(100, 0, 14, name='hcalEnergy', label=r'Energy [MeV]')
hcalsumenergy_axis = hist.axis.Regular(25, 0, 1000, name='sumEnergy', label=r'Summed Energy [MeV]')

# a string axis will have
#  (list_of_strings, name_of_axis, growth)
#  if growth=True the list of strings can grow from the list originally specified
# declare gun energy string axis to tag each file
gunEnergy_axis = hist.axis.StrCategory([], name='gunEnergy', growth=True)

# based on the axis we have defined we can create histograms

# this histogram has the gunEnergy as a string axis and the hcalrechitenergy as a regular axis
hist_hcal_1 = hist.Hist(
    gunEnergy_axis,
    hcalenergy_axis
)

# the histograms can be filled using the `variables array`
for key,var_arrays in variables.items():
    # we can extract the gun Energy from the key
    energy_str = key
    print(energy_str)
    
    # to fill the hist_hcalsum histogram we need to fill each axis
    # the order in which we fill does not matter as long as we specify the axis name
    hist_hcal_1.fill(
        hcalEnergy = variables["hcalrechit_energy"],
        gunEnergy = energy_str,
    )

# we can print the histogram
print(hist_hcal_1)

# and select on the axis that we care about
#  we will select on 0.10

#  the syntax is: [{"name_of_axis": selection}]
#  where selection=string in a StrAxis
#    or  selection=[:] slice or bin number in a RegularAxis
h1 = hist_hcal_1[{"gunEnergy":"0.10"}]

# now we will have a 1d histogram
print(h1)

# and we can plot it in matplotlib
fig, axs = plt.subplots(1, 1, figsize=(8, 8))
# we can use histplot to plot a 1D histogram
#  https://mplhep.readthedocs.io/en/latest/api.html#mplhep.histplot
hep.histplot(
    h1, # histogram
    ax=axs,  # axis
    density=False, # whether to normalize the histogram to 1 or not
    label="0.10 GeV" # label of histogram
)
# set labels
axs.set_ylabel("Rec Hits")
axs.legend(title="Neutron Energy", fontsize=30)
hep.cms.text(text="", loc=0, ax=axs,
             **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True)})
fig.tight_layout()
fig.savefig("example_ngun_0.10.png")

# we can also plot both of the files in the same histogram

# we get the next histogram
h2 = hist_hcal_1[{"gunEnergy":"0.30"}]

fig, axs = plt.subplots(1, 1, figsize=(8, 8))
hep.histplot(h1,ax=axs,label="0.10 GeV")
hep.histplot(h2,ax=axs,label="0.30 GeV")
axs.set_ylabel("Rec Hits")
axs.legend(title="Neutron Energy", fontsize=30)
hep.cms.text(text="", loc=0, ax=axs,
             **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True)})
fig.tight_layout()
fig.savefig("example_nguns.png")
