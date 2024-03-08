from app.commands import Command

class GreetCommand(Command):
    def execute(self):
        print("Hello! Welcome to Chris' the calculator. Type 'help' to see available commands.")