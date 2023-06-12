import h5py, hist, os
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import mplhep as hep

plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 18})
os.system('mkdir -p plots/')

#
# load the data and populate a dictionary with numpy arrays
f = h5py.File('data/events.h5', 'r')
variables = { k : np.array(f[k]) for k in f.keys() }

#
# Fill a 1d histogram with particle energy
axis_1 = hist.axis.Regular(30, 0, 6000, name='energy', label='Energy [MeV]')
hist_1a = hist.Hist(axis_1)
hist_1a.fill( energy=variables["PFCandidates_energy"] )
hist_1b = hist.Hist(axis_1)
hist_1b.fill( energy=variables["PFCandidates_truthEnergy"] )

#
# Fill a 2d histogram with particle position (x,y)
axis_2x = hist.axis.Regular(40, -200, 200, name='x', label='Ecal x position [mm]')
axis_2y = hist.axis.Regular(40, -200, 200, name='y', label='Ecal y position [mm]')
hist_2 = hist.Hist(axis_2x, axis_2y)
hist_2.fill( x=variables["PFCandidates_ecalClusterX"], y=variables["PFCandidates_ecalClusterY"], )

#
# Draw the histograms
fig, axs = plt.subplots(1, 1, figsize=(8, 8))
hep.histplot(
    [hist_1a, hist_1b],
    label=['Reco','Truth'],
    ax=axs,
    density=False,
)
fig.legend()
fig.savefig('plots/example_1d.png')

fig, axs = plt.subplots(1, 1, figsize=(8, 8))
hep.hist2dplot(
    hist_2,ax=axs,
)
fig.savefig('plots/example_2d.png')


#
# Slightly more complicated example of a "profile" plot

recoE=variables["PFCandidates_ecalEnergy"]
truthE=variables["PFCandidates_truthEnergy"]
response = np.divide(recoE,truthE,out=np.zeros_like(truthE), where=truthE>0)

def profilePlot(x,y,saveName,xtitle='',ytitle='',lims=None, nbins=20, col='C0'):
    if not lims: lims = (x.min(),x.max())
    median_result = scipy.stats.binned_statistic(x, y, bins=nbins, range=lims, statistic=lambda x: np.quantile(x,0.5))
    lo_result     = scipy.stats.binned_statistic(x, y, bins=nbins, range=lims, statistic=lambda x: np.quantile(x,0.5-0.68/2))
    hi_result     = scipy.stats.binned_statistic(x, y, bins=nbins, range=lims, statistic=lambda x: np.quantile(x,0.5+0.68/2))
    mean_result   = scipy.stats.binned_statistic(x, y, bins=nbins, range=lims, statistic='mean')
    median = np.nan_to_num(median_result.statistic)
    mean = np.nan_to_num(mean_result.statistic)
    hi = np.nan_to_num(hi_result.statistic)
    lo = np.nan_to_num(lo_result.statistic)
    hie = hi-median
    loe = median-lo
    bin_edges = median_result.bin_edges
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2.
    fig, axs = plt.subplots(1, 1, figsize=(8, 8))
    plt.errorbar(x=bin_centers, y=median, yerr=[loe,hie], linestyle='none', marker='.',c=col)
    plt.plot(bin_centers, mean, linestyle='none', marker='x', c=col)
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)
    fig.savefig(saveName)
    
profilePlot(truthE, response, 'plots/example_profile.png',
            nbins=18, lims = (400,4e3),
            xtitle='Truth Energy [MeV]', ytitle='Ecal Cluster Energy / Truth Energy',)
