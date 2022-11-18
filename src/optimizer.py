"""Utilities to calculate the optimal path from a set of contracts."""

from collections import namedtuple

Contract = namedtuple('Contract', 'name, start, duration, price')

class Schedule:
    def __init__(self, income, path):
        self.income = income
        self.path = path

def find_latest_ending_before(contracts: list[Contract], date: int) -> int:
    """Returns the latest contract (by end date) before a given date, or null if there is none."""
    lower = 0
    upper = len(contracts) - 1
    while lower <= upper:
        mid = (lower + upper) // 2
        end = contracts[mid].start + contracts[mid].duration
        if end < date:
            lower = mid + 1
        elif end > date:
            upper = mid - 1
        else:
            return mid
    return -1

def calculate_optimal_schedule(contracts: list[Contract]) -> Schedule:
    """Returns the Schedule with the highest income that can be constructed."""
    # Sort contracts by end date.
    contracts.sort(key = lambda contract: contract.start + contract.duration)
    # Find for each contract the index of the latest contract that can be executed before it.
    indexes = [find_latest_ending_before(contracts, contract.start) for contract in contracts]

    # Build a list of schedules with the highest income subset of contracts up to a given index.
    schedules = []
    i = 0
    while i < len(contracts):
        # If no contract can be executed before this one, just include it.
        if indexes[i] < 0:
            schedules.append(Schedule(contracts[i].price, [contracts[i].name]))
        else:
            # Check if a higher income can be obtained by adding the contract.
            income_adding_node = contracts[i].price + schedules[indexes[i]].income
            income_previous_node = schedules[i - 1].income
            if income_adding_node > income_previous_node:
                path = schedules[indexes[i]].path + [contracts[i].name]
                schedules.append(Schedule(income_adding_node, path))
            else:
                schedules.append(Schedule(income_previous_node, schedules[i - 1].path))
        i += 1

    return schedules[len(contracts) - 1]
