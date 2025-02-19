import logging
import os
import subprocess
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("serpents_hand_toolkit.log"),
                              logging.StreamHandler()])

def backup_current_source(backup_dir):
    cf = os.path.abspath(sys.argv[0])
    if not os.path.exists(backup_dir): os.makedirs(backup_dir)
    base = os.path.basename(cf)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{os.path.splitext(base)[0]}_backup_{ts}.py"
    backup_path = os.path.join(backup_dir, backup_name)
    try:
        with open(cf, "r") as src:
            code = src.read()
        with open(backup_path, "w") as dst:
            dst.write(code)
        logging.info(f"Backup => {backup_path}")
    except Exception as e:
        logging.error(f"backup error => {e}")

def rewrite_own_code(patch_text):
    cf = os.path.abspath(sys.argv[0])
    try:
        with open(cf, "r") as f:
            orig = f.read()
        patched = orig + f"\n# Self patch note => {patch_text}"
        with open(cf, "w") as f:
            f.write(patched)
        logging.info("Source code patched successfully.")
    except Exception as e:
        logging.error(f"rewriting error => {e}")