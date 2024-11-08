# # scripts/insert_yesterday_ranges.py
# import os
# from utils import create_connection
# from mysql.connector import IntegrityError
# from datetime import datetime, timedelta

# # Path to your text file
# RANGES_FILE = os.path.join(os.path.dirname(__file__), '../data/txt/vpn-or-datacenter-ipv4-ranges-04-11-24.txt')

# def insert_cidr_ranges_from_file():
#     connection = create_connection()
#     if connection is not None:
#         with open(RANGES_FILE, 'r') as file:
#             for line in file:
#                 cidr_range = line.strip()
#                 if cidr_range:  # Ensure it's not an empty line
#                     insert_cidr_range(connection, cidr_range)
        
#         connection.close()
#     else:
#         print("Failed to create database connection.")


# def insert_cidr_range(connection, cidr_range):
#     """
#     Insert a CIDR range into the database with yesterday's date.
    
#     Parameters:
#         connection: MySQL database connection object
#         cidr_range (str): The CIDR range to insert
#     """
#     yesterday_date = (datetime.now() - timedelta(days=1)).date()  # Get yesterday's date
#     insert_query = "INSERT INTO cidr_ranges (date_added, cidr_range) VALUES (%s, %s)"
#     values = (yesterday_date, cidr_range)

#     with connection.cursor() as cursor:
#         try:
#             cursor.execute(insert_query, values)
#             connection.commit()
#             print(f"Inserted: {cidr_range} with date {yesterday_date}")
#         except IntegrityError:
#             print(f"Already exists: {cidr_range}")


# if __name__ == "__main__":
#     insert_cidr_ranges_from_file()
