import schedule
import time
from utils import fetch_cidr_ranges, create_connection, insert_cidr_range, log_execution
import yaml
import os

# Load configurations
config_path = os.path.join(os.path.dirname(__file__), '../configs/config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

GITHUB_URL = config['github_url']

def update_cidr_ranges():
    # Fetch CIDR ranges from GitHub
    try:
        cidr_ranges = fetch_cidr_ranges(GITHUB_URL)
        print(f"Fetched {len(cidr_ranges)} CIDR ranges.")
        
        connection = create_connection()
        if connection is not None:
            for cidr_range in cidr_ranges:
                insert_cidr_range(connection, cidr_range)
            log_execution(connection, status='success')
            connection.close()
        else:
            raise Exception("Database connection failed.")
    
    except Exception as e:
        # Log error in the database
        connection = create_connection()
        if connection is not None:
            log_execution(connection, status='failed', error_message=str(e))
            connection.close()
        print(f"Error: {e}")


# Schedule the job to run daily at --:--
schedule.every().day.at("10:04").do(update_cidr_ranges)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
