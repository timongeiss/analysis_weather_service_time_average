import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_time_average_radiation(days=4, samples_per_hour=6, scaling_factor=150):
    """
    Generates a fictitious radiation time series for the original values
    and computes the cumulative mean and hourly averages.

    Returns:
    - data: DataFrame with radiation and cumulative means
    - hourly_mean: DataFrame with cumulative hourly means
    """

    # basic funktion
    total_hours = days * 24
    time_index = np.linspace(0, total_hours, total_hours * samples_per_hour + 1)
    radiation_raw = np.sin((2 * np.pi / 24) * (time_index % 24) - np.pi / 2)

    # delete nighttimes
    radiation = np.clip(radiation_raw, 0, None)
    radiation = radiation * scaling_factor

    # add some fluctuation in the original values
    radiation_noisy = radiation.copy()
    positive_mask = radiation > 0
    noise = np.random.normal(0, 10, len(radiation[positive_mask]))
    radiation_noisy[positive_mask] += noise
    radiation_noisy = np.clip(radiation_noisy, 0, None)

    # time axis for the data
    time_index_datetime = pd.date_range(
        start="2025-03-15",
        periods=len(radiation_noisy),
        freq=f"{int(60 / samples_per_hour)}min",
    )

    # merge noisy curve and time index
    data = pd.DataFrame({"time": time_index_datetime, "radiation": radiation_noisy})

    # calculate the time average
    time_diff_hours = 1 / samples_per_hour
    data["time_diff"] = time_diff_hours  # time difference between time steps
    data["cumulative_area"] = (
        data["radiation"] * data["time_diff"]
    ).cumsum()  # accumulated area for each time step (Integral)
    data["cumulative_mean"] = (
        data["cumulative_area"] / ((data.index + 1) * time_diff_hours)
    )  # average value over the entire interval from the start to the current point in time

    # uses the last value for each hour (only one value is in the metadata for each hour, which contains the information from the integral of the preceding values)
    data["hour"] = data["time"].dt.floor("H")
    hourly_mean = data.groupby("hour")["cumulative_mean"].last().reset_index()

    return data, hourly_mean


def recalculate_original_values(hourly_mean):
    """
    Reconstructs the original hourly values from the cumulative mean values.

    Parameters:
    - hourly_mean: DataFrame with 'hour' and 'cumulative_mean'

    Returns:
    - hourly_mean_with_original: DataFrame with 'Original' in addition to 'cumulative_mean'
    """
    hourly_mean_with_original = hourly_mean.copy()
    hourly_mean_with_original["Original"] = 0.0

    for i in range(1, len(hourly_mean_with_original)):
        t1 = (
            hourly_mean_with_original.at[i - 1, "hour"]
            - hourly_mean_with_original.at[0, "hour"]
        ).total_seconds() / 3600
        t2 = (
            hourly_mean_with_original.at[i, "hour"]
            - hourly_mean_with_original.at[0, "hour"]
        ).total_seconds() / 3600

        y1 = hourly_mean_with_original.at[i - 1, "cumulative_mean"]
        y2 = hourly_mean_with_original.at[i, "cumulative_mean"]

        original_value = (t2 * y2 - t1 * y1) / (t2 - t1)

        hourly_mean_with_original.at[i, "Original"] = original_value

    return hourly_mean_with_original


def plot_radiation_analysis(data, hourly_mean, hourly_mean_with_reconstruction):
    """
    Parameters:
    - data: DataFrame with 'time', 'radiation', 'cumulative_mean'
    - hourly_mean: DataFrame with 'hour', 'cumulative_mean'
    - hourly_mean_with_reconstruction: DataFrame with 'hour', 'Original'
    """

    plt.figure(figsize=(14, 7))

    plt.scatter(
        data["time"],
        data["radiation"],
        label="Fictitious radiation data (noisy)",
        color="gray",
        s=3,
    )

    plt.plot(
        data["time"],
        data["cumulative_mean"],
        label="Time average for each step",
        linestyle="",
        marker="o",
        color="blue",
        markersize=1,
    )

    plt.plot(
        hourly_mean["hour"],
        hourly_mean["cumulative_mean"],
        label="Metadata published value (last of hour)",
        linestyle="-",
        marker="o",
        color="darkblue",
        markersize=3,
    )

    plt.plot(
        hourly_mean_with_reconstruction["hour"],
        hourly_mean_with_reconstruction["Original"],
        label="Reconstructed absolute",
        linestyle="-",
        marker="o",
        markersize=3,
        color="orange",
    )

    plt.xlabel("Time")
    plt.ylabel("Radiation in W/m²")
    plt.title("Time-averaging and absolute value reconstruction in weather wata")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


data, hourly_mean = generate_time_average_radiation(days=4, samples_per_hour=6)
hourly_mean_with_reconstruction = recalculate_original_values(hourly_mean)
plot_radiation_analysis(data, hourly_mean, hourly_mean_with_reconstruction)
