"""
Unit tests for SetupManager.

These tests verify:
- region selection via simulated mouse clicks
- config saving behavior
- optional callback handling (on_step)
- robustness when callbacks are not provided

All pynput mouse input is fully mocked to ensure deterministic tests.
"""

import pytest
from unittest.mock import patch
from src.managers.setup_manager import SetupManager


# ==================================================
# Fake mouse module used to replace pynput
# ==================================================
class FakeMouse:
    """
    Simulates pynput.mouse module for unit testing.

    This avoids OS-level mouse hooks and ensures deterministic behavior.
    """

    class Button:
        """Button"""
        left = "left"

    class Listener:
        """
        Fake listener that simulates two user clicks:
        - top-left corner
        - bottom-right corner
        """

        def __init__(self, on_click=None):
            self.on_click = on_click

        def __enter__(self):
            # Simulate first click (top-left)
            self.on_click(10, 20, FakeMouse.Button.left, True)

            # Simulate second click (bottom-right)
            self.on_click(110, 220, FakeMouse.Button.left, True)

            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def join(self):
            """Join function"""
            # No blocking required in tests
            pass


# ==================================================
# TEST 1: Full setup flow with callback
# ==================================================
def test_setup_region_saves_region():
    """
    Ensures:
    - region is calculated correctly
    - config is saved
    - on_step callback is triggered in correct order
    """

    manager = SetupManager()
    steps = []

    def on_step(step):
        steps.append(step)

    with patch("src.managers.setup_manager.mouse", FakeMouse), \
         patch("src.managers.config_manager.save_region") as mock_save:

        manager.setup_region("test_region", on_step=on_step)

    # Validate calculated region
    assert manager.region == (10, 20, 100, 200)

    # Validate config save
    mock_save.assert_called_once_with(
        (10, 20, 100, 200),
        "test_region"
    )

    # Validate UI step flow
    assert steps == ["top_left", "bottom_right_prompt", "done"]


# ==================================================
# TEST 2: Setup without callback (headless mode)
# ==================================================
def test_setup_region_without_callback():
    """
    Ensures setup works even when no on_step callback is provided.
    """

    manager = SetupManager()

    with patch("src.managers.setup_manager.mouse", FakeMouse), \
         patch("src.managers.config_manager.save_region") as mock_save:

        manager.setup_region("test_region")

    assert manager.region == (10, 20, 100, 200)
    mock_save.assert_called_once()


# ==================================================
# TEST 3: Edge case safety (defensive behavior)
# ==================================================
def test_setup_region_safe_execution_flow():
    """
    Ensures function does not crash under minimal conditions.

    This verifies:
    - listener still runs
    - region is still computed
    - no dependency on external callback or UI
    """

    manager = SetupManager()

    with patch("src.managers.setup_manager.mouse", FakeMouse), \
         patch("src.managers.config_manager.save_region"):

        try:
            manager.setup_region("test_region")
        except Exception as e:
            pytest.fail(f"SetupManager crashed unexpectedly: {e}")

    assert manager.region == (10, 20, 100, 200)
