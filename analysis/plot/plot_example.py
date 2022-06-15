import pickle
import argparse
import sys
import hist

"""
Example plotting script from pickled files.
Should be run in an environment (or jup notebook) with boost histogram
https://boost-histogram.readthedocs.io/en/latest/notebooks/aghast.html
"""

# this example uses ngun_0.10.pkl and ngun_0.30.pkl as input files

parser = argparse.ArgumentParser(f'python3 {sys.argv[0]}')
parser.add_argument('input_files',nargs='+')
arg = parser.parse_args()

# get input files from arguments
input_files = arg.input_files

# load a dictionary of these files with the arrays within each file
variables_by_files = {}
for filename in input_files:
    # load each input pickle file
    with open(filename,"rb") as pickle_file:
        variables_by_files[filename] = pickle.load(pickle_file)

# print dictionary (for debugging)
#print(variables)

# declare some axis that we are interested in plotting
# a regular axis will have
#  (number_of_bins, start_range, stop_range, name_of_axis, label_of_axis)
hcalenergy_axis = hist.axis.Regular(100, 0, 5, name='hcalEnergy', label=r'Energy [MeV]')
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
for filename,variables in variables_by_files.items():
    # we can extract the gun Energy from the filename string
    energy_str = filename.split('_')[-1]

    # to fill the hist_hcalsum histogram we need to fill each axis
    # the order in which we fill does not matter as long as we specify the axis name
    hist_hcal_1.fill(
        hcalEnergy = variables["hcalrechit_energy"],
        gunEnergy = energy_str,
    )

# we can print the histogram
print(hist_hcal_1)

# and select on the axis that we care about
