import os
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def download_image(url, images_dir):
    """Download a single image from a URL."""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        im = Image.open(resp.raw)
        base = os.path.basename(url)
        if not os.path.splitext(base)[1]:
            base += ".png"
        path = os.path.join(images_dir, base)
        im.save(path)
        logging.info(f"Image downloaded and saved to {path}")
        return True
    except Exception as e:
        logging.error(f"Download error for {url}: {e}")
        return False

def download_images(image_urls, output_dir, max_workers=5, progress_callback=None):
    """Download multiple images concurrently."""
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    total = len(image_urls)
    completed = 0
    success = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        fut_map = {executor.submit(download_image, url, images_dir): url for url in image_urls}
        for fut in as_completed(fut_map):
            completed += 1
            if fut.result():
                success += 1
            if progress_callback:
                progress_callback(completed, total)
    logging.info(f"Downloaded {success} out of {total} images successfully")
    return completed, success