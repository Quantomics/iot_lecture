
import time
import datetime
import requests
import sensors

# only notify once in 5 minutes
NOTIFY_INTERVAL = 1 * 60
NOTIFY_THRESHOLD = 1
NOTIFY_DELAY = 15
KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

sen = sensors.SoilTemperatureSensor()

def getvalue() -> int:
    return 100


def main() -> None:
    initial_value = sen.read()
    max_value = initial_value
    min_value = initial_value
    mean_value = initial_value
    std_value = 0

    # initialize last notify time as many years ago so that the first time the script runs, it will notify
    last_notify_time = datetime.datetime.now() - datetime.timedelta(seconds=NOTIFY_INTERVAL - NOTIFY_DELAY)

    while True:
        value = getvalue()
        if value > max_value:
            max_value = value
            print(f"New max value: {max_value}")
        if value < min_value:
            min_value = value
            print(f"New min value: {min_value}")
        mean_value = (mean_value + value) / 2
        std_value = (std_value + (value - mean_value) ** 2) / 2
        zscore = (value - mean_value) / std_value

        print(f"Current value: {value}, max: {max_value}, min: {min_value}, mean: {mean_value}, std: {std_value}, zscore: {zscore}, at {datetime.datetime.now()}")
        # notify if the value is above the threshold and the last notify time is more than 5 minutes ago
        if zscore > NOTIFY_THRESHOLD and (datetime.datetime.now() - last_notify_time).total_seconds() > NOTIFY_INTERVAL:
            send_pushnotification(f"Temperature is {value:0.1f}°C")
            last_notify_time = datetime.datetime.now()
        time.sleep(1)


def send_pushnotification(msg: str) -> None:
    # send to simplepush.io
    requests.post(f"https://api.simplepush.io/send/", data={"title": "Temperature warning", "msg": msg, "key": KEY})


if __name__ == "__main__":
    main()


