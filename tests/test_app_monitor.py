# tests/model/test_app_monitor.py
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from model.app_monitor import AppMonitor
from model.data_manager import DataManager

@pytest.fixture
def app_monitor():
    data_manager = DataManager()
    return AppMonitor(data_manager)

def test_start_tracking(app_monitor):
    app_monitor.start_tracking()
    assert app_monitor.is_tracking == True

def test_stop_tracking(app_monitor):
    app_monitor.start_tracking()
    app_monitor.stop_tracking()
    assert app_monitor.is_tracking == False
@patch("model.app_monitor.psutil.Process")
@patch("model.app_monitor.win32gui.GetForegroundWindow")
@patch("model.app_monitor.win32process.GetWindowThreadProcessId")
def test_get_active_app_info(mock_get_window_thread, mock_get_foreground, mock_process, app_monitor):
    mock_get_foreground.return_value = 1234
    mock_get_window_thread.return_value = (0, 5678)
    mock_process.return_value.name.return_value = "TestApp"
    mock_process.return_value.exe.return_value = "C:/Program Files/TestApp.exe"
    
    app_info = app_monitor.get_active_app_info()
    
    print("Test Output:", app_info)  # Added print statement
    
    assert app_info["name"] == "TestApp"
    assert app_info["exe"] == "C:/Program Files/TestApp.exe"
    assert app_info["pid"] == 5678

from unittest.mock import patch
from model.app_monitor import AppMonitor

@patch("model.app_monitor.win32api.GetLastInputInfo")
@patch("model.app_monitor.win32api.GetTickCount")
def test_get_last_input_time(mock_get_tick_count, mock_get_last_input):
    # Mock values for system input time and tick count
    mock_get_last_input.return_value = 100000
    mock_get_tick_count.return_value = 150000

    app_monitor = AppMonitor(data_manager=None)  # Mock data_manager if needed
    last_input_time = app_monitor.get_last_input_time()

    print("Last Input Time (seconds):", last_input_time)  # Debug print

    # Expected output: (150000 - 100000) / 1000 = 50.0 seconds
    assert last_input_time == 50.0

@patch("threading.Thread")
def test_start_tracking(mock_thread, app_monitor):
    app_monitor.start_tracking(interval=2)

    # Ensure two threads are created
    assert mock_thread.call_count == 2

    # Check that the correct target functions are being used
    mock_thread.assert_any_call(target=app_monitor._app_tracking_loop, args=(2,), daemon=True)
    mock_thread.assert_any_call(target=app_monitor._idle_detection_loop, args=(2,), daemon=True)

    # Ensure both threads are started
    assert mock_thread.return_value.start.call_count == 2
@patch("model.app_monitor.AppMonitor.is_system_idle")
@patch("time.sleep", return_value=None)  # Prevent actual sleeping in the loop
def test_idle_detection_loop(mock_sleep, mock_is_idle, app_monitor):
    app_monitor._log_idle_session = MagicMock()
    
    # Simulate idle state changes over iterations
    mock_is_idle.side_effect = [True, True, False, False]

    app_monitor.idle_start = None  # Ensure it starts as None
    app_monitor.is_tracking = True

    # Run the loop iteration manually to avoid infinite looping
    for _ in range(2):  
        app_monitor._idle_detection_loop(interval=1)

    # Check that idle_start was set when system went idle
    assert app_monitor.idle_start is not None

    # Check that _log_idle_session() was called when exiting idle state
    assert app_monitor._log_idle_session.called
