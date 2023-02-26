import time
import requests

# import logging

from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


PATH_GCODE = "/home/tassilo/3d_print/gcode/"
PATTERNS = ["*.gcode"]
IP = "192.168.1.165"


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


def upload_gcode(path_to_file: Path) -> bool:
    """
    Uses the API of Moonraker to upload a file to Klipper. Its checked in response if the uploaded filename is
    returned as indication of successful upload.
    :param path_to_file: Path-opbj
    :return: flag for successful operation
    """
    file_path = Path(path_to_file)
    with open(path_to_file, "rb") as gcode:
        pload = {"file": gcode, "print": "false"}
        print(
            f"~~~~~ Starting upload of {get_size(file_path)} to moonraker  ~~~~~~~~~~~~~~~~~"
        )
        r = requests.post(f"http://{IP}/server/files/upload", files=pload)
        # print(r.text)
        print(f"Upload took {r.elapsed.seconds} seconds")

    if r != "" and r.json()["item"]["path"] == file_path.name:
        print(
            "~~~~~ Successfully uploaded new gcode file to moonraker  ~~~~~~~~~~~~~~~~~"
        )
        return True
    return False


def on_created(event):
    print(f"hey ho, {event.src_path} has been created!")
    upload_gcode(event.src_path)


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")


my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved


my_observer.schedule(my_event_handler, PATH_GCODE, recursive=go_recursively)
my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
my_observer.join()
