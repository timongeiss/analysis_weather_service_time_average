import pandas as pd
import pytest
import time_average_field_analysis as tafa


def test_generate_time_average_radiation():
    days = 2
    samples_per_hour = 6
    scaling_factor = 150

    data, hourly_mean = tafa.generate_time_average_radiation(
        days=days, samples_per_hour=samples_per_hour, scaling_factor=scaling_factor
    )

    # check type
    assert isinstance(data, pd.DataFrame), "data should be dataframe"
    assert isinstance(hourly_mean, pd.DataFrame), "hourly_mean shout be dataframe"

    # check column
    assert "time" in data.columns
    assert "radiation" in data.columns
    assert "cumulative_area" in data.columns
    assert "cumulative_mean" in data.columns

    # check lenght of dataset
    expected_length = days * 24 * samples_per_hour + 1
    assert len(data) == expected_length, f"data should have {expected_length} rows"

    # no night radiation
    assert (data["radiation"] >= 0).all(), "all radiation values are >= 0"


def test_recalculate_original_values():
    hourly_mean = pd.DataFrame(
        {
            "hour": pd.date_range(start="2025-01-01", periods=3, freq="H"),
            "cumulative_mean": [0, 50, 100],
        }
    )

    result = tafa.recalculate_original_values(hourly_mean)

    # check column
    assert "Original" in result.columns

    # check lenght
    assert len(result) == 3

    # check for pos radiation
    assert result.loc[1, "Original"] >= 0


def test_plot_radiation_analysis():
    data = pd.DataFrame(
        {
            "time": pd.date_range(start="2025-01-01", periods=3, freq="H"),
            "radiation": [0, 100, 50],
            "cumulative_area": [0, 50, 75],
            "cumulative_mean": [0, 50, 75],
        }
    )

    hourly_mean = pd.DataFrame(
        {
            "hour": pd.date_range(start="2025-01-01", periods=3, freq="H"),
            "cumulative_mean": [0, 50, 75],
        }
    )

    hourly_mean_with_reconstruction = pd.DataFrame(
        {
            "hour": pd.date_range(start="2025-01-01", periods=3, freq="H"),
            "Original": [0, 100, 50],
        }
    )

    # check for failiure
    tafa.plot_radiation_analysis(data, hourly_mean, hourly_mean_with_reconstruction)
