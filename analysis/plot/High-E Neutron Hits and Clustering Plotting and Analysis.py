import numpy as np
import pickle
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import matplotlib.ticker as ticker
import mplhep as hep
import hist
import os
import scipy.optimize as opt
from astropy.modeling import models, fitting

"""
This code is used to generate all kinds of plots based around rechits in the Hcal and clusters in the Hcal.
A lot is commented out as this code can be retooled to do a lot of things.
It is probably not written very well. I apologize for that.
"""

# all of these are for loading in differenet types of files
with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/1.00-3.00_GeV_Clusters_1_Plus.pkl", "rb")\
        as pickle_file:
    variables = pickle.load(pickle_file)  # defines the dictionary as a shorter variable
path_surname = "_gev_cluster.root"  # defines second part of path name after energy value
with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/1.00-3.00_GeV_Clusters_11_Plus.pkl", "rb")\
        as pickle_file:
    variables_2 = pickle.load(pickle_file)  # defines the dictionary as a shorter variable
path_surname_2 = "_gev_cluster_11.root"  # defines second part of path name after energy value
with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/1.00-3.00_GeV_Clusters_5_Plus.pkl", "rb")\
        as pickle_file:
    variables_3 = pickle.load(pickle_file)  # defines the dictionary as a shorter variable
path_surname_3 = "_gev_cluster_5.root"  # defines second part of path name after energy value
with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/1.00-3.00_GeV_Clusters_10_Plus.pkl", "rb")\
        as pickle_file:
    variables_4 = pickle.load(pickle_file)  # defines the dictionary as a shorter variable
path_surname_4 = "_gev_cluster_10.root"  # defines second part of path name after energy value
with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/1.00-3.00_GeV_Clusters_7_Plus.pkl", "rb")\
        as pickle_file:
    variables_5 = pickle.load(pickle_file)  # defines the dictionary as a shorter variable
path_surname_5 = "_gev_cluster_7.root"  # defines second part of path name after energy value


with open("C:/Users/Jonathan/Documents/Fermilab/LDMX/Data/24_sim_events.pkl", "rb") as test_file:
    test = pickle.load(test_file)

print(variables.keys())  # this is done just to see the energies available. If you know them, this can be commented
print(variables["data/ngun_690.60mm_1.00_gev_cluster.root"].keys())
# this prints the keys you may want to access
path_first_name = "data/ngun_690.60mm_"  # defines first part of path name

sim_var_pos = "hcalsimhit_Position"  # simhit variable for position
sim_var_edep = "hcalsimhit_Edep"  # sihit variable for energy deposited

sim_x_ax_2d = "x [mm]"  # sets 2d x-axis label
sim_y_ax_2d = "y [mm]"  # sets 2d y-axis label

var_hist = "3d_cluster_energy"  # sets 1d histogram variable

var_x_2d = "3d_cluster_energy"  # sets 2d x-axis variable
var_y_2d = "3d_cluster_layer"  # sets 3d y-axis variable
var_layer = "hcalrechit_layer"  # short form of rechit layer variable

var_x_3d = "hcalrechit_z"  # sets 3d x-axis variable
var_y_3d = "hcalrechit_x"  # sets 3d y-axis variable
var_z_3d = "hcalrechit_y"  # sets 3d z-axis variable
var_weight = "hcalrechit_energy"  # defines variable to weight by
var_cut = "hcalrechit_section"  # used to cut out events that didn't happen in back hcal
var_test = "event_nhcalrechit"  # sets a test variable for debugging or analysis

x_ax = "Cluster Energy [MeV]"  # x axis label for 1D hist
y_ax = "3D-Clusters (Normalized)"  # y-axis label for 1D hist

x_ax_2d = ""  # sets 2d x-axis label
y_ax_2d = ""  # sets 2d y-axis label

x_ax_3d = "z [mm]"  # sets 3d x-axis label
y_ax_3d = "x [mm]"  # sets 3d y-axis label
z_ax_3d = "y [mm]"  # sets 3d z-axis label

