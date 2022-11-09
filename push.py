
import time
import datetime
import requests
import sensors

NOTIFY_INTERVAL = 1 * 60  # minimum interval for consecutive notifications (seconds)
NOTIFY_THRESHOLD = 30  # notify if above it (degree Celsius)
NOTIFY_DELAY = 15  # duration of initial silent period (seconds)
KEY = "xxxxxxxxxxxxxx"  # NEED TO EDIT THIS!

sen = sensors.SoilTemperatureSensor()


def main() -> None:
    initial_value = sen.read()
    max_value = initial_value
    min_value = initial_value

    # initialize last notified time to reflect initial silent period
    last_notify_time = datetime.datetime.now() - datetime.timedelta(seconds=NOTIFY_INTERVAL - NOTIFY_DELAY)

    while True:
        value = sen.read()

        print(f"Current value: {value:0.1f}, max: {max_value:0.1f}, min: {min_value:0.1f}, at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # notify if the value is above the threshold and the elapsed time since the last time is more than the interval
        if value > NOTIFY_THRESHOLD and (datetime.datetime.now() - last_notify_time).total_seconds() > NOTIFY_INTERVAL:
            send_pushnotification(value)
            last_notify_time = datetime.datetime.now()

        if value > max_value+0.1:
            max_value = value
            print(f"New max value: {max_value: 0.1f}")
        if value < min_value-0.1:
            min_value = value
            print(f"New min value: {min_value: 0.1f}")

        time.sleep(1)


def send_pushnotification(temp: float) -> None:
    msg = f"Temperature is {value:0.1f}°C"
    
    # send to simplepush.io
    requests.post(f"https://api.simplepush.io/send", data={"title": "Temperature warning", "msg": msg, "key": KEY})


if __name__ == "__main__":
    main()


