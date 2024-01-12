import multiprocessing
import multiprocessing.managers
import time

from multiprocessing import Process
from multiprocessing.managers import SyncManager
from typing import Optional

from Collision_Finder import CollisionFinder


class ProcessesManager:
    """Main controller. Manages processes, where collision finding is happening

    Attributes:
        cycles_per_each_process: How many cycles should each process try to find a collision
        update_each_cycles: How often should a process update its current status
        spare_these_processes: How many processes should NOT be used (so you could still use your PC)
        processes_to_use: Number of precesses, that will be used
        overall_cycles_to_do: How many overall cycles should be made (cycles_per_each_process * processes_to_use)

        collisions_list: ListProxy, where collision message will appear, if collision will happen
        status: Process-communicator, so that we could read data from processes in main-scope
        manager: multiprocessing.Manager, to launch processes and create related stuff
        processes: List witch created processes

        last_msg: Last message, generated during run time"""

    def __init__(self,
                 spare_these_processes: int,
                 update_each_cycles: int,
                 cycles_per_each_process: int):
        """Init

        Args:
            spare_these_processes: How many processes should NOT be used (so you could still use your PC)
            update_each_cycles: How often should a process update its current status
            cycles_per_each_process: How many cycles should each process try to find a collision"""

        self.cycles_per_each_process = cycles_per_each_process
        self.update_each_cycles = update_each_cycles
        self.spare_these_processes = spare_these_processes
        self.processes_to_use = 0
        self.overall_cycles_to_do: int = 0

        self.collisions_list: Optional[multiprocessing.managers.ListProxy] = None
        self.status: Optional[multiprocessing.managers.DictProxy] = None
        self.manager: Optional[SyncManager] = None
        self.processes: Optional[list[Process]] = []

        self.last_msg: str = ''

    def book_processes(self) -> None:
        """Finds out, how many processes to create and print initial message"""

        num_processes = multiprocessing.cpu_count()
        self.processes_to_use = num_processes - self.spare_these_processes
        msg = f'Your CPU has {num_processes} processes. Will use {self.processes_to_use} of them, ' \
              f'so that your PC will still be able to handle mouse-movement and wont explode'
        print(msg)

    def execute_this_shit(self) -> None:
        """Entry-point. Creates processes and watches, if there are any collisions happened"""

        with multiprocessing.Manager() as manager:
            self.manager = manager
            self.collisions_list = manager.list()
            self.status = manager.dict()
            self.overall_cycles_to_do = self.cycles_per_each_process * self.processes_to_use

            self._prepare_status()

            self._start_processes()

            # Checking, if collisions happened and printing progress if not
            while not self.collisions_list:
                time.sleep(0.1)
                self._print_progress()

            # If encountered a collision - printing results and stopping processes
            else:
                collision_message = self.collisions_list[0]
                print(collision_message)
                for process in self.processes:
                    process.terminate()

    def _prepare_status(self) -> None:
        """Creates a status (processes-communicator) and fills it with initial data"""

        for process_number in range(self.processes_to_use):
            proc_dict = self.manager.dict()
            proc_dict['cycle'] = 0
            proc_dict['time_took'] = 0.0
            self.status[process_number + 1] = proc_dict

    def _start_processes(self) -> None:
        """Starts processes"""

        collision_finder = CollisionFinder()
        for process_number in range(self.processes_to_use):
            process = multiprocessing.Process(
                target=collision_finder.find_me_a_collision,
                args=(
                    process_number + 1,
                    self.collisions_list,
                    self.status,
                    self.update_each_cycles,
                    self.cycles_per_each_process
                ))
            self.processes.append(process)
            process.start()

    def _print_progress(self) -> None:
        """Prints current progress"""

        overall_completed_cycles = 0  # How many cycles currently completed
        overall_time = 0              # How much time all the processes were executing current cycle
        for proc_num, data in self.status.items():
            overall_completed_cycles += data['cycle']
            overall_time += data['time_took']
        average_time = round(overall_time / len(self.status), 5)  # Average time each process was executing single cycle

        stat_msg = f'Cycles left: {self.overall_cycles_to_do - overall_completed_cycles}. ' \
                   f'Avg time: {average_time} sec per {self.update_each_cycles} cycles in each process. ' \
                   f'No collisions yet.'

        # Printing only if new message is different from the last one, not to spam with the same message
        if self.last_msg != stat_msg:
            print(stat_msg)
        self.last_msg = stat_msg
