# Analysis

Use `EventTree.py` to analyze LDMX Events.

## Getting started
- [Install the docker engine](https://docs.docker.com/engine/install/)
- (on Linux systems) [Manage docker as non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
- Clone the repo: `git clone --recursive git@github.com:LDMX-Software/ldmx-sw.git`
  - **Note**: You need to [setup an SSH-key with your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) on the computer you are using.
- Setup the environment (in bash): 
```
source ldmx-sw/scripts/ldmx-env.sh
```
- Check that `ldmx` can run:
```
ldmx
```
- Then install github repo in a similar path:
```
git clone git@github.com:cmantill/ldmx-fnal.git
```

## Tutorial

Two example are provided in `ana_example*.py`.
- Example data is placed in `data/`
  Copy data from https://www.dropbox.com/sh/jbw6iai2wez95fp/AABnIy7nUf1_IBbYuNNCuqGda?dl=0
  into the `data/` directory.

- Output arrays will be saved with pickle (in .pkl format) and stored in `output/`

How to run:
```
# first example
ldmx python3 ana_example_1.py
# second example
ldmx python3 ana_example_2.py data/ngun_870mm_0.10_gev.root data/ngun_870mm_0.80_gev.root --output example_2
```

### Accessing Hcal ID information

To access Hcal ID information you need a particular configuration of ldmx-sw
```
cd ldmx-sw/
git switch iss1048-detectorID-bindings
git submodule update
ldmx use dev iss41-boost-python
mkdir build; cd build;
ldmx cmake .. -DBUILD_DETECTORID_BINDINGS=ON
ldmx make install -j2
```

Then you can run
```
ldmx python3
import libDetDescr
```

If this works, look at `get_hcalids.py` as an example to get the layer and strip numbering of an HcalHit.

## Plotting

In `plot/` you will find tools to plot the arrays saved in the pickle files.

- Common functions will be saved in `plot/utils.py`.
- Needed libraries are:
```
pip3 install hist mplhep
```

### Example
An example is provided in `plot_example.py`.

How to run:
```
cd plot/
# first example ../output/example_1.pkl
python3 plot_example_1.py
# second example from ../output/example_2.pkl
python3 plot_example_2.py ../output/example_2.pkl 
```
