import pickle

with open("../output/example_1.pkl","rb") as pickle_file:
    variables = pickle.load(pickle_file)

print(variables.keys())

import hist
axis_1 = hist.axis.Regular(10, 0, 200, name='sumenergy', label='Sum Energy [MeV]')
hist_1 = hist.Hist(axis_1)

hist_1.fill(
    sumenergy=variables["sumenergy"]
)

import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 32})

fig, axs = plt.subplots(1, 1, figsize=(8, 8))
hep.histplot(
    hist_1,ax=axs,
    density=False,
    label='Temp'
)

import os
os.system('mkdir -p plots/')
fig.savefig('plots/example_1.png')