e_1 = "1.00"  # input the energies you want here
e_2 = "1.50"  # make sure each energy follows the necessary format
e_3 = "2.00"  # no need for a space before or after
e_4 = "2.50"  # examples: "0.05", "0.70", "1.50"
e_5 = "3.00"
e_6 = "3.50"
e_7 = "4.00"


def get_path(variable, energy, file=""):  # gets path given the variable name and energy
    if file == "":
        data_array = variables[path_first_name + energy + path_surname][variable]
        data_array[np.isnan(data_array)] = -2000
        return data_array
    if file == "2":
        data_array = variables_2[path_first_name + energy + path_surname_2][variable]
        data_array[np.isnan(data_array)] = -2000
        return data_array
    if file == "3":
        data_array = variables_3[path_first_name + energy + path_surname_3][variable]
        data_array[np.isnan(data_array)] = -2000
        return data_array
    if file == "4":
        data_array = variables_4[path_first_name + energy + path_surname_4][variable]
        data_array[np.isnan(data_array)] = -2000
        return data_array
    if file == "5":
        data_array = variables_5[path_first_name + energy + path_surname_5][variable]
        data_array[np.isnan(data_array)] = -2000
        return data_array


def sim_path(variable, energy):  # gets path for simhits
    raw_data_array = variables[path_first_name + energy + path_surname][variable]
    clean_arr = raw_data_array[np.isnan(raw_data_array)] = 0
    return test[path_first_name + energy + path_surname][variable]


# print(get_path(var_hist, e_1))
data_max = np.amax(get_path(var_hist, e_5))  # maximum of the highest energy data. Used to give upper bound
data_min = np.amin(get_path(var_hist, e_1))  # minimum of the lowest energy data. Used to give lower bound
data_ext = data_max + 0.10 * data_max
# used to give the graph some extra space to show where data stops and fit legend


def get_bin(x, y):  # handles binning data automatically
    if 100 < x - y:  # if range of data is more than 30...
        bin_number = 50
        return bin_number  # have 50 bins
    if 0 < x - y <= 100:  # if range of data is greater than zero and less than or equal to 30...
        bin_number = int(x - y)  # have bins equal to the range of the data. (probably breaks if data is non-integer)
        return bin_number
    if x - y == 0:  # if range of data is 0...
        bin_number = 1  # have one bin
        return bin_number


bin_num = get_bin(data_max, data_min)  # this sets bins according to the function


def get_sim_pos(axis, energy):  # used with simhit position variable
    if axis == "x":
        x_values = []
        for i in range(len(test[path_first_name + energy + path_surname][sim_var_pos])):
            x_values = np.append(x_values, test[path_first_name + energy + path_surname][sim_var_pos][i][0])
        return x_values
    if axis == "y":
        y_values = []
        for i in range(len(test[path_first_name + energy + path_surname][sim_var_pos])):
            y_values = np.append(y_values, test[path_first_name + energy + path_surname][sim_var_pos][i][1])
        return y_values
    if axis == "z":
        z_values = []
        for i in range(len(test[path_first_name + energy + path_surname][sim_var_pos])):
            z_values = np.append(z_values, test[path_first_name + energy + path_surname][sim_var_pos][i][1])
        return z_values


def get_back(variable, energy):  # gets only events in the back hcal, but could be adapted to cut based on other params
    where_to_cut = np.where(get_path(var_cut, energy) != 0)  # must be given the variable you want to cut and energy
    return np.delete(get_path(variable, energy), where_to_cut)


def cut_en(variable, energy):  # defines a cut on 3d cluster energy
    where_to_cut = np.where(get_path("3d_cluster_energy", energy) < 10)
    return np.delete(get_path(variable, energy), where_to_cut)


def ratio_hist(energy):  # sets a max energy cluster / sum of energy clustered histogram
    axis = hist.axis.Regular(50, 0, 100, name='axis')
    histogram = hist.Hist(axis)
    max_e = get_path("3d_cluster_maxenergy", energy, "")
    sum_e = get_path("3d_cluster_sumenergy", energy, "")
    data = 100 * max_e/sum_e
    data[np.isnan(data)] = 0
    histogram.fill(axis=data)
    return hep.histplot(histogram, ax=ax, density=False, label=energy + " GeV")


