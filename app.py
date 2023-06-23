from flask import Flask, render_template, request
import sqlite3
import pandas as pd
import random
import string

app = Flask(__name__)

def generate_coupons(num):
    coupons = [num]
    for i in range(num):
        coupon = (random.choices(string.ascii_uppercase + string.digits, k=4))
        coupons.append(coupon)
    return coupons

# Create a function to initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS form_data
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 cpfno TEXT,
                 email TEXT,
                 num_coupons INTEGER)''')
    conn.commit()
    conn.close()

# Call the init_db function to create the database and table
init_db()

# Route to handle form submission

# Route to handle form submission
@app.route('/')
def main():
    return render_template("home.html")


@app.route('/coupon', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        cpfno = request.form['cpfno']
        email = request.form['email']
        num_coupons = request.form['num_coupons']

        n = int(num_coupons)

        # Read the Excel sheet data
        excel_data = pd.read_excel('data.xlsx')

        # Check if the data already exists in the Excel sheet
        # matching_data = excel_data[(excel_data['cpfno'] == cpfno) & (excel_data['email'] == email)]
        matching_data = excel_data[(excel_data['email'] == email)]

        if  matching_data.empty:
            return render_template('invalid.html')
        else:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('SELECT * FROM form_data WHERE cpfno=? AND email=?', (cpfno, email))
            stored_data = c.fetchone()
            conn.close()

            if stored_data:
                return render_template('already_filled.html')
            else:
                # Add the data to the database
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute('INSERT INTO form_data (name, cpfno, email, num_coupons) VALUES (?, ?, ?, ?)', (name, cpfno, email, num_coupons))

            conn.commit()
            # conn.close()

            coupons = generate_coupons(n)
            return render_template('success.html', coupons=coupons,cpfno=cpfno )



    return render_template('index.html')


#admin

@app.route('/admin')
def admin_access():
    return render_template('admin.html')



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




# Route to generate and store the number of coupons
# @app.route('/generate_coupon', methods=['GET','POST'])
# def generate_coupon():
#     if request.method == 'POST':
#         num_coupons = request.form['num_coupons']

#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()

#     # Get the total number of rows in the form_data table
#     # c.execute('SELECT COUNT(*) FROM form_data')
#     # total_rows = c.fetchone()[0]

#     # Check if the total number of rows has reached the limit (1500)
#     # if total_rows >= 1500:
#     #     return render_template('coupon_limit.html')

#     # Store the number of coupons in the database
#     c.execute('INSERT INTO form_data (num_coupons) VALUES (?)', (num_coupons))
#     conn.commit()
#     conn.close()

#     return render_template('data.html')




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




