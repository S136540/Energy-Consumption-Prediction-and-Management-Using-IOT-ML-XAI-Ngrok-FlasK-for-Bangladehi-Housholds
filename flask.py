# import requests
# from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO
# import plotly
# import plotly.graph_objs as go
# import json
# from model import predict_power, get_future_data
# import pandas as pd
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from threading import Thread
# import time
# import serial
#
# app = Flask(_name_)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)
#
# sensor_data = {
#     "voltage": 0,
#     "current": 0
# }
#
# # Email alert function
# def send_alert_email(voltage, current):
#     sender_email = "abdulgofferbepari@gmail.com"
#     receiver_email = "arnmollah@gmail.com"
#     password = "your_email_password"  # Use environment variable in production
#
#     message = MIMEMultipart("alternative")
#     message["Subject"] = "Alert: Sensor Data Exceeded Threshold"
#     message["From"] = sender_email
#     message["To"] = receiver_email
#
#     text = f"""\
#     Alert!
#     Voltage: {voltage}V
#     Current: {current}A
#     The sensor data has exceeded the defined threshold."""
#     part = MIMEText(text, "plain")
#     message.attach(part)
#
#     try:
#         server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message.as_string())
#         server.close()
#         print("Email sent successfully!")
#     except Exception as e:
#         print(f"Error sending email: {e}")
#
# # Function to log sensor data to Excel
# def log_sensor_data_to_excel(voltage, current):
#     file_path = 'sensor_data_log.xlsx'
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     df = pd.DataFrame({
#         'Time': [current_time],
#         'Voltage': [voltage],
#         'Current': [current]
#     })
#
#     try:
#         with pd.ExcelWriter(file_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
#             df.to_excel(writer, index=False, header=writer.sheets['Sheet1'].max_row == 1, startrow=writer.sheets['Sheet1'].max_row)
#     except FileNotFoundError:
#         df.to_excel(file_path, index=False)
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json
#     date = data['date']
#     avg_voltage = float(data['avg_voltage'])
#     avg_intensity = float(data['avg_intensity'])
#     interval = data['interval']
#
#     predicted_power = predict_power(avg_voltage, avg_intensity)
#     future_data = get_future_data(date, interval, avg_voltage, avg_intensity)
#
#     trace = go.Scatter(x=[d['date'] for d in future_data], y=[d['predicted_power'] for d in future_data],
#                        mode='lines+markers', name='Predicted Power')
#     layout = go.Layout(title='Power Consumption Prediction', xaxis={'title': 'Date'}, yaxis={'title': 'Power (kW)'})
#     graphJSON = json.dumps([trace], cls=plotly.utils.PlotlyJSONEncoder)
#
#     return jsonify(predicted_power=predicted_power, graph=json.loads(graphJSON))
#
# @app.route('/sensor', methods=['POST'])
# def sensor():
#     global sensor_data
#     data = request.json
#     sensor_data['voltage'] = data['voltage']
#     sensor_data['current'] = data['current']
#
#     log_sensor_data_to_excel(sensor_data['voltage'], sensor_data['current'])
#
#     if sensor_data['voltage'] > 223 or sensor_data['current'] > 0.05:
#         send_alert_email(sensor_data['voltage'], sensor_data['current'])
#
#     socketio.emit('sensor_update', sensor_data)
#     return jsonify(status='success')
#
# @app.route('/get_sensor_data', methods=['GET'])
# def get_sensor_data():
#     return jsonify(sensor_data)
#
# def read_from_serial():
#     serial_port = 'COM3'  # Update this to match your Arduino's port
#     baud_rate = 250000
#     ser = serial.Serial(serial_port, baud_rate)
#
#     while True:
#         try:
#             if ser.in_waiting > 0:
#                 line = ser.readline().decode('utf-8').strip()
#                 print(f"Received data: {line}")
#
#                 data = line.split('\t')
#                 voltage = float(data[0].split()[1])
#                 current = float(data[1].split()[1])
#
#                 sensor_data['voltage'] = voltage
#                 sensor_data['current'] = current
#
#                 socketio.emit('sensor_update', sensor_data)
#
#                 # Update the sensor data
#                 requests.post('http://127.0.0.1:5000/sensor', json={'voltage': voltage, 'current': current})
#
#         except Exception as e:
#             print(f"Error: {e}")
#
#         time.sleep(2)
#
# if _name_ == '_main_':
#     # Start the serial reading thread
#     Thread(target=read_from_serial).start()
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True
