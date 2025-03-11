import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


FILE_CATEGORIES = { 
    "Documents" : [".pdf", ".txt", ".docx", ".pptx", ".xslx"] , 
    "Images" : [".jpg" , ".jpeg", ".png", ".gif"],
    "Videos" : [".mp4", ".mov", ".avi"],
    "Music" : [".mp3", ".wav"],
    "Programs" : [ ".exe", ".msi", ".jar"],
    "Compressed": [".zip", ".rar"]
    }

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

def scan_folder():
    for filename in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, filename)
        if os.path.isfile(file_path):
            move_file(file_path)

def move_file(file_path):
    _, file_extension = os.path.splitext(file_path)

    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            destination_folder = os.path.join(DOWNLOADS_FOLDER, category)
            os.makedirs(destination_folder, exist_ok= True) # Create folder if not exists
            shutil.move(file_path, os.path.join(destination_folder, os.path.basename(file_path)))
            print(f"Moved: {file_path} -> {destination_folder}")
            return  # Stop once the file is moved


scan_folder()


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            move_file(event.src_path)


def monitor_folder():
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, DOWNLOADS_FOLDER, recursive= False)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

monitor_folder()
