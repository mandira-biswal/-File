import csv
from datetime import datetime, timedelta
import sys

def analyze_time_records(file_path):
    # Assumption: The CSV file has a header row and columns are in the same order as mentioned in the provided data.
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        
        # Dictionary to store employee data
        employees = {}

        for row in reader:
            employee_name = row['Employee Name']
            # time_in = datetime.strptime(row['Time'], '%m/%d/%Y %I:%M %p')
            if row['Time']:
                time_in = datetime.strptime(row['Time'], '%m/%d/%Y %I:%M %p')
            else:
                time_in = None

            time_out = datetime.strptime(row['Time Out'], '%m/%d/%Y %I:%M %p') if row['Time Out'] else None

            # If the employee is not in the dictionary, add them
            if employee_name not in employees:
                employees[employee_name] = {'positions': set(), 'work_days': set(), 'shifts': []}

            # Update position
            employees[employee_name]['positions'].add(row['Position ID'])

            # Check consecutive work days
            if time_in is not None:
                employees[employee_name]['work_days'].add(time_in.date())

            # Check time between shifts
            if employees[employee_name]['shifts']:
                last_shift_end = employees[employee_name]['shifts'][-1]['time_out']
                if last_shift_end is not None:
                    time_between_shifts = time_in - last_shift_end
                    if timedelta(hours=1) < time_between_shifts < timedelta(hours=10):
                        sys.stdout.write(f"{employee_name} has less than 10 hours between shifts.\n")

            # Check for long shifts
            if time_out and (time_out - time_in) > timedelta(hours=14):
                sys.stdout.write(f"{employee_name} worked for more than 14 hours in a single shift.\n")

            # Update shifts
            employees[employee_name]['shifts'].append({'time_in': time_in, 'time_out': time_out})

        # Check for employees who worked for 7 consecutive days
        for employee_name, data in employees.items():
            if len(data['work_days']) >= 7:
                sys.stdout.write(f"{employee_name} has worked for 7 consecutive days.\n")


# Provide the correct path to your Excel file
file_path = 'assignment_timecard.csv'
sys.stdout = open('output.txt', 'w')
analyze_time_records(file_path)

# Close the file
sys.stdout.close()