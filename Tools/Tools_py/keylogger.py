import time
import difflib
from tkinter import Tk, filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_cache = {}

def diff_file(path):
    global file_cache

    try:
        with open(path, 'r', encoding='utf-8') as f:
            new = f.readlines()
    except:
        return  # file có thể bị khóa hoặc không đọc được

    old = file_cache.get(path)

    if old is None:
        file_cache[path] = new
        return

    diff = difflib.unified_diff(old, new, fromfile='old', tofile='new')
    print(''.join(diff))

    file_cache[path] = new


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[MODIFIED] {event.src_path}")
            diff_file(event.src_path)


def choose_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Chọn thư mục cần theo dõi")
    root.destroy()
    return folder


if __name__ == "__main__":
    folder = choose_folder()
    if not folder:
        print("Bạn chưa chọn thư mục.")
        exit()

    observer = Observer()
    observer.schedule(MyHandler(), folder, recursive=True)
    observer.start()

    print(f"Đang theo dõi thư mục: {folder}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()