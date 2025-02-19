import unittest
from serpents_hand_toolkit.image_downloader import download_image
import os

class TestImageDownloader(unittest.TestCase):
    def test_download_image(self):
        url = "https://example.com/image.png"
        images_dir = "./test_images"
        os.makedirs(images_dir, exist_ok=True)
        result = download_image(url, images_dir)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(images_dir, "image.png")))

if __name__ == '__main__':
    unittest.main()