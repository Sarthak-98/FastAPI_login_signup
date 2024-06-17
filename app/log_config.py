import logging
import os

logs_folder = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(logs_folder, exist_ok=True)
log_file = os.path.join(logs_folder, 'error.log')

logging.basicConfig(filename=log_file, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Optionally, add more log handlers if needed
# Example:
# log_handler = logging.StreamHandler()
# log_handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# log_handler.setFormatter(formatter)
# logging.getLogger().addHandler(log_handler)