import mysql.connector
from faker import Faker
import random
import string
import time

# Database connection details
username = 'doadmin'
password = 'AVNS_09AYyWLmRSksoqMYzTK'
host = 'db-mysql-nyc1-53719-do-user-2491287-0.b.db.ondigitalocean.com'
port = 25060
database = 'flightdatabase'
sslmode = 'REQUIRED'

# Connect to the MySQL server (without specifying the database)
cnx = mysql.connector.connect(user=username, password=password, host=host, port=port)

# Create a cursor object
cursor = cnx.cursor()

# Create the database if it does not exist
cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database))

# Select the database
cursor.execute("USE {}".format(database))

print ("Connected to database")
# Create a cursor object
cursor = cnx.cursor()

# Create tables
cursor.execute("SHOW TABLES LIKE 'Airlines'")
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE Airlines (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), country VARCHAR(255), iata_code VARCHAR(3), icao_code VARCHAR(4), callsign VARCHAR(255), founded_year INT, ceased_operation_year INT)")
cursor.execute("SHOW TABLES LIKE 'Airports'")
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE Airports (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), location VARCHAR(255), country VARCHAR(255), iata_code VARCHAR(3), icao_code VARCHAR(4), latitude DECIMAL(9,6), longitude DECIMAL(9,6), elevation_ft INT, timezone VARCHAR(255))")
cursor.execute("SHOW TABLES LIKE 'Flights'")
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE Flights (id INT AUTO_INCREMENT PRIMARY KEY, airline_id INT, departure_airport_id INT, arrival_airport_id INT, departure_time TIME, arrival_time TIME, flight_duration TIME, flight_number VARCHAR(255), FOREIGN KEY (airline_id) REFERENCES Airlines(id), FOREIGN KEY (departure_airport_id) REFERENCES Airports(id), FOREIGN KEY (arrival_airport_id) REFERENCES Airports(id))")
cursor.execute("SHOW TABLES LIKE 'Passengers'")
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE Passengers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), birth_date DATE, nationality VARCHAR(255), passport_number VARCHAR(255), frequent_flyer_number VARCHAR(255), email VARCHAR(255), phone_number VARCHAR(255))")
cursor.execute("SHOW TABLES LIKE 'Reservations'")
if cursor.fetchone() is None:
    cursor.execute("CREATE TABLE Reservations (id INT AUTO_INCREMENT PRIMARY KEY, flight_id INT, passenger_id INT, booking_date DATE, seat_number VARCHAR(255), class VARCHAR(255), price DECIMAL(10,2), FOREIGN KEY (flight_id) REFERENCES Flights(id), FOREIGN KEY (passenger_id) REFERENCES Passengers(id))")

print ("Created tables")
# Create a Faker instance
fake = Faker()

# Populate tables with large amounts of data
start_time = time.time()
for _ in range(1000):
    print("inserting airline and airport" + str(_) + "of 1000")
    cursor.execute("INSERT INTO Airlines (name, country, iata_code, icao_code, callsign, founded_year, ceased_operation_year) VALUES (%s, %s, %s, %s, %s, %s, %s)", (fake.company(), fake.country(), fake.lexify(text='???'), fake.lexify(text='????'), fake.catch_phrase(), fake.year(), fake.year()))
    cursor.execute("INSERT INTO Airports (name, location, country, iata_code, icao_code, latitude, longitude, elevation_ft, timezone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (fake.city(), fake.address(), fake.country(), fake.lexify(text='???'), fake.lexify(text='????'), fake.latitude(), fake.longitude(), fake.random_int(min=0, max=10000), fake.timezone()))

print ("populated airlines and airports")

for _ in range(1000000):
    print("inserting passenger" + str(_) + "of 1000000")
    cursor.execute("INSERT INTO Passengers (name, birth_date, nationality, passport_number, frequent_flyer_number, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s, %s)", (fake.name(), fake.date_of_birth(minimum_age=18, maximum_age=90), fake.country(), fake.bothify(text='????????##'), fake.bothify(text='????????##'), fake.email(), fake.phone_number()))

print ("populated passengers")

for _ in range(30000):
    print("inserting flight and reservation" + str(_) + "of 1000000")
    cursor.execute("INSERT INTO Flights (airline_id, departure_airport_id, arrival_airport_id, departure_time, arrival_time, flight_duration, flight_number) VALUES (%s, %s, %s, %s, %s, %s, %s)", (random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 1000), fake.time(), fake.time(), fake.time(), fake.bothify(text='??####')))
    cursor.execute("INSERT INTO Reservations (flight_id, passenger_id, booking_date, seat_number, class, price) VALUES (%s, %s, %s, %s, %s, %s)", (random.randint(1, 1000000), random.randint(1, 1000), fake.date_this_year(), fake.bothify(text='##?'), fake.random_element(elements=('Economy', 'Business', 'First')), fake.random_number(digits=4, fix_len=True)))

print ("populated flights and reservations")

# Commit the transaction
cnx.commit()

end_time = time.time()
total_time = end_time - start_time
print ("Populated tables in {} seconds".format(total_time))

# Close the connection
cnx.close()