import sqlite3
from prettytable import PrettyTable  # Optional, for nice table formatting

# Connect to the database (make sure this path is correct)
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Fetch all patient records
cursor.execute("SELECT id, name, age, gender, disease, prediction, risk_level, risk_probability, date_created FROM patient")
rows = cursor.fetchall()

# Display using pretty table (if prettytable is not installed, install with: pip install prettytable)
table = PrettyTable()
table.field_names = ["ID", "Name", "Age", "Gender", "Disease", "Prediction", "Risk Level", "Risk %", "Date"]

for row in rows:
    # Convert probability to percentage
    row = list(row)
    row[7] = f"{row[7]*100:.2f}%"
    table.add_row(row)

print(table)

# Close connection
conn.close()