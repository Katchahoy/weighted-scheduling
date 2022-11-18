import unittest
from optimizer.optimizer import Contract, calculate_optimal_schedule

class TestOptimizer(unittest.TestCase):

    def test_empty_list(self):
        contracts = []
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 0)
        self.assertEqual(schedule.path, [])

    def test_single_contract(self):
        contracts = [Contract("Contract1", 0, 8, 5)]
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 5)
        self.assertEqual(schedule.path, ["Contract1"])

    def test_basic_case(self):
        contracts = [
            Contract("Contract1", 0, 5, 10),
            Contract("Contract2", 3, 7, 14),
            Contract("Contract3", 5, 9, 8),
            Contract("Contract4", 5, 9, 7),
        ]
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 18)
        self.assertEqual(schedule.path, ["Contract1", "Contract3"])

    def test_simple_sequence(self):
        contracts = [
            Contract("Contract1", 0, 5, 10),
            Contract("Contract2", 5, 7, 3),
            Contract("Contract3", 12, 3, 8)
        ]
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 21)
        self.assertEqual(schedule.path, ["Contract1", "Contract2", "Contract3"])

    def test_simple_sequence_with_gaps(self):
        contracts = [
            Contract("Contract1", 0, 5, 10),
            Contract("Contract2", 6, 7, 3),
            Contract("Contract3", 20, 3, 8)
        ]
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 21)
        self.assertEqual(schedule.path, ["Contract1", "Contract2", "Contract3"])
    
    def test_simple_superposition(self):
        contracts = [
            Contract("Contract1", 0, 5, 10),
            Contract("Contract2", 4, 7, 3),
            Contract("Contract3", 12, 3, 8)
        ]
        schedule = calculate_optimal_schedule(contracts)
        self.assertEqual(schedule.income, 18)
        self.assertEqual(schedule.path, ["Contract1", "Contract3"])
