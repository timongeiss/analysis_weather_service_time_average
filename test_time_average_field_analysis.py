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