def set_hist(energy, back="", file=""):  # sets an unweighted histogram based on the energy variable entered
    axis = hist.axis.Regular(bin_num, data_min, data_max, name='axis')
    histogram = hist.Hist(axis)
    if back == "":
        data = get_path(var_hist, energy, file)
    if back == "back":
        data = get_back(var_hist, energy, file)
    histogram.fill(axis=data)
    return hep.histplot(histogram, ax=ax, density=False, label=energy + " GeV")


def mask_hist(energy, mask, file=""):  # sets an unweighted histogram of 3d cluster energies with a certain mask
    axis = hist.axis.Regular(bin_num, data_min, data_max, name='axis')
    histogram = hist.Hist(axis)
    data = get_path("3d_cluster_energy", energy, file)
    data_mask = np.delete(data, np.where(data < mask))
    histogram.fill(axis=data_mask)
    final_hist = hep.histplot(histogram, ax=ax, density=True, label=energy + " GeV")
    return


def set_hist_weight(energy, weight, back=""):  # sets a weighted histogram based on the energy variable entered
    axis = hist.axis.Regular(bin_num, data_min, data_max, name='axis')
    histogram = hist.Hist(axis)
    if back == "":
        data = get_path(var_hist, energy)
        weight_data = get_path(weight, energy)
    if back == "back":
        data = get_back(var_hist, energy)
        weight_data = get_back(weight, energy)
    histogram.fill(axis=data, weight=weight_data)
    return hep.histplot(histogram, ax=ax, density=False, label=energy + " GeV")


def get_extrema(extrema, variable, energy, back=""):  # used for getting different maxima/minima. Used in 2d hists
    if back == "":
        data_range = np.amax(get_path(variable, energy)) - np.amin(get_path(variable, energy))
        if extrema == "max":
            return np.amax(get_path(variable, energy)) + 0.10 * data_range
        if extrema == "min":
            return np.amin(get_path(variable, energy)) - 0.10 * data_range
    if back == "back":
        data_range = np.amax(get_back(variable, energy)) - np.amin(get_back(variable, energy))
        if extrema == "max":
            return np.amax(get_back(variable, energy)) + 0.10 * data_range
        if extrema == "min":
            return np.amin(get_back(variable, energy)) - 0.10 * data_range
    if back == "cut":
        data_range = np.amax(cut_en(variable, energy)) - np.amin(cut_en(variable, energy))
        if extrema == "max":
            return np.amax(cut_en(variable, energy)) + 0.10 * data_range
        if extrema == "min":
            return np.amin(cut_en(variable, energy)) - 0.10 * data_range


def back_center(variable, energy):
    maximum = np.amax(get_back(variable, energy))
    minimum = np.amin(get_back(variable, energy))
    data_range = maximum - minimum
    if np.abs(maximum) >= np.abs(minimum):
        return np.abs(maximum) + 0.10 * np.abs(data_range)
    if np.abs(maximum) < np.abs(minimum):
        return np.abs(minimum) + 0.10 * np.abs(data_range)


def sim_center(variable, energy):  # used for setting axes limits of simhit plots
    maximum = np.amax(get_sim_pos(variable, energy))
    minimum = np.amin(get_sim_pos(variable, energy))
    data_range = maximum - minimum
    if np.abs(maximum) >= np.abs(minimum):
        return np.abs(maximum) + 0.10 * np.abs(data_range)
    if np.abs(maximum) < np.abs(minimum):
        return np.abs(minimum) + 0.10 * np.abs(data_range)


plt.style.use(hep.style.CMS)  # style of hist definition, always leave this in. It's typeface stuff
plt.rcParams.update({'font.size': 24})  # setting font size for the hist

