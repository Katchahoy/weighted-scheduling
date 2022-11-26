"""Utilities to calculate the optimal path from a set of contracts."""

from collections import namedtuple

Contract = namedtuple('Contract', 'name, start, duration, price')


class Schedule:
    def __init__(self, income: int, path: list[str]):
        self.income = income
        self.path = path


class ScheduleNode:
    def __init__(
        self,
        contract: Contract,
        node: 'ScheduleNode' = None
    ):
        self.income = contract.price + (0 if node is None else node.income)
        self.contract_name = contract.name
        self.node = node

    def path(self) -> list[str]:
        if self.node is None:
            return [self.contract_name]
        else:
            path = self.node.path()
            path.append(self.contract_name)
            return path


def find_latest_before(contracts: list[Contract], date: int) -> int:
    """
    Returns the latest contract (by end date) before a given date,
    or null if there is none.
    """
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
    return lower - 1


def calculate_optimal_schedule(contracts: list[Contract]) -> Schedule:
    """Returns the Schedule with the highest income that can be constructed."""
    if len(contracts) == 0:
        return Schedule(0, [])
    # Sort contracts by end date.
    contracts.sort(key=lambda contract: contract.start + contract.duration)
    # Find the index of the latest contract that can be executed before each.
    indexes = [
        find_latest_before(contracts, contract.start) for contract in contracts
    ]

    # Build a list of schedules with the highest income subset
    # of contracts up to a given index.
    schedules = [ScheduleNode(contracts[0])]
    i = 1
    while i < len(contracts):
        # If no contract can be executed before this one, just include it.
        previous_price = 0 if indexes[i] < 0 else schedules[indexes[i]].income
        income_adding_node = previous_price + contracts[i].price
        # Check if a higher income can be obtained by adding the contract.
        income_previous_node = schedules[i - 1].income
        if income_adding_node > income_previous_node:
            if indexes[i] < 0:
                schedules.append(ScheduleNode(contracts[i]))
            else:
                schedules.append(
                    ScheduleNode(contracts[i], schedules[indexes[i]])
                )
        else:
            schedules.append(schedules[i - 1])
        i += 1

    optimal_schedule = schedules[len(contracts) - 1]
    return Schedule(optimal_schedule.income, optimal_schedule.path())
