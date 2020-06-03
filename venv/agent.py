import psutil
import time
import sys


def run():
    print('CPU load:', psutil.cpu_percent(),'%')
    print('RAM usage:', psutil.virtual_memory().percent,'%')

    # you can convert that object to a dictionary
    dict(psutil.virtual_memory()._asdict())

    run_timer(10)


def run_timer(seconds):
    # Automatic countdown mechanism
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        minutes = 0
        seconds = remaining
        if remaining > 60:
            minutes = int(seconds / 60)
            seconds = int(seconds % 60)
        else:
            seconds = remaining
        # sys.stdout.write("{:2d} seconds remaining until next poll".format(seconds))
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")
    run()


run()