fig, ax = plt.subplots(1, 1, figsize=(8, 8))  # can change subplot values for more plots. 8, 8 fig size is good
plt.subplots_adjust(wspace=0.8)  # separates the graphs in subplots
# leave in for 1D and 2D, take out for 3D

# 1d histogram plotting stuff
# set_hist(e_1, file="2")  # uses function above to set histogram for each energy
# set_hist(e_2)
# set_hist(e_3, file="2")
# set_hist(e_4)
# set_hist(e_5, file="2")
# set_hist(e_6)
# set_hist(e_7)

# mask_hist(e_1, 20)
# mask_hist(e_3, 20)
# mask_hist(e_5, 20)

# ratio_hist(e_1)
# ratio_hist(e_3)
# ratio_hist(e_5)

hep.cms.lumitext(f"Version 2.1 Energy Resolution", ax=ax, **{"fontsize": 26})  # Title text
hep.cms.text(text="", loc=0, ax=ax, **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True)})
ax.set_ylabel(y_ax)  # this takes axes names from above. I could have just defined these manually
ax.set_xlabel(x_ax)  # But it is easier to keep all manually variable items in the same place at the top
ax.legend(title="Neutron Energy", fontsize=24)  # legend definition
fig.tight_layout()  # necessary to keep the text at the bottom of the graph from being cut off!!!!
# os.system('mkdir -p plots/')  # This defines where to save the graphs. I don't use this
# fig.savefig('example_1.png')  # Saves the plot. I also do not use this. I save my plots manually
plt.show()

# def get_max_layer(energy):


def sim_2d_hist(x_variable, y_variable, energy, weight, title): # used for a 2d hist of simhits
    ax2_1 = hist.axis.Regular(120, - sim_center(x_variable, energy), sim_center(x_variable, energy), name='ax2_1')
    ax2_2 = hist.axis.Regular(120, - sim_center(y_variable, energy), sim_center(y_variable, energy), name='ax2_2')
    h_2d = hist.Hist(ax2_1, ax2_2)
    if weight == 1:
        h_2d.fill(ax2_1=get_sim_pos(x_variable, energy), ax2_2=get_sim_pos(y_variable, energy))
    else:
        h_2d.fill(ax2_1=get_sim_pos(x_variable, energy), ax2_2=get_sim_pos(y_variable, energy),
                  weight=sim_path(weight, energy))
    ax.set_xlabel(sim_x_ax_2d)  # this takes axes names from above
    ax.set_ylabel(sim_y_ax_2d)
    hep.cms.lumitext(title, ax=ax, **{"fontsize": 18})  # Title text
    hep.cms.text(text="", loc=0, ax=ax, **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True)})
    fig.tight_layout()  # necessary to keep the text at the bottom of the graph from being cut off!!!!
    return hep.hist2dplot(h_2d, ax=ax, cmap="plasma", norm=mpl.colors.LogNorm(vmin=1e-3, vmax=1000))


