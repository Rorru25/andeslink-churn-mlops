from src.config import TARGET_COLUMN
from src.data import load_raw_data, validate_data


def test_load_raw_data_not_empty():
    df = load_raw_data()
    assert not df.empty


def test_target_column_exists():
    df = load_raw_data()
    assert TARGET_COLUMN in df.columns


def test_validate_data_runs_without_error():
    df = load_raw_data()
    validate_data(df)
