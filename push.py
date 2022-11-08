
import time
import datetime
import requests
import sensors

NOTIFY_INTERVAL = 1 * 60  # only notify once in a minute
NOTIFY_THRESHOLD = 30  # above it then notify
NOTIFY_DELAY = 15  # initial no-notify period
KEY = "xxxxxxxxxxxxxx"  # NEED TO EDIT THIS!

sen = sensors.SoilTemperatureSensor()


def main() -> None:
    initial_value = sen.read()
    max_value = initial_value
    min_value = initial_value

    # initialize last notify time to reflect initial no-notify period
    last_notify_time = datetime.datetime.now() - datetime.timedelta(seconds=NOTIFY_INTERVAL - NOTIFY_DELAY)

    while True:
        value = sen.read()

        print(f"Current value: {value:0.1f}, max: {max_value:0.1f}, min: {min_value:0.1f}, at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # notify if the value is above the threshold and the last notify time is more than a certain interval ago
        if value > NOTIFY_THRESHOLD and (datetime.datetime.now() - last_notify_time).total_seconds() > NOTIFY_INTERVAL:
            send_pushnotification(f"Temperature is {value:0.1f}°C")
            last_notify_time = datetime.datetime.now()

        if value > max_value+0.1:
            max_value = value
            print(f"New max value: {max_value: 0.1f}")
        if value < min_value-0.1:
            min_value = value
            print(f"New min value: {min_value: 0.1f}")

        time.sleep(1)


def send_pushnotification(msg: str) -> None:
    # send to simplepush.io
    requests.post(f"https://api.simplepush.io/send", data={"title": "Temperature warning", "msg": msg, "key": KEY})


if __name__ == "__main__":
    main()


