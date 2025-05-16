import csv

from traitlets import Callable

from routines.constants import Context
from routines.routine import Routine
from utils.command_line_interface import CommandInterface
from utils.timing import UET


class CheckExtraTimestampsRoutine(Routine):
    def __init__(self, video_id: int = 0, update: Callable = lambda x: x):
        self.video_id = video_id
        self.__context = Context()
        self.__upd = update
        self.__timestamps = []

    def __find_problematic_spots(self):
        cmd = CommandInterface("Starting vetting job!")
        with open(self.__context.EXTRA_TIMESTAMPS_FOLDER + f"{self.video_id}.csv", 'r') as f:
            reader = csv.reader(f)
            prev_uet = 0
            counter = -1
            problematic_spots = []
            for row in reader:
                counter += 1
                uet = UET(row[0])
                self.__timestamps.append(row[0])
                if uet < prev_uet:
                    problematic_spots.append(counter)
                prev_uet = uet
            cmd.write_instruction("PROBLEMATIC SPOTS")
            cmd.write_instruction(str(problematic_spots))
        cmd.write_instruction("Vetting job done!")

    def execute(self):
        cmd = CommandInterface('Starting checking your timestamps!')
        self.__find_problematic_spots()
        cmd.write("Would you like to change all of your timestamps? y/N ")
        key = cmd.read_symbol()
        if key.lower() == "y":
            self.__timestamps = list(map(lambda x: [self.__upd(x)], self.__timestamps))
            with open(self.__context.EXTRA_TIMESTAMPS_FOLDER + f"{self.video_id}.csv", 'w') as f:
                writer = csv.writer(f)
                writer.writerows(self.__timestamps)
            cmd.write_instruction("Changes applied!")
            return True
        cmd.write_instruction("No changes applied!")
        return True
