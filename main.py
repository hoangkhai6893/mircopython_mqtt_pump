
def sub_cb(topic, msg):
    global state
    print((topic, msg))
    if msg == b"on":
        led.value(1)
        state = msg
        # control_pumer('on')
    elif msg == b"off":
        led.value(0)
        state = msg
        # control_pumer('off')
    else:
        pass

def control_pumer(msg):
    if msg == 'on':
        led.value(1)
        pump.value(0)
        client.publish(topic_pub, msg)
    elif msg == 'off':
        led.value(0)
        pump.value(1)
        client.publish(topic_pub, msg)


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

#init data
last_message = 0
counter = 0
count_auto_pump = 0
count_status = 0
# set data value
time_delay_state = 5
time_watering_auto = 8
time_cycle_auto = 720
while True:
    try:
        led.value(0)
        client.check_msg()
        time_count_down = time_delay_state - (time.time() - last_message)

        if time_count_down <= 0:

            last_message = time.time()
            control_pumer('off')
            count_auto_pump = count_auto_pump + 1
            print("send msg")
            led.value(1)
            sleep(0.01)
        if state == b'on':
            time_delay_state = 1
            control_pumer('on')
        else:
            time_delay_state = 5
        if count_auto_pump > 300:
            count_auto_pump = 0
            if state == b'off':
                control_pumer('on')
                time.sleep(time_watering_auto)
                control_pumer('off')
        else:
            if state == b'on':
                count_status += 1
                if count_status >= 3:
                    count_auto_pump
                    count_status

    except OSError as e:
        restart_and_reconnect()
