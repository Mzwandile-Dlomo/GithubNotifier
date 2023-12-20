import unittest
from unittest.mock import patch
from github_activity_notifier import get_github_activity

class TestNotificationApp(unittest.TestCase):

    @patch('requests.get')
    def test_get_github_activity_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'type': 'IssuesEvent'}]  # Replace with your actual test data
        mock_get.return_value = mock_response

        # Call the function with test data
        result = get_github_activity('owner', 'repo')

        # Assert that the function returns the expected result
        self.assertEqual(result, [{'type': 'IssuesEvent'}])

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with('https://api.github.com/repos/owner/repo/events')

    @patch('requests.get')
    def test_get_github_activity_failure(self, mock_get):
        # Mock the requests.get function to return a failed response
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Call the function with test data
        result = get_github_activity('owner', 'repo')

        # Assert that the function returns None for a failed response
        self.assertIsNone(result)

        # Assert that requests.get was called with the correct URL
        mock_get.assert_called_once_with('https://api.github.com/repos/owner/repo/events')

if __name__ == '__main__':
    unittest.main()
