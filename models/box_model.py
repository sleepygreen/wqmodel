import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ammonium = {
    "ammonium": 1
}

sources = {
    "ammonia": 0.001,
    "temp": 15,
    "pH": 8,
    "atmospheric_deposition": 2,
    "point_sources": 0.02,
    "diffuse_sources": 0.04
}

sinks = {
    "bio-uptake": 5,
    "sediment_deposition": 0.04,
}

num_pars = len(sources) + len(sinks)
parameters = {**ammonium, **sources, **sinks}


def init_box(parameters: dict) -> pd.DataFrame:
    box = pd.DataFrame(data=parameters, index=[0])
    return box


def calc_source_change(box):
    dn_dt = box['point_sources'] + box['diffuse_sources']
    return dn_dt


def calc_sink_change(box):
    dn_dt = -box["sediment_deposition"] * box["ammonium"]
    return dn_dt


def iterate_model(box, t: int) -> pd.DataFrame:
    box_copy = box.copy(deep=True)
    results = [box_copy]
    for t in range(t):
        source_change = calc_source_change(results[-1])
        sink_change = calc_sink_change(results[-1])
        dn = source_change + sink_change
        change = np.array([dn] + [0 for par in range(num_pars)])
        parameter_change = results[-1] + change
        results.append(parameter_change)

    return pd.concat(results).reset_index()


box = init_box(parameters=parameters)

results = iterate_model(box, 100)

fig, ax = plt.subplots()
ax.plot(results['ammonium'])
ax.set_xlabel("Time/s")
ax.set_ylabel("Ammonium/mg/l", position=(1, 1.05), rotation=0, labelpad=-20)
plt.show()
