# Analysis

Use `EventTree.py` to analyze LDMX Events.

## Getting started
- Install https://docs.docker.com/engine/install/
- Clone repo:
```
git clone --recursive git@github.com:LDMX-Software/ldmx-sw.git
```
* Note: You need to setup an SSH-key with your GitHub account on the computer you are using.
- Setup the environment (in bash): source ldmx-sw/scripts/ldmx-env.sh
- Check that `ldmx` can run:
```
ldmx
```

## Tutorial

Two example are provided in `ana_example*.py`.
- Example data is placed in `data/`
- Output arrays will be saved with pickle (in .pkl format) and stored in `output/`

How to run:
```
# first example
ldmx python3 ana_example_1.py
# second example
ldmx python3 ana_example_2.py data/ngun_870mm_0.10_gev.root data/ngun_870mm_0.80_gev.root --output example_2
```

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
# first example ../data/example_1.pkl
# second example from ../data/example_2.pkl
python3 plot_example_1.py
```