from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

# Create a function to initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS form_data
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 email TEXT,
                 message TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS coupon_data
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 coupon INTEGER)''')
    conn.commit()
    conn.close()

# Call the init_db function to create the database and table
init_db()

# Route to handle form submission

# Route to handle form submission
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Read the Excel sheet data
        excel_data = pd.read_excel('data.xlsx')

        # Check if the data already exists in the Excel sheet
        matching_data = excel_data[(excel_data['name'] == name) & (excel_data['email'] == email)]

        if  matching_data.empty:
            return render_template('invalid.html')
        else:
            # Add the data to the database
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('INSERT INTO form_data (name, email, message) VALUES (?, ?, ?)', (name, email, message))
            conn.commit()
            conn.close()

            return render_template('success.html')

    return render_template('index.html')

    
    # Route to display the database content
@app.route('/data')
def data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM form_data')
    data = c.fetchall()

    # Find duplicate entries based on name and email
    duplicates = set()
    unique_data = []
    for row in data:
        if (row[1], row[2]) in duplicates:
            duplicates.add((row[1], row[2]))
        else:
            unique_data.append(row)

    conn.close()

    return render_template('data.html', data=unique_data, duplicates=duplicates)


# Route to clear the database
@app.route('/clear', methods=['GET'])
def clear_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM form_data')
    conn.commit()
    conn.close()
    return "Database cleared successfully"

@app.route('/final', methods=['GET','POST'])
def final_coupon():
    # if request.method == 'POST':
    #     coupon = request.form['coupon']
    return render_template("final.html")

# Run the Flask application
if __name__ == '__main__':
    app.run(port=2020)
