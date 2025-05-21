from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="dental_hospital"
)
cursor = conn.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM treatments")
    treatments = cursor.fetchall()
    return render_template('index.html', treatments=treatments)

@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    patient_name = request.form['patient_name']
    treatment_id = request.form['treatment_id']
    
    cursor.execute("INSERT INTO receipts (patient_name, treatment_id) VALUES (%s, %s)", (patient_name, treatment_id))
    conn.commit()
    
    cursor.execute("""
        SELECT r.id, r.patient_name, t.treatment_name, t.price, r.date
        FROM receipts r
        JOIN treatments t ON r.treatment_id = t.id
        ORDER BY r.id DESC LIMIT 1
    """)
    receipt = cursor.fetchone()
    
    return render_template('receipt.html', receipt=receipt)

if __name__ == '__main__':
    app.run(debug=True)
