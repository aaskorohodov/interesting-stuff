import random
import string
import time

import multiprocessing.managers


class CollisionFinder:
    """Executes actual job of finding collisions

    Attributes:
        symbols: Symbols, that will be used to generate random strings"""

    def __init__(self):
        """Init"""

        self.symbols = tuple(string.ascii_letters + string.hexdigits + string.punctuation)

    def find_me_a_collision(self,
                            process_num: int,
                            collisions: multiprocessing.managers.ListProxy,
                            stat: multiprocessing.managers.DictProxy,
                            print_each_cycles: int,
                            cycles_per_each_process: int) -> None:
        """Actual job of finding a collision, that will be executed in different processes

        Args:
            process_num: Number of current process
            collisions: List, where collision-message will be added, in case collision will happen
            stat: Process-communicator, where this process will place its current progress
            print_each_cycles: How often should this process update stat
            cycles_per_each_process: How many cycles should this process work"""

        # Creating original string to compare all the other hashes with its hash
        original_string = self._generate_random_string()
        original_hash = hash(original_string)

        current_cycle = 0
        cycle_begins_time = time.perf_counter()
        for _ in range(cycles_per_each_process):
            # Generating new string and getting its hash
            random_string = self._generate_random_string()
            new_hash = hash(random_string)

            # Checking if hashes are the same and string are different
            if new_hash == original_hash:
                if original_string != random_string:
                    collision_msg = self._make_collision_msg(original_string,
                                                             random_string,
                                                             original_hash,
                                                             new_hash,
                                                             process_num)
                    collisions.append(collision_msg)  # This will trigger termination of all processes

            # Updating data each 'print_each_cycles' cycles
            current_cycle += 1
            if not current_cycle % print_each_cycles:
                cycle_end_time = time.perf_counter()
                cycle_took_time = round(cycle_end_time - cycle_begins_time, 5)
                stat[process_num]['cycle'] = current_cycle
                stat[process_num]['time_took'] = cycle_took_time
                cycle_begins_time = time.perf_counter()

    def _generate_random_string(self):
        """Generates random string"""

        return ''.join(random.choice(self.symbols) for _ in range(random.randint(2, 100)))

    def _make_collision_msg(self, *args) -> str:
        """Creates a message about collision

        Returns:
            A message about collision"""

        original_string, random_string, original_hash, new_hash, process_num = args
        message = f'\n----------------------\n' \
                  f'Collision happened!\n' \
                  f'Original string "{original_string}" generated hash "{original_hash}"\n' \
                  f'Random string "{random_string}" generated hash "{new_hash}"!'

        return message
