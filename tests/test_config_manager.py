"""
Unit tests for config_manager.

Covers:
- loading missing config
- saving full config
- saving/loading generic values
- saving/loading regions

All file I/O is mocked to ensure safe and deterministic tests.
"""

import pytest
from unittest.mock import patch
import src.managers.config_manager as cfg


# ==================================================
# TEST 1: Missing config file
# ==================================================
def test_load_config_missing_file():
    """
    Should return empty dict when file does not exist.
    """

    with patch("os.path.exists", return_value=False):
        result = cfg.load_config()

    assert result == {}


# ==================================================
# TEST 2: save_config writes JSON
# ==================================================
def test_save_config_writes_json():
    """
    Ensures save_config calls json.dump via file write.
    """

    from unittest.mock import mock_open

    with patch("builtins.open", mock_open()) as m:
        cfg.save_config({"test": 123})

    m.assert_called_once()


# ==================================================
# TEST 3: save_value + load_value cycle
# ==================================================
def test_save_and_load_value():
    """
    Ensures generic values persist correctly.
    """

    state = {}

    def fake_load():
        return dict(state)

    def fake_save(new_data):
        state.clear()
        state.update(new_data)

    with patch("src.managers.config_manager.load_config", fake_load), \
         patch("src.managers.config_manager.save_config", fake_save):

        cfg.save_value("food_key", "F1")

        result = cfg.load_value("food_key")

    assert result == "F1"


# ==================================================
# TEST 4: save_region + load_region cycle
# ==================================================
def test_save_and_load_region():
    """
    Ensures region tuple is correctly stored and retrieved.
    """

    state = {}

    def fake_load():
        return dict(state)

    def fake_save(new_data):
        state.clear()
        state.update(new_data)

    with patch("src.managers.config_manager.load_config", fake_load), \
         patch("src.managers.config_manager.save_config", fake_save):

        cfg.save_region((10, 20, 30, 40), "test_region")

        region = cfg.load_region("test_region")

    assert region == (10, 20, 30, 40)


# ==================================================
# TEST 5: save_value override behavior
# ==================================================
def test_save_value_overwrites_existing_key():
    """
    Ensures saving a key overwrites previous value.
    """

    state = {"food_key": "OLD"}

    def fake_load():
        return dict(state)

    def fake_save(new_data):
        state.clear()
        state.update(new_data)

    with patch("src.managers.config_manager.load_config", fake_load), \
         patch("src.managers.config_manager.save_config", fake_save):

        cfg.save_value("food_key", "NEW")

        result = cfg.load_value("food_key")

    assert result == "NEW"
