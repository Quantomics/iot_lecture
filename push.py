
import time
import datetime
import requests
import sensors

# only notify once in 5 minutes
NOTIFY_INTERVAL = 1 * 60
NOTIFY_THRESHOLD = 3
NOTIFY_DELAY = 15
KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

sen = sensors.SoilTemperatureSensor()

def getvalue() -> int:
    return 100


def main() -> None:
    initial_value = sen.read()
    max_value = initial_value
    min_value = initial_value

    # initialize last notify time as many years ago so that the first time the script runs, it will notify
    last_notify_time = datetime.datetime.now() - datetime.timedelta(seconds=NOTIFY_INTERVAL - NOTIFY_DELAY)

    while True:
        value = sen.read()

        print(f"Current value: {value:0.1f}, max: {max_value:0.1f}, min: {min_value:0.1f}, at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        # notify if the value is above the threshold and the last notify time is more than 5 minutes ago
        if value > max_value + NOTIFY_THRESHOLD and (datetime.datetime.now() - last_notify_time).total_seconds() > NOTIFY_INTERVAL:
            send_pushnotification(f"Temperature is {value:0.1f}°C")
            last_notify_time = datetime.datetime.now()

        if value > max_value:
            max_value = value
            print(f"New max value: {max_value}")
        if value < min_value:
            min_value = value
            print(f"New min value: {min_value}")

        time.sleep(1)


def send_pushnotification(msg: str) -> None:
    # send to simplepush.io
    requests.post(f"https://api.simplepush.io/send/", data={"title": "Temperature warning", "msg": msg, "key": KEY})


if __name__ == "__main__":
    main()



        time.sleep(1)


def send_pushnotification(msg: str) -> None:
    # send to simplepush.io
    requests.post(f"https://api.simplepush.io/send/", data={"title": "Temperature warning", "msg": msg, "key": KEY})


if __name__ == "__main__":
    main()


