from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from time import sleep
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = '192.168.0.170'
app.config['MQTT_BROKER_PORT'] = 1883

socketio = SocketIO(app)
mqtt = Mqtt(app)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("connected to broker")
    sleep(1)
    mqtt.subscribe('client/0')
    mqtt.subscribe('client/1')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    received_message_json = message.payload.decode()
    received_temp = json.loads(received_message_json)["temp"]
    if message.topic == "client/0":
        socketio.emit('temp_living_room', received_temp)
    elif message.topic == "client/1":
        socketio.emit('temp_bedroom', received_temp)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)