def set_2d_hist(x_variable, y_variable, energy, weight, title, back="", strip=""): # sets all kinds of 2d rechit hists
    if back == "":
        if strip == "":
            ax2_1 = hist.axis.Regular(30, get_extrema("min", x_variable, energy, back=""),
                                      get_extrema("max", x_variable, energy, back=""), name='ax2_1')
            ax2_2 = hist.axis.Regular(30, get_extrema("min", y_variable, energy, back=""),
                                      get_extrema("max", y_variable, energy, back=""), name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                h_2d.fill(ax2_1=get_path(x_variable, energy), ax2_2=get_path(y_variable, energy))
            else:
                h_2d.fill(ax2_1=get_path(x_variable, energy), ax2_2=get_path(y_variable, energy),
                          weight=get_path(weight, energy))
            ax.set_xlabel(x_ax_2d)  # this takes axes names from above
            ax.set_ylabel(y_ax_2d)
        if strip == "horizontal":
            horizontal_arr = []
            for i in range(0, len(get_path(var_layer, energy))):
                orientation = get_path(var_layer, energy)[i] % 2
                if orientation == 0:
                    horizontal_arr.append(i)
            ax2_1 = hist.axis.Regular(1, -1825, 1825, name='ax2_1')
            ax2_2 = hist.axis.Regular(62, 0, 62, name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                for n in horizontal_arr:
                    h_2d.fill(ax2_1=get_path("hcalrechit_x", energy)[n], ax2_2=get_path("hcalrechit_strip", energy)[n])
            else:
                for n in horizontal_arr:
                    h_2d.fill(ax2_1=get_path("hcalrechit_x", energy)[n], ax2_2=get_path("hcalrechit_strip", energy)[n],
                              weight=get_path(weight, energy)[n])
            ax.set_xlabel("x [mm]")  # this takes axes names from above
            ax.set_ylabel("Strip")
        if strip == "vertical":
            vertical_arr = []
            for i in range(0, len(get_path(var_layer, energy))):
                orientation = get_path(var_layer, energy)[i] % 2
                if orientation == 1:
                    vertical_arr.append(i)
            ax2_1 = hist.axis.Regular(62, 0, 62, name='ax2_1')
            ax2_2 = hist.axis.Regular(1, -1825, 1825, name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                for n in vertical_arr:
                    h_2d.fill(ax2_1=get_path("hcalrechit_strip", energy)[n], ax2_2=get_path("hcalrechit_y", energy)[n])
            else:
                for n in vertical_arr:
                    h_2d.fill(ax2_1=get_path("hcalrechit_strip", energy)[n], ax2_2=get_path("hcalrechit_y", energy)[n],
                              weight=get_path(weight, energy)[n])
            ax.set_xlabel("Strip")  # this takes axes names from above
            ax.set_ylabel("y [mm]")
        if strip == "max":
            max_layer = int(get_path("event_hcalrechit_maxpe_layer", energy)) + 1
            max_layer_ind_arr = np.where(
                 get_path("hcalrechit_layer", energy) == max_layer)
            orientation = max_layer % 2
            if orientation == 0:
                ax2_1 = hist.axis.Regular(1, -1825, 1825, name='ax2_1')
                ax2_2 = hist.axis.Regular(62, 0, 62, name='ax2_2')
                h_2d = hist.Hist(ax2_1, ax2_2)
                if weight == 1:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_path("hcalrechit_x", energy)[n],
                                  ax2_2=get_path("hcalrechit_strip", energy)[n])
                else:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_path("hcalrechit_x", energy)[n],
                                  ax2_2=get_path("hcalrechit_strip", energy)[n],
                                  weight=get_path(weight, energy)[n])
                ax.set_xlabel("x [mm]")  # this takes axes names from above
                ax.set_ylabel("Strip")
            if orientation == 1:
                ax2_1 = hist.axis.Regular(62, 0, 62, name='ax2_1')
                ax2_2 = hist.axis.Regular(1, -1825, 1825, name='ax2_2')
                h_2d = hist.Hist(ax2_1, ax2_2)
                if weight == 1:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_path("hcalrechit_strip", energy)[n],
                                  ax2_2=get_path("hcalrechit_y", energy)[n])
                else:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_path("hcalrechit_strip", energy)[n],
                                  ax2_2=get_path("hcalrechit_y", energy)[n],
                                  weight=get_path(weight, energy)[n])
                ax.set_xlabel("Strip")  # this takes axes names from above
                ax.set_ylabel("y [mm]")
    if back == "back":
        if strip == "":
            ax2_1 = hist.axis.Regular(30, get_extrema("min", x_variable, energy, back),
                                      get_extrema("max", x_variable, energy, back), name='ax2_1')
            ax2_2 = hist.axis.Regular(30, get_extrema("min", y_variable, energy, back),
                                      get_extrema("max", y_variable, energy, back), name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                h_2d.fill(ax2_1=get_back(x_variable, energy), ax2_2=get_back(y_variable, energy))
            else:
                h_2d.fill(ax2_1=get_back(x_variable, energy), ax2_2=get_back(y_variable, energy),
                          weight=get_back(weight, energy))
            ax.set_xlabel(x_ax_2d)  # this takes axes names from above
            ax.set_ylabel(y_ax_2d)
        if strip == "horizontal":
            horizontal_arr = []
            for i in range(0, len(get_back(var_layer, energy))):
                orientation = get_back(var_layer, energy)[i] % 2
                if orientation == 0:
                    horizontal_arr.append(i)
            ax2_1 = hist.axis.Regular(1, -1825, 1825, name='ax2_1')
            ax2_2 = hist.axis.Regular(62, 0, 62, name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                for n in horizontal_arr:
                    h_2d.fill(ax2_1=get_back("hcalrechit_x", energy)[n], ax2_2=get_back("hcalrechit_strip", energy)[n])
            else:
                for n in horizontal_arr:
                    h_2d.fill(ax2_1=get_back("hcalrechit_x", energy)[n], ax2_2=get_back("hcalrechit_strip", energy)[n],
                              weight=get_back(weight, energy)[n])
            ax.set_xlabel("x [mm]")  # this takes axes names from above
            ax.set_ylabel("Strip")
        if strip == "vertical":
            vertical_arr = []
            for i in range(0, len(get_back(var_layer, energy))):
                orientation = get_back(var_layer, energy)[i] % 2
                if orientation == 1:
                    vertical_arr.append(i)
            ax2_1 = hist.axis.Regular(62, 0, 62, name='ax2_1')
            ax2_2 = hist.axis.Regular(1, -1825, 1825, name='ax2_2')
            h_2d = hist.Hist(ax2_1, ax2_2)
            if weight == 1:
                for n in vertical_arr:
                    h_2d.fill(ax2_1=get_back("hcalrechit_strip", energy)[n], ax2_2=get_back("hcalrechit_y", energy)[n])
            else:
                for n in vertical_arr:
                    h_2d.fill(ax2_1=get_back("hcalrechit_strip", energy)[n], ax2_2=get_back("hcalrechit_y", energy)[n],
                              weight=get_back(weight, energy)[n])
            ax.set_xlabel("Strip")  # this takes axes names from above
            ax.set_ylabel("y [mm]")
        if strip == "max":
            max_layer = int(get_path("event_hcalrechit_maxpe_layer", energy)) + 1
            max_layer_ind_arr = np.where(
                get_path("hcalrechit_layer", energy) == max_layer)
            orientation = max_layer % 2
            if orientation == 0:
                ax2_1 = hist.axis.Regular(1, -1825, 1825, name='ax2_1')
                ax2_2 = hist.axis.Regular(62, 0, 62, name='ax2_2')
                h_2d = hist.Hist(ax2_1, ax2_2)
                if weight == 1:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_back("hcalrechit_x", energy)[n],
                                  ax2_2=get_back("hcalrechit_strip", energy)[n])
                else:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_back("hcalrechit_x", energy)[n],
                                  ax2_2=get_back("hcalrechit_strip", energy)[n],
                                  weight=get_back(weight, energy)[n])
                ax.set_xlabel("x [mm]")  # this takes axes names from above
                ax.set_ylabel("Strip")
            if orientation == 1:
                ax2_1 = hist.axis.Regular(62, 0, 62, name='ax2_1')
                ax2_2 = hist.axis.Regular(1, -1825, 1825, name='ax2_2')
                h_2d = hist.Hist(ax2_1, ax2_2)
                if weight == 1:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_back("hcalrechit_strip", energy)[n],
                                  ax2_2=get_back("hcalrechit_y", energy)[n])
                else:
                    for n in max_layer_ind_arr:
                        h_2d.fill(ax2_1=get_back("hcalrechit_strip", energy)[n],
                                  ax2_2=get_back("hcalrechit_y", energy)[n],
                                  weight=get_back(weight, energy)[n])
                ax.set_xlabel("Strip")  # this takes axes names from above
                ax.set_ylabel("y [mm]")
    hep.cms.lumitext(title, ax=ax, **{"fontsize": 26})  # Title text
    hep.cms.text(text="", loc=0, ax=ax, **{"exp": "LDMX", "exp_weight": "bold", "fontsize": 23, "italic": (True, True)})
    fig.tight_layout()  # necessary to keep the text at the bottom of the graph from being cut off!!!!
    return hep.hist2dplot(h_2d, ax=ax, cmap="plasma", norm=mpl.colors.LogNorm(vmin=1e-3, vmax=1000), edgecolor='k')


