import csv
import json
from datetime import datetime

from Config.env_vars import MAX_SUCCESSES_PER_DAY, SUCCESS_TIME_THRESHOLD


class FlightsManager:
    def __init__(self, csv_file='flights.csv'):
        self.csv_file = csv_file
        self.flights_info = {}
        self.determine_flights_status()

    def determine_flights_status(self, new_flights=None):
        # Read the input file and store the flights in a list of dictionaries
        flights = []
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            flights = list(reader)

        if new_flights and new_flights[0]:
            for flight in new_flights:
                # Check if flight id not exist
                if flight.flight_ID not in self.flights_info.keys():
                    flight = {"flight ID": flight.flight_ID, "Arrival": flight.Arrival,
                              "Departure": flight.Departure, "success": ""}
                    flights.append(flight)
        # Sort the flights by arrival time
        flights.sort(key=lambda flight: flight['Arrival'])

        # Initialize the success count to zero
        success_count = 0

        # Calculate the success for each flight
        for flight in flights:
            # clear previous status
            flight['success'] = ''

            # Convert the arrival and departure times to datetime objects
            arrival_time = datetime.strptime(flight['Arrival'], '%H:%M')
            departure_time = datetime.strptime(flight['Departure'], '%H:%M')

            # Calculate the time difference between the arrival and departure times
            time_diff = (departure_time - arrival_time).total_seconds() // 60

            # Check if the time difference is greater than or equal to the success time threshold
            # And the maximum number of successes per day has been reached
            if time_diff >= SUCCESS_TIME_THRESHOLD and success_count < MAX_SUCCESSES_PER_DAY:
                # Update the success count and set the success flag for the flight
                success_count += 1
                flight['success'] = 'success'
            else:
                # Set the fail flag for the flight
                flight['success'] = 'fail'

        self.flights_info = {flight['flight ID']: flight for flight in flights}
        # Write the flights with success to the output file
        with open(self.csv_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['flight ID', 'Arrival', 'Departure', 'success'])
            writer.writeheader()
            for flight in flights:
                writer.writerow(flight)

        return f'Flights file has been updated!'

    def get_flight_info(self, flight_id):
        try:
            return self.flights_info[flight_id]
        except Exception as e:
            return f'Flight {flight_id} Not found!'
