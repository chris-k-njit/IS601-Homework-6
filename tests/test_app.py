# ''' Test app.py here'''
# import logging
# import pytest
# from app import App  # Adjust import based on actual class name

# def test_app_get_environment_variable():
#     app = App()
# #   Retrieve the current environment setting
#     current_env = app.get_environment_variable('ENVIRONMENT')
#     # Assert that the current environment is what you expect
#     assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

# def test_app_start_exit_command(monkeypatch):
#     """Test that the REPL exits correctly or handles 'exit' command."""
#     monkeypatch.setattr('builtins.input', lambda _: 'exit')
#     app = App()
#     with pytest.raises(SystemExit) as e:
#         app.start()  # Assuming 'start' is the correct method name
#     assert e.type == SystemExit

# def test_app_start_unknown_command(capfd, monkeypatch):
#     """Test how the REPL handles an unknown command before exiting."""
#     inputs = iter(['unknown_command', 'exit'])
#     monkeypatch.setattr('builtins.input', lambda _: next(inputs))

#     app = App()
#     with pytest.raises(SystemExit) as e:
#         app.start()  # Adjust for the actual method name
#     assert e.value.code == 0
#     captured = capfd.readouterr()
#     # Make sure this matches the exact output format of your application
#     assert "No such command: 'unknown_command'" in captured.out

import logging
import pytest
from app import App
from unittest.mock import patch, mock_open

@pytest.fixture
def app():
    return App()

def test_configure_logging_default(app, monkeypatch):
    """Test the default logging configuration is applied if logging.conf does not exist."""
    monkeypatch.setattr("os.path.exists", lambda path: False)
    with patch("logging.basicConfig") as mock_basicConfig:
        app.configure_logging()
        mock_basicConfig.assert_called_once()
        assert logging.getLogger().level == logging.INFO
        # You might need to adjust assertions based on your default configuration

def test_configure_logging_from_file(app, monkeypatch):
    """Test logging configuration from a file."""
    config_file_content = "[loggers]\nkeys=root\n"
    monkeypatch.setattr("os.path.exists", lambda path: True)
    with patch("builtins.open", mock_open(read_data=config_file_content)):
        with patch("logging.config.fileConfig") as mock_fileConfig:
            app.configure_logging()
            mock_fileConfig.assert_called_once()

def test_get_environment_variable(app):
    """Test retrieval of environment variables."""
    expected_env = "PRODUCTION"
    assert app.get_environment_variable('ENVIRONMENT') == expected_env

def test_app_start_exit_command(monkeypatch, app):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit

def test_app_start_unknown_command(capfd, monkeypatch, app):
    """Test how the REPL handles an unknown command before exiting."""
    inputs = iter(['unknown_command', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.value.code == 1  # Adjust based on your application's exit code for unknown commands
    captured = capfd.readouterr()
    assert "Unknown command entered: unknown_command" in captured.err  # Adjust based on your application's logging for unknown commands