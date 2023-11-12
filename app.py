# app.py

from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__, template_folder='static')

# Route to serve the static HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch data from SQLite database
@app.route('/api/data')
def get_data():
    try:
        print("FETCHING DATA")
        conn = sqlite3.connect('councilBotDatabase.db')  # Replace 'data.db' with your actual database file
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questions_summaries')  # Replace 'your_table_name' with your actual table name
        data = cursor.fetchall()
        conn.close()

        data = [(str(item[0]), str(item[1])) for item in data]

        return jsonify(data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
