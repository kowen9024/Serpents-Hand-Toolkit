import unittest
from unittest.mock import patch, MagicMock
from serpents_hand_toolkit.gui import SerpentsHandToolkit, CrawlerFrame, ImageDownloaderFrame, OCRFrame

class TestGUI(unittest.TestCase):
    def setUp(self):
        self.app = SerpentsHandToolkit()

    def test_initial_frame(self):
        self.assertIsInstance(self.app.frames["CrawlerFrame"], CrawlerFrame)
        self.assertIsInstance(self.app.frames["ImageDownloaderFrame"], ImageDownloaderFrame)
        self.assertIsInstance(self.app.frames["OCRFrame"], OCRFrame)

    @patch('serpents_hand_toolkit.gui.minimal_bfs_scrape')
    @patch('serpents_hand_toolkit.gui.save_bfs_results')
    def test_crawler_frame_bfs(self, mock_save_bfs, mock_bfs_scrape):
        mock_bfs_scrape.return_value = ["https://example.com"]
        frame = self.app.frames["CrawlerFrame"]
        frame.base_url_var.set("https://example.com")
        frame.search_var.set("test")
        frame.pages_var.set(1)
        frame.start_bfs()
        frame.controller.after(1000, frame.controller.quit)
        frame.controller.mainloop()
        mock_bfs_scrape.assert_called_once()
        mock_save_bfs.assert_called_once()

    @patch('serpents_hand_toolkit.gui.download_images')
    def test_image_downloader_frame(self, mock_download_images):
        mock_download_images.return_value = (1, 1)
        frame = self.app.frames["ImageDownloaderFrame"]
        frame.csv_file_var.set("test.csv")
        frame.out_dir_var.set(".")
        frame.start_download()
        frame.controller.after(1000, frame.controller.quit)
        frame.controller.mainloop()
        mock_download_images.assert_called_once()

    @patch('serpents_hand_toolkit.gui.perform_ocr_on_directory')
    def test_ocr_frame(self, mock_perform_ocr):
        mock_perform_ocr.return_value = None
        frame = self.app.frames["OCRFrame"]
        frame.folder_var.set(".")
        frame.csv_var.set("test_output.csv")
        frame.start_ocr()
        frame.controller.after(1000, frame.controller.quit)
        frame.controller.mainloop()
        mock_perform_ocr.assert_called_once()

if __name__ == '__main__':
    unittest.main()