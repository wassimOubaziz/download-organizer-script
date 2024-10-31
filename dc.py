import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import winreg

def get_download_folder():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
        download_folder = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    return download_folder

class FileHandler(FileSystemEventHandler):
    def __init__(self, download_folder, image_folder, video_folder, document_folder, music_folder, compressed_folder, others_folder):
        self.download_folder = download_folder
        self.image_folder = image_folder
        self.video_folder = video_folder
        self.document_folder = document_folder
        self.music_folder = music_folder
        self.compressed_folder = compressed_folder
        self.others_folder = others_folder

    def on_modified(self, event):
        for filename in os.listdir(self.download_folder):
            if not os.path.isdir(os.path.join(self.download_folder, filename)):
                self.move_file(filename)

    def move_file(self, filename, retries=5):
        file_path = os.path.join(self.download_folder, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            destination = os.path.join(self.image_folder, filename)
        elif filename.lower().endswith(('.mp4', '.mkv', '.flv', '.avi', '.mov')):
            destination = os.path.join(self.video_folder, filename)
        elif filename.lower().endswith(('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt')):
            destination = os.path.join(self.document_folder, filename)
        elif filename.lower().endswith(('.mp3', '.wav', '.flac', '.aac', '.ogg')):
            destination = os.path.join(self.music_folder, filename)
        elif filename.lower().endswith(('.zip', '.rar', '.tar', '.gz', '.7z', '.bz2')):
            destination = os.path.join(self.compressed_folder, filename)
        else:
            destination = os.path.join(self.others_folder, filename)

        for attempt in range(retries):
            try:
                shutil.move(file_path, destination)
                print(f'Moved: {file_path} to {destination}')
                break
            except PermissionError:
                print(f'PermissionError: Retrying to move {file_path}... ({attempt + 1}/{retries})')
                time.sleep(1)  # Wait a bit before retrying
        else:
            print(f'Failed to move {file_path} after {retries} attempts.')

def main():
    download_folder = get_download_folder()
    image_folder = os.path.join(download_folder, 'images')
    video_folder = os.path.join(download_folder, 'videos')
    document_folder = os.path.join(download_folder, 'documents')
    music_folder = os.path.join(download_folder, 'music')
    compressed_folder = os.path.join(download_folder, 'compressed')
    others_folder = os.path.join(download_folder, 'others')

    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(video_folder, exist_ok=True)
    os.makedirs(document_folder, exist_ok=True)
    os.makedirs(music_folder, exist_ok=True)
    os.makedirs(compressed_folder, exist_ok=True)
    os.makedirs(others_folder, exist_ok=True)

    event_handler = FileHandler(download_folder, image_folder, video_folder, document_folder, music_folder, compressed_folder, others_folder)
    observer = Observer()
    observer.schedule(event_handler, path=download_folder, recursive=False)
    observer.start()

    print('Monitoring started. Press Ctrl+C to stop.')
    try:
        while True:
            pass  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
