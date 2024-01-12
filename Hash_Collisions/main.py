"""
This is an attempt to create a hash-collision. In this example, we will try to:

1. Create a string and get its hash
2. Generate a lot of other strings in attempt to find the same hash from different value

This process will be executed in parallel using multiprocessing. Each process will do the same:

- Create a string and save its hash
- Generate other strings and compare their hashes with original hash from original string

If any of the processes finds a collision - the whole program will stop and a message will be displayed.


!!!!!!!!!!!!!!!!!!! IMPORTANT !!!!!!!!!!!!!!!!!!!:
You may wanna adjust the number of processes, so that your PC will be able to do something else, like let you move a
mouse or stop this madness.

Make sure that your PC has a proper cooling system and there are enough thermo-paste on your CPU.

Approximate time of encountering a collision should (maybe, as I calculated it) be about 2^32 (4_294_967_296)
cycles, to have a 50% chance.
"""


from Processes_Manager import ProcessesManager


if __name__ == "__main__":
    process_manager = ProcessesManager(
        spare_these_processes=2,
        update_each_cycles=100_000,
        cycles_per_each_process=100_000_000_000
    )
    process_manager.book_processes()
    process_manager.execute_this_shit()
