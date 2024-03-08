''' Test app.py here'''
import pytest
from app import App  # Adjust import based on actual class name

import pytest
from app import App  # Adjust import based on actual class name

def test_app_start_exit_command(monkeypatch):
    """Test that the REPL exits correctly or handles 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    with pytest.raises(SystemExit) as e:
        app.start()  # Assuming 'start' is the correct method name
    # Optionally, you can check the exit code if your application sets one
    # assert e.value.code == some_expected_code


# def test_app_start_exit_command(capfd, monkeypatch):
#     """Test that the REPL exits correctly or handles 'exit' command."""
#     # Adjust the method name and approach if your app doesn't explicitly raise SystemExit
#     monkeypatch.setattr('builtins.input', lambda _: 'exit')
#     app = App()
#     app.start()  # Assuming 'run' is the correct method name
#     # If the application doesn't exit, check the output instead
#     captured = capfd.readouterr()
#     assert "Exiting application." in captured.out  # Adjust the expected string as needed


def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.start()  # Adjust for the actual method name
    captured = capfd.readouterr()
    # Make sure this matches the exact output format of your application
    assert "No such command: 'unknown_command'" in captured.out

# def test_app_start_unknown_command(capfd, monkeypatch):
#     """Test how the REPL handles an unknown command before exiting."""
#     inputs = iter(['unknown_command', 'exit'])
#     monkeypatch.setattr('builtins.input', lambda _: next(inputs))

#     app = App()
#     app.start()  # Adjust for the actual method name
#     captured = capfd.readouterr()
#     # Adjust the assertion to match the actual handling of unknown commands
#     assert "No such command: 'unknown_command'" in captured.out  # Update the expected feedback