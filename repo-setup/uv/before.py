##
## To run this you need to set up the environment manually, every time, on every machine:
##
##   python3 -m venv .venv
##   source .venv/bin/activate
##   pip install numpy
##   python3 before.py
##   deactivate
##

import numpy

rng = numpy.random.default_rng(seed=0)
data = rng.normal(loc=0.0, scale=1.0, size=1_000_000)

print(f"\t> mean: {data.mean():.4f}")
print(f"\t> std: {data.std():.4f}")
print(f"\t> min: {data.min():.4f}")
print(f"\t> max: {data.max():.4f}")
