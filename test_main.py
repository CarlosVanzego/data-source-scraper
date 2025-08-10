# This is my test file; It will test that my data cleaning function renames columns correctly and converts data types as expected.
# 'pytest' is a framework for writing tests in Python.
# 'pandas' is for data manipulation and analysis.
# from main import clean_eia_data is importing my data cleaning function from my main.py file.
import pytest
import pandas as pd
from main import clean_eia_data

@pytest.fixture
def raw_data_frame():
    """Returns a sample raw DataFrame for testing"""
    data = {
        'period': ['2024-01', '2025-02'],
        'value': ['100', '200'],
        'statedid': ['TX', 'TX']
    }
    return pd.DataFrame(data)

def test_columns_renamed_correctly(raw_data_frame):
    """Test that the cleaning function renames columns as expected"""
    cleaned_df = clean_eia_data(raw_data_frame)
    expected_columns = ['date', 'production_bbl_per_day', 'stateid']
    assert list(cleaned_df.columns) == expected_columns

def test_data_types_converted_correctly(raw_data_frame):
    """Test that the 'date' and 'production' columns have the right data types"""
    cleaned_df = clean_eia_data(raw_data_frame)
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['date'])
    assert pd.api.typrd.is_numeric_dtype(cleaned_df['production_bbl_per_day'])