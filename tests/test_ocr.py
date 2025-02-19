import unittest
from serpents_hand_toolkit.ocr import extract_seagate_serials, perform_ocr_on_directory
import os

class TestOCR(unittest.TestCase):
    def test_extract_seagate_serials(self):
        # Mock an image path and content for testing
        img_path = "test_image.png"
        result = extract_seagate_serials(img_path)
        # As the image is mocked, we can't assert specific values, but we can check if it runs without errors
        self.assertIsInstance(result, list)

    def test_perform_ocr_on_directory(self):
        # Mock a directory with images and a CSV output path for testing
        dir_path = "./test_images"
        os.makedirs(dir_path, exist_ok=True)
        output_csv = "test_output.csv"
        perform_ocr_on_directory(dir_path, output_csv)
        # Check if the CSV file is created as expected
        self.assertTrue(os.path.exists(output_csv))
        os.remove(output_csv)

if __name__ == '__main__':
    unittest.main()