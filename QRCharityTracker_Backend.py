from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
import csv

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
csv_data = None

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to upload the CSV
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_file.csv')
    try:
        file.save(file_path)
        print(f"File saved to: {file_path}")  # Debug log
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
    except Exception as e:
        print(f"Error saving file: {e}")  # Debug log
        return jsonify({'message': f'Error saving file: {str(e)}'}), 500


# Endpoint to update the CSV file
@app.route('/update_csv', methods=['POST'])
def update_csv():
    data = request.json
    rows = data.get('rows', [])

    if not rows:
        return jsonify({'message': 'No data provided to update'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, 'uploaded_file.csv')
    if not os.path.exists(file_path):
        return jsonify({'message': 'CSV file not found on the server'}), 404

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Status', 'Timestamp'])  # Write headers
            for row in rows:
                writer.writerow([row['name'], row['status'], row['timestamp']])

        return jsonify({'message': 'CSV updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating CSV: {str(e)}'}), 500



@app.route('/check_name', methods=['POST'])
def check_name():
    global csv_data
    if csv_data is None:
        return jsonify({"message": "No CSV uploaded yet!"}), 400

    name = request.json.get('name')
    if name in csv_data["Name"].values:
        return jsonify({"message": "Yes, it's in the list."}), 200
    else:
        return jsonify({"message": "No, it's not found."}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")