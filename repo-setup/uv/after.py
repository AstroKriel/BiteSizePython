# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
# ]
# ///

##
## uv run after.py
##
## That is it. No venv, no activate, no pip install, no deactivate.
## uv reads the block above, installs what is needed, and runs the script.
##

import numpy

rng = numpy.random.default_rng(seed=0)
data = rng.normal(loc=0.0, scale=1.0, size=1_000_000)

print(f"\t> mean: {data.mean():.4f}")
print(f"\t> std: {data.std():.4f}")
print(f"\t> min: {data.min():.4f}")
print(f"\t> max: {data.max():.4f}")
