import multiprocessing
import random
import string
import time


def generate_random_string():
    length = random.randint(2, 50)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def find_me_a_collision(process_num, error_queue):
    original_string = generate_random_string()
    original_hash = hash(original_string)

    cycles_to_do = 100_000_000_000
    current_cycle = 0
    for i in range(cycles_to_do):
        random_string = generate_random_string()
        new_hash = hash(random_string)

        if new_hash == original_hash:
            if original_string != random_string:
                message = f'\n----------------------\n' \
                          f'Collision happened!\n' \
                          f'Original string {original_string} generated hash "{original_hash}"\n' \
                          f'Random string {random_string} generated hash "{new_hash}"!'
                error_queue.put((process_num, message))

        current_cycle += 1
        if not current_cycle % 100_000:
            print(f'Process #{process_num}: Iteration {current_cycle}. '
                  f'No collisions yet. {cycles_to_do - current_cycle} cycles left...')


if __name__ == "__main__":
    # Number of processes to run in parallel
    num_processes = multiprocessing.cpu_count() - 4

    # Create a list to hold process objects
    processes = []

    error_queue = multiprocessing.Queue()

    # Start multiple processes
    for process_number in range(num_processes):
        process = multiprocessing.Process(target=find_me_a_collision, args=(process_number + 1, error_queue,))
        processes.append(process)
        process.start()

    while error_queue.empty():
        time.sleep(1)

    _, error_msg = error_queue.get()
    print(error_msg)

    for process in processes:
        process.terminate()
