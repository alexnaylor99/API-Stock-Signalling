import unittest
from unittest.mock import patch, Mock
import price_alert_utils

class TestPriceAlertUtils(unittest.TestCase):
    
    @patch("price_alert_utils.requests.get")
    def test_fetch_price_and_avg_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = [
            {"close": 100},
            {"close": 105},
            {"close": 110},
            {"close": 115},
            {"close": 120},
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        today_price, avg_7_day = price_alert_utils.fetch_price_and_avg("AAPL", "https://fakeurl.com", "fake_key")
        self.assertEqual(today_price, 120)
        self.assertEqual(avg_7_day, 107.5)

    @patch("price_alert_utils.requests.post")
    def test_notify_ifttt_success(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = price_alert_utils.notify_ifttt("fake_webhook_key", "test_event")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()