# 2d graphing stuff
rec_e = e_5  # used for rechit energy in 2d hist
# set_2d_hist(var_x_2d, var_y_2d, rec_e, 1, rec_e + " GeV Single Event Strips", back="back",
#             strip="horizontal")  # only the first couple variables are mandatory, the latter are all for defining
# things further for different types of 2d hists.
# 2d histogram for rechits. Super complex function, but it works
# sim_e = e_7  # used for simhit energy in 2d hist right below
# sim_2d_hist("x", "y", sim_e, 1, sim_e + " GeV Sim Hits")  # simhit 2d hist function
# plt.show()


def cut_3d(variable, energy, minimum, maximum, cluster=""):  # sets 3d plot with a limit on axes
    x_array = []
    if cluster == "":
        x_array = np.append(x_array, np.where(get_back(var_y_3d, energy) < minimum))
        x_array = np.append(x_array, np.where(get_back(var_y_3d, energy) > maximum))
    if cluster == "True":
        x_array = np.append(x_array, np.where(get_path(var_y_3d, energy) < minimum))
        x_array = np.append(x_array, np.where(get_path(var_y_3d, energy) > maximum))
    y_array = []
    if cluster == "":
        y_array = np.append(y_array, np.where(get_back(var_z_3d, energy) < minimum))
        y_array = np.append(y_array, np.where(get_back(var_z_3d, energy) > maximum))
    if cluster == "True":
        y_array = np.append(y_array, np.where(get_path(var_z_3d, energy) < minimum))
        y_array = np.append(y_array, np.where(get_path(var_z_3d, energy) > maximum))
    cut_array = np.array(np.intersect1d(x_array, y_array, return_indices=True))[2]
    cut_array = cut_array.astype(int)
    add_array = np.delete(y_array, cut_array)
    final_array = np.append(x_array, add_array)
    final_array = final_array.astype(int)
    if cluster == "":
        out_array = np.delete(get_back(variable, energy), final_array)
    if cluster == "True":
        out_array = np.delete(get_path(variable, energy), final_array)
    return out_array


