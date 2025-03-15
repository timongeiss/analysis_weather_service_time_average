# License
This project comes with a MIT License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Time-averaging and absolute value reconstruction in weather wata

## Overview
Weather services, like the German Weather Service (DWD), often provide **time-averaged** forecast outputs rather than **absolute values**.
The modeled values of a model run are always averaged over the integral of the values calculated up to this point in time.
For many applications, such as energy modeling, **absolute values** are required.

This module demonstrates:
- How time-averaged fields are calculated in a numerical weather prediction by an example of the radiation prediction values for some location
- How "absolute" (not original) values can be reconstructed from them


## Functions

### `generate_time_average_radiation()`
Simulates fictitious radiation data over several days  
- Creates **realistic radiation curves** with some prediction/ simulation noise
- Calculates **time averaged fields** (cumulative means), mimicking the process used in weather models

### `recalculate_original_values()`
Reconstructs **absolute values** from the **time averaged fields**
Simulates reversing the **time-averaging process** common in weather services, recovering absolute data

### `plot_radiation_analysis()`
Shows the relationship between **averaged** and **reconstructed absolute values**, helping to understand the underlying data structure
Visualizes:
- The original fictitious noisy data: the output fields of a numerical weather prediction which are not published
- The time-averaged values: the values that you than find in the metadata 
- The reconstructed absolute values: a simple recalculation to use the absolute values for your application


## Workflow Example
```python
data, hourly_mean = generate_time_average_radiation(days=4, samples_per_hour=6)
hourly_mean_reconstructed = recalculate_original_values(hourly_mean)
plot_radiation_analysis(data, hourly_mean, hourly_mean_reconstructed)


