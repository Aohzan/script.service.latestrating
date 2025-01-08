import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from resources.lib.rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def setUp(self):
        self.rate_limiter = RateLimiter(calls_per_second=2)

    @patch('resources.lib.rate_limiter.datetime')
    @patch('resources.lib.rate_limiter.xbmc')
    def test_rate_limiting(self, mock_xbmc, mock_datetime):
        # Set up mock datetime
        now = datetime.now()
        mock_datetime.now.side_effect = [
            now,
            now + timedelta(milliseconds=100),
            now + timedelta(milliseconds=200),
            now + timedelta(milliseconds=300)
        ]

        # First two calls should not wait
        self.rate_limiter.wait_for_token('test_source')
        self.rate_limiter.add_call('test_source')
        self.rate_limiter.wait_for_token('test_source')
        self.rate_limiter.add_call('test_source')

        # Third call within the same second should wait
        self.rate_limiter.wait_for_token('test_source')
        mock_xbmc.sleep.assert_called_once()

    def test_multiple_sources(self):
        # Different sources should be rate limited independently
        self.rate_limiter.wait_for_token('source1')
        self.rate_limiter.add_call('source1')
        self.rate_limiter.wait_for_token('source1')
        self.rate_limiter.add_call('source1')

        # This should not wait as it's a different source
        self.rate_limiter.wait_for_token('source2')
        self.rate_limiter.add_call('source2')

if __name__ == '__main__':
    unittest.main() 