# 3d graphing stuff
"""
en_3d = e_1
graph_min = -500
graph_max = 500
# print(cut_3d(var_y, var_3d, -200, 200))
fig = plt.figure(figsize=(10, 10))  # creates new figure
ax = fig.add_subplot(projection='3d')  # sets the plot as 3d
ax.set_facecolor("white")
weight = cut_3d(var_weight, en_3d, graph_min, graph_max, cluster="True")  # Weights size and color of each point
data_x_ax = cut_3d(var_x_3d, en_3d, graph_min, graph_max, cluster="True")  # x-axis is on the x-axis
data_y_ax = cut_3d(var_y_3d, en_3d, graph_min, graph_max, cluster="True")  # y-axis
data_z_ax = cut_3d(var_z_3d, en_3d, graph_min, graph_max, cluster="True")  # z-axis
plot = ax.scatter(data_x_ax, data_y_ax, data_z_ax, s=5 + weight,  c=weight, marker="o")  # s=size and c=color
cbar = fig.colorbar(plot, ax=ax, location="right", pad=0.11)
cbar.set_label("Energy [MeV]                  ", loc="center")
ax.set_title("$\mathbf{LDMX}$ " + en_3d + " GeV Hit Locations", fontsize=25,
             style="italic", weight="bold")
# title
ax.set_xlim(5500, 0)
ax.set_ylim(graph_min, graph_max)
ax.set_zlim(graph_min, graph_max)
ax.set_xlabel("\n" + x_ax_3d, linespacing=2.2)  # sets each axis label as defined at the top
ax.set_ylabel("\n" + y_ax_3d, linespacing=2.2)  # \n adds a new line so the labels don't overlap with ticks
ax.set_zlabel("\n" + z_ax_3d, linespacing=2.2)  # linespacing adjusts distance of text to axis
# plt.show()
# print(np.amin(get_back(var_y, var_3d)))
"""


