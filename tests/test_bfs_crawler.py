import unittest
from serpents_hand_toolkit.bfs_crawler import minimal_bfs_scrape

class TestBFSCrawler(unittest.TestCase):
    def test_bfs_scrape(self):
        result = minimal_bfs_scrape("https://example.com", "test", 2)
        self.assertEqual(len(result), 2)
        self.assertIn("https://example.com?q=test&page=1", result)
        self.assertIn("https://example.com?q=test&page=2", result)

if __name__ == '__main__':
    unittest.main()