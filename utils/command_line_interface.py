import sys

class CommandInterface:
    """
    Just a simple helper class to facilitate command line interactions.
    """
    def __init__(self, main_command_prompt: str):
        sys.stdout.write(main_command_prompt + '\n')
        sys.stdout.write("=" * 20 + '\n')
        sys.stdout.flush()

    def read_symbol(self) -> str:
        return sys.stdin.read(1)

    def write(self, prompt) -> None:
        sys.stdout.write('\r' + prompt)
        sys.stdout.flush()

    def write_instruction(self, instruction) -> None:
        sys.stdout.write('\r' + instruction + '\n')
        sys.stdout.flush()
