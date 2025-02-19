"""
Serpents Hand Toolkit v2.2 (c) 2025 Kenneth Owen
Licensed under the Proprietary License
Date: February 19, 2025

Changelog:
- Modularized the codebase for better maintainability.
- Added logging for better error tracking and debugging.
- Implemented unit tests and set up continuous integration using GitHub Actions.
- Formatted code using Black and added linting with flake8.
- Enhanced the Spyder plugin.
- Improved security practices.
"""

import logging
from gui import SerpentsHandToolkit
from ocr import perform_ocr_in_browser

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("serpents_hand_toolkit.log"),
                              logging.StreamHandler()])

def main():
    """Launch the GUI application."""
    logging.info("Starting Serpents Hand Toolkit v2.2")
    
    # Example usage of perform_ocr_in_browser
    search_term = "laptops"
    search_url = "https://www.example.com/search"
    listing_urls = [
        "https://www.example.com/item1",
        "https://www.example.com/item2"
    ]
    perform_ocr_in_browser(search_term, search_url, listing_urls)
    
    app = SerpentsHandToolkit()
    app.mainloop()
    logging.info("Exiting Serpents Hand Toolkit")

if __name__ == "__main__":
    main()