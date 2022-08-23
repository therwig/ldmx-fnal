from LDMX.Framework import ldmxcfg
p=ldmxcfg.Process("neutron")
p.libraries.append("libSimCore.so")
p.libraries.append("libHcal.so")
p.libraries.append("libEcal.so")

import argparse, sys, math
parser = argparse.ArgumentParser(f'ldmx fire {sys.argv[0]}')
parser.add_argument('energy',type=float)
arg = parser.parse_args()

nevents = 1000 # number of events
in_energy = arg.energy
energy = in_energy * 1000

from LDMX.SimCore import simulator
from LDMX.SimCore import generators
sim = simulator.simulator("neutrons")
sim.setDetector( 'ldmx-det-v12' , True )
sim.runNumber = 0
sim.description = "HCal neutron"
sim.beamSpotSmear = [20., 80., 0.] #mm
particle_gun = generators.multi( "two_neutron_upstream_hcal")
particle_gun.pdgID = 2112
# position = 870.
position = 690.6 # back hcal
# position = 240.4 # ecal face
neutrons = 2
particle_gun.nParticles = neutrons # number of neutrons
particle_gun.vertex = [ 0., 0., position ]  # mm
particle_gun.enablePoisson = False
#pz = math.sqrt((energy*1000.)**2-(939.565**2))
#print('pz ',pz,' energy ',energy)
particle_gun.momentum = [ 0., 0., energy] # MeV
print(particle_gun)
sim.generators.append(particle_gun)

p.outputFiles=['data/%ingun_%.2fmm_%.2f_gev.root'%(neutrons,position,in_energy)]
p.maxEvents = nevents
p.logFrequency = 100

p.sequence=[sim]

import LDMX.Ecal.digi as ecal_digi
import LDMX.Hcal.digi as hcal_digi

from LDMX.Ecal import EcalGeometry
geom = EcalGeometry.EcalGeometryProvider.getInstance()

from LDMX.Hcal import HcalGeometry
geom = HcalGeometry.HcalGeometryProvider.getInstance()

import LDMX.Hcal.hcal_hardcoded_conditions
digit = hcal_digi.HcalDigiProducer()
recon = hcal_digi.HcalRecProducer()

import LDMX.Ecal.ecal_hardcoded_conditions
p.sequence.extend([
    ecal_digi.EcalDigiProducer(),
    ecal_digi.EcalRecProducer(),
    digit,recon
])

