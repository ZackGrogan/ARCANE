import logging
import unittest
from unittest.mock import patch

class TestLogging(unittest.TestCase):
    @patch('logging.Logger.info')
    @patch('logging.Logger.error')
    def test_logging(self, mock_error, mock_info):
        logger = logging.getLogger('test_logger')
        logger.setLevel(logging.DEBUG)

        # Simulate info logging
        logger.info('This is an info message')
        mock_info.assert_called_with('This is an info message')

        # Simulate error logging
        logger.error('This is an error message')
        mock_error.assert_called_with('This is an error message')

if __name__ == '__main__':
    unittest.main()
