"""
Wiki: https://en.wikipedia.org/wiki/Monty_Hall_problem

Suppose you're on a game show, and you're given the choice of three doors: Behind one door is a car; behind the
others, goats. You pick a door, say No. 1, and the host, who knows what's behind the doors, opens another door,
say No. 3, which has a goat. He then says to you, "Do you want to pick door No. 2?" Is it to your advantage to
switch your choice?

This code illustrates, that switching doors actually helps.
"""


import random


def simulate_monty_hall(num_attempts: int) -> tuple[int, int]:
    """Simulates the game N times, on each sticks to original choice and changes it

    Args:
        num_attempts: Number of attempts
    Returns:
        Number of successes when initial choice was switched, and when it was not"""

    switch_success = 0
    stick_success = 0

    # Simulate the scenario: 3 doors and a prize behind one of them
    doors = ['goat', 'goat', 'car']

    for _ in range(num_attempts):
        # Shuffle to randomize prize location
        random.shuffle(doors)

        # Participant's initial choice
        original_choice = random.randint(0, 2)

        # Monty Hall opens one door without the prize
        remaining_closed_doors = get_remaining_closed_doors_with_goats(original_choice, doors)
        monty_opens = random.choice(remaining_closed_doors)

        # Switch strategy: change the choice to the other unopened door
        switch_choice = switch_doors(original_choice, monty_opens)
        if doors[switch_choice] == 'car':
            switch_success += 1

        # Stick strategy: keep the initial choice
        if doors[original_choice] == 'car':
            stick_success += 1

    return switch_success, stick_success


def get_remaining_closed_doors_with_goats(choice: int, doors: list[str]) -> list[int]:
    """Gets doors, that player did not choice initially, and which have a goat in it.

    May return list with 1 or 2 elements.

    Args:
        choice: Original choice
        doors: All doors
    Returns:
        List[representing doors with goats, that player did not initially selected]"""

    closed_doors = []
    for i in range(3):
        if i != choice and doors[i] != 'car':
            closed_doors.append(i)

    return closed_doors


def switch_doors(original_choice: int, monty_opened: int) -> int:
    """Switching initial choice

    Args:
        original_choice: Door number of original choice
        monty_opened: Door number, that Monty opened for us (with goat)
    Returns:
        New choice"""

    for i in range(3):
        if i != original_choice and i != monty_opened:
            return i


# Number of attempts
attempts = 100_000

# Simulate the Monty Hall problem
switch, stick = simulate_monty_hall(attempts)

# Display the results
print(f"Switching doors success: {switch} out of {attempts}. Success rate = {round(switch/attempts, 2)}")
print(f"Sticking to initial choice success: {stick} out of {attempts}. Success rate = {round(stick/attempts, 2)}")
