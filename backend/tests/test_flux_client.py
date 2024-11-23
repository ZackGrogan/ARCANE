import unittest
from unittest.mock import patch, Mock
from io import BytesIO
from backend.ai_services.flux import FLUXClient, AIServiceError, Image

class TestFLUXClient(unittest.TestCase):
    def setUp(self):
        self.flux_client = FLUXClient()

    @patch('backend.ai_services.flux.requests.post')
    def test_generate_profile_picture_success(self, mock_post):
        # Mock the API response
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.json.return_value = {'image_url': 'http://example.com/image.jpg'}
        mock_post.return_value = mock_response

        # Call the method
        image_url = self.flux_client.generate_profile_picture('A brave knight')

        # Assertions
        self.assertEqual(image_url, 'http://example.com/image.jpg')
        mock_post.assert_called_once_with(
            'https://api.flux.com/generate-image',
            json={'prompt': 'A brave knight'},
            headers=self.flux_client.headers,
            timeout=30
        )

    @patch('backend.ai_services.flux.requests.get')
    def test_download_and_process_image_success(self, mock_get):
        # Mock the image response
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_response.content = b'fake_image_data'
        mock_get.return_value = mock_response

        # Mock Image.open
        with patch('backend.ai_services.flux.Image.open') as mock_open:
            mock_image = Mock()
            mock_open.return_value = mock_image
            # Ensure convert returns the same mock_image instance
            mock_image.convert.return_value = mock_image
            # Ensure resize returns the same mock_image instance
            mock_image.resize.return_value = mock_image

            # Explicitly mock the save method
            mock_image.save = Mock()

            # Call the method
            save_path = 'media/npc_test_portrait.jpg'
            result_path = self.flux_client.download_and_process_image('http://example.com/image.jpg', save_path)

            # Assertions
            self.assertEqual(result_path, save_path)
            mock_get.assert_called_once_with('http://example.com/image.jpg', timeout=30)

            # Retrieve the call arguments to Image.open
            args, kwargs = mock_open.call_args

            # Assert that the first argument is a BytesIO object
            self.assertIsInstance(args[0], BytesIO)

            # Read the content from the BytesIO object
            image_content = args[0].getvalue()

            # Assert that the content matches the fake image data
            self.assertEqual(image_content, b'fake_image_data')

            mock_image.convert.assert_called_once_with('RGB')
            mock_image.resize.assert_called_once_with((512, 512), Image.LANCZOS)
            mock_image.save.assert_called_once_with(save_path, format='JPEG', quality=85)

if __name__ == '__main__':
    unittest.main()
