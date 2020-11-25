import os
import threading
import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

folder_id = ""
total_files = 0
current_count = 0
counter_lock = Lock()

def create_google_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

def get_folder_id(drive, folderName):
    global folder_id
    folders = drive.ListFile({'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        if folder['title'] == folderName:
            folder_id = folder['id']
            print(f"Found parent folder {folder_id}")
            break

def _upload_file(file_path, drive):
    global total_files, current_count
    if os.path.exists(file_path):
        thread_name = threading.current_thread().getName()
        temp_file = drive.CreateFile({
            'title': os.path.basename(file_path), 
            'parents': [{'id': folder_id}]})
        temp_file.SetContentFile(os.path.abspath(file_path))
        temp_file.Upload()
        with counter_lock:
            current_count += 1
        print(f"Thread -> {thread_name} has uploaded the file {os.path.basename(file_path)}. Progress: {current_count}/{total_files}({(current_count/total_files)*100:.0f}%)")

def upload_files(file_path, drive, pool):
    global total_files
    total_files = 0
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            pool.submit(_upload_file, os.path.abspath(file_path), drive)
            total_files = 1
        else:
            for root, _, files in os.walk(file_path):
                print(f"Started to work on the directory {root}")
                total_files += len(files)
                for f in files:
                    pool.submit(_upload_file, os.path.join(root, f), drive)
    else:
        print("The directory {0} doesn't exist".format(file_path))

def main():
    folder_list = ["List of local folders to be synced"]
    try:
        drive = create_google_drive()
        get_folder_id(drive, "<<SAMPLE_FOLDER_ON_DRIVE>>")
        start_time = time.time()
        pool = ThreadPoolExecutor()
        for folder in folder_list:
            upload_files(folder, drive, pool)
        pool.shutdown(wait=True)
        end_time = time.time()
        print(f"The execution took around {(end_time - start_time):.3f} seconds to upload {total_files} files.")
    except FileNotFoundError as fio:
        print(fio)
    except Exception as es:
        print(es)

if __name__ == "__main__":
    main()