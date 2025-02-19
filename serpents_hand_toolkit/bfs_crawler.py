import time
import csv
import logging

def minimal_bfs_scrape(base_url, search_term, max_pages):
    """Perform a minimal BFS web scrape."""
    logging.info(f"Starting BFS scrape on {base_url} with search term '{search_term}' for {max_pages} pages")
    discovered = []
    for i in range(max_pages):
        discovered.append(f"{base_url}?q={search_term}&page={i+1}")
        time.sleep(0.3)
    logging.info(f"BFS scrape completed with {len(discovered)} pages discovered")
    return discovered

def save_bfs_results(discovered, output_file="bfs_search_results.csv"):
    """Save BFS results to a CSV file."""
    logging.info(f"Saving BFS results to {output_file}")
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as cf:
            w = csv.writer(cf)
            w.writerow(["listing_url"])
            for d in discovered:
                w.writerow([d])
        logging.info(f"BFS results saved successfully to {output_file}")
    except Exception as e:
        logging.error(f"Error saving BFS results: {e}")