# Analysis

Use `EventTree.py` to analyze LDMX Events.

## Tutorial

An example is provided in `analysis_example.py`.
- Example data is placed in `data/`
- Output arrays will be saved with pickle (in .pkl format) and stored in `output/`

How to run:
```
ldmx python3 analyze_example.py data/ngun_870mm_0.10_gev.root data/ngun_870mm_0.80_gev.root --output neutron_guns
```

## Plotting

In `plot/` you will find tools to plot the arrays saved in the pickle files.
Common functions will be saved in `plot/utils.py`.

### Example
An example is provided in `plot_example.py`

How to run:
```

```


