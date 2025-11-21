COMMANDS = {}

def command(name=None):
    def wrapper(func):
        cmd_name = name or func.__name__
        COMMANDS[cmd_name] = func
        return func
    return wrapper

def run_command(name, *args, **kwargs):
    if name not in COMMANDS:
        raise ValueError(f"Unknown command: {name}")
    return COMMANDS[name](*args, **kwargs)