import logging
import os
import datetime

# Create a directory for the logs if it doesn't exist
log_directory = "/home/cai/New/logs"
os.makedirs(log_directory, exist_ok=True)

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Define the log message format
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)

# Get the current date to create the log file name
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create the log file path with the current date as the filename
log_file = os.path.join(log_directory, f"{current_date}.log")

# Create the file handler with the log file path
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
