from pathlib import Path

from src.config import MODEL_PATH


def test_model_file_exists_after_training():
    assert Path(MODEL_PATH).exists()