Seed_Energy_Threshold = [0.10, 0.50, 0.60, 1.0]  # seed energy array
Neighboring_Energy_Threshold = [0.01, 0.50, 1.00, 1.50, 2.00]  # neighboring energy array
Neighboring_Strips = [4, 6, 8, 10]  # neighboring strip array


def e_rec_plot(energy_arr, file_arr, x_arr, dimension=""):  # reconstructed energy plot
    local_en_path = "_cluster_energy"
    local_var = dimension + local_en_path
    energy_name = 0
    for i in energy_arr:
        # n = 0
        y_ax_arr = []
        # x_ax_arr = []
        for f in file_arr:
            if f == 1:
                file_name = ""
            else:
                file_name = str(f)
            cluster_energy_arr = get_path(local_var, i, file_name)
            for x in cluster_energy_arr:
                squared_arr = []
                x_squared = x ** 2
                squared_arr = np.append(squared_arr, x_squared)
            n_of_entries = len(cluster_energy_arr)
            mean_square_arr = squared_arr / n_of_entries
            rms = mean_square_arr ** 0.5
            mean_en = np.mean(cluster_energy_arr)
            resolution = float(rms) / mean_en
            y_ax_arr = np.append(y_ax_arr, resolution)
            # x_ax_arr = np.append(x_ax_arr, float(x_arr[n]))
            # n = n + 1
        # print(x_ax_arr)
        # print(y_ax_arr)
        ax.scatter(x_arr, y_ax_arr, label=str(energy_arr[energy_name]) + " GeV", lw=3)
        energy_name = energy_name + 1
    if dimension == "2d":
        title = "2D"
    if dimension == "3d":
        title = "3D"
    ax.set_title("LDMX " + title + "-Clusters, Varying Seed-Energy Threshold",
                 fontsize=14, style="italic", weight="bold")


"""
energy_array = get_path("3d_cluster_energy", e_3, "2")
for i in energy_array:
    squared_arr = []
    i_squared = i**2
    squared_arr = np.append(squared_arr, i_squared)
n_of_entries = len(energy_array)
mean_square_arr = squared_arr/n_of_entries
rms = mean_square_arr ** 0.5
print(energy_array)
print(rms)


# e_rec_plot([e_1, e_3, e_5], [1, 2, 3, 4], Seed_Energy_Threshold, "3d")
# Okay, to use this, first you put in an array of the energies you want to look at
# Then, you put in an array of the corresponding files. This will probably be just of the form [1, 2, 3]
# Then, you put in what variable you're analyzing, neighbroing energy threshold, seed energy, etc.
# Finally, you tell it if you want 2d or 3d info

# ax.set_title("$\mathbf{LDMX}$ 2D Varying Strips", fontsize=25, style="italic", weight="bold")
ax.legend(title="Gun Energy", fontsize=23)
ax.set_ylabel("Energy Resolution [MeV]", fontsize=25)

# Seed Energy Settings
ax.set_xlabel("Seed Energy Threshold [MeV]", fontsize=25)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.20))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(0.01))
ax.set_xlim(0, 1.2)


# Neighboring Strip Settings
ax.set_xlabel("# of Neighboring Strips", fontsize=25)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.set_xlim(2, 12)


# Neighboring Energy Threshold Settings
ax.set_xlabel("Neighboring E-Threshold [MeV]", fontsize=25)
ax.xaxis.set_major_locator(ticker.MultipleLocator(0.50))
ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.set_xlim(-.20, 2.40)

# ax.set_ylim(0, 0.00025)
fig.tight_layout()
plt.show()
"""