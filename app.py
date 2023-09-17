from flask import Flask,render_template,request
import csv
import pandas as pd

app = Flask(__name__)

csv_path='request.csv'

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/request')
def request():
	requests=[]
	with open(csv_path,'r') as file:
		reader=csv.reader(file)
		next(reader,None)
		for row in reader:
			if row[6] =='Pending':
				requests.append({
					"id": row[0],
					"course_type": row[1],
					"course_name": row[2],
					"duration": row[3],
					"mode": row[4],
					"team": row[5],
					"status": row[6],
				})
	return render_template('request.html',requests=requests)


@app.route('/approve_request/<int:request_id>')
def approve_request(request_id):
	with open(csv_path,'r') as file:
		reader = csv.reader(file)
		header=next(reader)
		rows = [header] + [row for i, row in enumerate(reader) if i != request_id]
		if 0 <= request_id < len(rows):
			rows[request_id][6] = "Approved"
	with open(csv_path,'w',newline='') as file:
		writer = csv.writer(file)
		writer.writerows(rows)
	return render_template('request.html')


@app.route('/block_request/<int:request_id>')
def block_request(request_id):
	with open(csv_path,'r') as file:
		reader = csv.reader(file)
		header=next(reader)
		rows = [header] + [row for i, row in enumerate(reader) if i != request_id]
		if 0 <= request_id < len(rows):
			rows[request_id][6] = "Blocked"
	with open(csv_path,'w',newline='') as file:
		writer = csv.writer(file)
		writer.writerows(rows)
	return render_template('request.html')

if __name__ == '__main__':
	app.run(debug=True)
