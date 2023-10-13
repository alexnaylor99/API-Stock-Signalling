import unittest

# Import the function you want to test
from main import calculate_7_day_average

class TestCalculate7DayAverage(unittest.TestCase):
    def test_calculate_7_day_average(self):
        # Test case 1: Test case with seven figures
        test_stock_data_1 = [100.0, 110.0, 95.0, 105.0, 112.0, 108.0, 98.0]
        expected_average_1 = 104.57  # Rounded to two decimal places

        result_1 = calculate_7_day_average(test_stock_data_1)
        self.assertAlmostEqual(result_1, expected_average_1, places=2)

        # Test case 2: Test case with eight figures
        test_stock_data_2 = [50.0, 60.0, 55.0, 70.0, 65.0, 62.0, 58.0, 50.0]
        expected_average_2 = 60.00  # Rounded to two decimal places

        result_2 = calculate_7_day_average(test_stock_data_2)
        self.assertAlmostEqual(result_2, expected_average_2, places=2)

if __name__ == '__main__':
    unittest.main()

