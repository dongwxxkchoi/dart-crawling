from datetime import datetime
import os

def get_today():
    today = datetime.today().strftime("%Y-%m-%d")
    return today

def get_file_path(folder, file_name, file_ext):
    today = get_today()
    folder = 'data'
    file = file_name + today + file_ext
    file_path = os.path.join(folder, file)

    return file_path