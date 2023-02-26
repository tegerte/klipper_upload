import os
import signal
import sys
import time
import requests
import argparse

# import logging

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


PATTERNS = ["*.gcode"]


ignore_patterns = None
ignore_directories = False
case_sensitive = True
go_recursively = True

my_event_handler = PatternMatchingEventHandler(
    PATTERNS, ignore_patterns, ignore_directories, case_sensitive
)
my_observer = Observer()


def get_size(path):
    size = path.stat().st_size
    if size < 1024:
        return f"{size} bytes"
    elif size < pow(1024, 2):
        return f"{round(size/1024, 2)} KB"
    elif size < pow(1024, 3):
        return f"{round(size/(pow(1024,2)), 2)} MB"
    elif size < pow(1024, 4):
        return f"{round(size/(pow(1024,3)), 2)} GB"


def upload_gcode(path_to_file: Path, ip_adress: str) -> tuple[int, str]:
    """
    Uses the API of Moonraker to upload a file to Klipper. Its checked in response if the uploaded filename is
    returned as indication of successful upload.
    :param path_to_file: Path-opbj
    :return: flag for successful operation
    """
    file_path = Path(path_to_file)
    print(f"Initiating  upload to {ip_adress} !")
    with open(path_to_file, "rb") as gcode:
        pload = {"file": gcode, "print": "false"}
        print(
            f"~~~~~ Starting upload of {get_size(file_path)} to moonraker  ~~~~~~~~~~~~~~~~~"
        )
        try:
            r = requests.post(f"http://{ip_adress}/server/files/upload", files=pload)
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            exit(11)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            return 12, str(errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            return 13, str(errt)
        except requests.exceptions.RequestException as e:
            # catastrophic error...
            print(f"Something went really wrong, error message: {e}")
            exit(100)
        # print(r.text)
        print(f"Upload took {r.elapsed.seconds} seconds")

    if r != "" and r.json()["item"]["path"] == file_path.name:
        print(
            "~~~~~ Successfully uploaded new gcode file to moonraker  ~~~~~~~~~~~~~~~~~"
        )
        return 0, ""
    return 1, "some other error"


def on_created(event):
    print(f"hey ho, new gcode {event.src_path} has been created!")
    ret = upload_gcode(event.src_path, ip)
    if ret[0] > 0:
        print(f"Sh..., that didn't work, exiting...")
        exit(ret[0])


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")


def on_moved(event):
    print(f"Hey, i think PrucaSlicer created some nice gcode {event.dest_path} !")
    # the way PrisaSlicer generates the files...
    ret = upload_gcode(event.dest_path, ip)
    if ret[0] > 0:
        print(f"Sh..., that didn't work, exiting...")
        # that is not so nice, but we're in a threaded process so simply exiting will not work
        os.kill(os.getpid(), signal.SIGINT)


my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--ip_address")
parser.add_argument("-d", "--observed_dir")

args = parser.parse_args()


ip = args.ip_address
path_gcode = args.observed_dir
print(f"Listening for changes in {path_gcode} to upload to {ip}... ")

my_observer.schedule(my_event_handler, path_gcode, recursive=go_recursively)
my_observer.start()


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    my_observer.stop()
my_observer.join()
