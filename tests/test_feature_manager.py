"""Feature Manager unit testing"""

from unittest.mock import patch
from src.managers.feature_manager import FeatureManager


def test_auto_tab():
    """Tests AutoTab feature"""
    fm = FeatureManager()

    with patch("src.managers.feature_manager.pyautogui.hotkey") as mock_hotkey:
        fm.auto_tab()

        mock_hotkey.assert_called_once_with("ctrl", "tab")


def test_eat_food():
    """Tests AutoFood feature"""
    fm = FeatureManager()

    with patch("src.managers.feature_manager.pyautogui.press") as mock_press:
        fm.eat_food("f1")

        mock_press.assert_called_once_with("f1")


def test_make_rune():
    """Tests RuneMaker feature"""
    fm = FeatureManager()

    with patch("src.managers.feature_manager.pyautogui.press") as mock_press:
        fm.make_rune("f2")

        mock_press.assert_called_once_with("f2")


def test_make_rune_lowercase():
    """Tests RuneMaker lowercase feature"""
    fm = FeatureManager()

    with patch("src.managers.feature_manager.pyautogui.press") as mock_press:
        fm.make_rune("F5")

        mock_press.assert_called_once_with("f5")


def test_make_rune_strip_spaces():
    """Tests RuneMaker strip spaces feature"""
    fm = FeatureManager()

    with patch("src.managers.feature_manager.pyautogui.press") as mock_press:
        fm.make_rune("  f6  ")

        mock_press.assert_called_once_with("f6")
