import unittest
from unittest.mock import patch, mock_open
from serpents_hand_toolkit.utils import backup_current_source, rewrite_own_code

class TestUtils(unittest.TestCase):
    @patch("serpents_hand_toolkit.utils.os.path.abspath")
    @patch("serpents_hand_toolkit.utils.os.path.exists")
    @patch("serpents_hand_toolkit.utils.open", new_callable=mock_open)
    def test_backup_current_source(self, mock_open, mock_exists, mock_abspath):
        mock_abspath.return_value = "/path/to/script.py"
        mock_exists.return_value = False
        backup_current_source("/backup/dir")
        mock_open.assert_called()

    @patch("serpents_hand_toolkit.utils.os.path.abspath")
    @patch("serpents_hand_toolkit.utils.open", new_callable=mock_open)
    def test_rewrite_own_code(self, mock_open, mock_abspath):
        mock_abspath.return_value = "/path/to/script.py"
        rewrite_own_code("This is a patch note")
        mock_open.assert_called()

if __name__ == '__main__':
    unittest.main()