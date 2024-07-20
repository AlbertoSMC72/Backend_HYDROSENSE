import serial
import json
import pika
import numpy as np
import datetime
from scipy.fft import fft

# Configuración del puerto serie
serial_port = '/dev/ttyUSB0'
baud_rate = 115200

# Configuración de RabbitMQ
amqp_options = {
    'hostname': '34.200.119.111',
    'port': 5672,
    'username': 'guest',
    'password': 'guest'
}

# Variables globales
totalLiters = 0

# Función para enviar mensajes a RabbitMQ
def send_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=amqp_options['hostname'],
        port=amqp_options['port'],
        credentials=pika.PlainCredentials(
            amqp_options['username'],
            amqp_options['password']
        )
    ))
    channel = connection.channel()
    channel.queue_declare(queue='data', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='data',
                          body=message)
    connection.close()

# Leer datos del puerto serie
ser = serial.Serial(serial_port, baud_rate)

# Buffer para datos del MPU6050
accel_x = []
accel_y = []
accel_z = []

while True:
    try:
        line = ser.readline().decode('utf-8').rstrip()
        data = json.loads(line)
        
        # Actualizar totalLiters
        if 'flow_rate' in data:
            totalLiters += data['flow_rate'] / 60
            data['total_liters'] = totalLiters
        
        # Procesar datos del MPU6050
        if 'acceleration_x' in data and 'acceleration_y' in data and 'acceleration_z' in data:
            print(f"Accel: {data['acceleration_x']}, {data['acceleration_y']}, {data['acceleration_z']}")
            accel_x.append(data['acceleration_x'])
            accel_y.append(data['acceleration_y'])
            accel_z.append(data['acceleration_z'])
            
            # Mantener el tamaño del buffer
            if len(accel_x) > 100:
                accel_x.pop(0)
                accel_y.pop(0)
                accel_z.pop(0)
            
            # Realizar la FFT cuando hay suficientes datos
            if len(accel_x) == 100:
                fft_x = fft(accel_x)
                fft_y = fft(accel_y)
                fft_z = fft(accel_z)
                
                # Detectar vibraciones (ejemplo simple: detectar picos en la FFT)
                vibration_x = np.abs(fft_x).max()
                vibration_y = np.abs(fft_y).max()
                vibration_z = np.abs(fft_z).max()
                
                data['vibration_x'] = vibration_x
                data['vibration_y'] = vibration_y
                data['vibration_z'] = vibration_z
        # Crear mensaje con solo los datos relevantes
        relevant_data = {
            "date": datetime.datetime.now().isoformat(),
            "data": {
                'temperature': data.get('temperature', None),
                'flow_rate': data.get('flow_rate', None),
                'total_liters': data.get('total_liters', None),
                'vibration_x': data.get('vibration_x', None),
                'vibration_y': data.get('vibration_y', None),
                'vibration_z': data.get('vibration_z', None)
            },
            "engine_ref_data": 1
        }

        message = json.dumps(relevant_data)
        send_to_queue(message)
        print(f"Sent: {message}")
    except Exception as e:
        print(f"Error: {e}")
