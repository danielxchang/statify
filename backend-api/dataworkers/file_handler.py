from uuid import uuid4
from os import path, remove

from helpers.constants import EXPECTED_FILES

class FileHandler:
    def __init__(self, dir_path):
        self.__destination = dir_path

    def validate_input_files(self, files, file_type, file_extension):
        if file_type not in EXPECTED_FILES:
            return False
        
        for key in EXPECTED_FILES[file_type]:
            if key not in files or not self.__allowed_file(files[key].filename, file_extension):
                return False
        
        uploaded_file_paths = {}
        for key in EXPECTED_FILES[file_type]: 
            upload_path = self.__upload_file(files[key], key)
            uploaded_file_paths[key] = upload_path
        
        return uploaded_file_paths

    def finished_reading_files(self, file_paths):
        for path in file_paths:
            self.__delete_file(path)

    def __allowed_file(self, filename, file_extension):
        return '.' in filename and filename.rsplit('.', 1)[-1].lower() == file_extension

    def __upload_file(self, file, kind):
        file_path = path.join(self.__destination, self.__generate_unique_file_name(kind))
        file.save(file_path)
        return file_path

    def __generate_unique_file_name(self, kind):
        return f"${kind}-${uuid4()}.csv"

    def __delete_file(self, file_path):
        if path.exists(file_path):
            remove(file_path)
