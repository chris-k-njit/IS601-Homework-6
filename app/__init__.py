# """
# Dynamically load and execute command plugins without a strict command interface.
# """
# import pkgutil
# import importlib
# from typing import Dict, Any, Callable
# from app.commands import CommandHandler, Command

# class App:
#     """
#     Core application class that handles command registration and execution.
#     Dynamically loads command plugins and executes them based on user input.
#     """
#     def __init__(self):
#         self.commands: Dict[str, Callable] = {}

#     def load_plugins(self):
#         """
#         Dynamically load command plugins from the app/plugins directory.
#         Assumes each plugin module defines an `execute` function.
#         """
#         plugins_package = 'app.plugins'
#         discovered_plugins = pkgutil.iter_modules([plugins_package.replace('.', '/')])

#         for _, plugin_name, _ in discovered_plugins:
#             plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
#             execute_function = getattr(plugin_module, 'execute', None)
#             if callable(execute_function):
#                 self.commands[plugin_name] = execute_function

#     def execute_command(self, command_name: str, *args):
#         """
#         Execute a registered command by its name, passing any arguments.
#         """
#         command = self.commands.get(command_name)
#         if command:
#             command(*args)  # Directly invoke the execute function
#         else:
#             print(f"No such command: '{command_name}'")

#     def run(self):
#         """
#         Main loop to run the application.
#         """
#         self.load_plugins()
#         print("Welcome to the Chris' calculator application.")
#         print("\tType a command to execute. Type 'exit' to quit.")

#         while True:
#             user_input = input(">>> ").strip()
#             if user_input == "exit":
#                 print("Exiting calculator application...")
#                 raise SystemExit
#             command_name, *args = user_input.split(maxsplit=1)
#             args = args[0].split() if args else []
#             self.execute_command(command_name, *args)

import pkgutil
import importlib
from app.commands import CommandHandler
from app.commands import Command

class App:
    def __init__(self): # Constructor
        self.command_handler = CommandHandler()

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)):  # Assuming a BaseCommand class exists
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore
    def start(self):
        # Register commands here
        self.load_plugins()
        print("Type 'exit' to exit.")
        while True:  #REPL Read, Evaluate, Print, Loop
            self.command_handler.execute_command(input(">>> ").strip())