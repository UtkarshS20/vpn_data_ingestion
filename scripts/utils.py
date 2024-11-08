import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import requests

load_dotenv()


def fetch_cidr_ranges(github_url):
    """
    Fetches CIDR ranges from a specified GitHub URL.
    
    Parameters:
        github_url (str): The URL to the GitHub raw file containing CIDR ranges.
        
    Returns:
        list: A list of CIDR ranges.
    """
    try:
        response = requests.get(github_url)
        response.raise_for_status()
        cidr_ranges = [line.strip() for line in response.text.splitlines() if line.strip()]
        if not cidr_ranges or not all('/' in cidr for cidr in cidr_ranges):
            raise ValueError("The content retrieved does not match expected CIDR format.")
        return cidr_ranges
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error fetching CIDR ranges: {e}")
        raise


def create_connection():
    """
    Create a database connection.
    
    Returns:
        connection: MySQL database connection object
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


def insert_cidr_range(connection, cidr_range):
    """
    Attempt to insert a CIDR range into the database.
    
    Parameters:
        connection: MySQL database connection object
        cidr_range (str): The CIDR range to insert
    """
    insert_query = "INSERT INTO cidr_ranges (date_added, cidr_range) VALUES (%s, %s)"
    date_added = datetime.now().date()
    values = (date_added, cidr_range)

    with connection.cursor() as cursor:
        try:
            cursor.execute(insert_query, values)
            connection.commit()
            print(f"Inserted: {cidr_range}")
        except mysql.connector.IntegrityError:
            print(f"Already exists: {cidr_range}")


def log_execution(connection, status, error_message=None):
    """Log execution status in the database."""
    log_query = "INSERT INTO execution_logs (execution_date, status, error_message) VALUES (%s, %s, %s)"
    execution_date = datetime.now()
    values = (execution_date, status, error_message)

    with connection.cursor() as cursor:
        cursor.execute(log_query, values)
        connection.commit()
