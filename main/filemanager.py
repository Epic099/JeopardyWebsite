import os
import shutil
import json

class ErrorHandler:
	def printError(error):
		print(error)
class File:
    def __init__(self, path : str, create : bool = False):
        relativePath = not os.path.isabs(path)		
        self.path = path if not relativePath else os.path.abspath(path)
        if not self.exists and create:
            self.create()
        temp = os.path.splitext(path)
        self.file_name = temp[0]
        self.file_extension = temp[1]
        self.file_directory = os.path.dirname(self.path)
    @classmethod
    def createPath(cl, directory : str, filename : str, extension : str):
        directory = directory + "/" if directory[len(directory)-1] != "/" else directory
        return directory + filename + extension
    @property
    def exists(self):
        return os.path.isfile(self.path)
    def getFullPath(self, update : bool = False):
        path = self.file_directory + "/" + self.file_name + self.file_extension
        if update:
            self.path = path
        return path
    def create(self):
        if self.exists: return
        try:
            with open(self.path, "x") as file:
                pass
        except Exception as error:
            ErrorHandler.printError(f"Could not create file at {self.path}. ({error})")	
		
    def read(self):
        try:
            if not self.exists:
                raise FileNotFoundError(f"[Errno 2] No such file or directory: {self.path}")
            with open(self.path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as error:
            ErrorHandler.printError(f"Could not read file at {self.path}. ({error})")
        return None
    def readJSON(self):
        data = self.read()
        if data == None: return None
        try:
            return json.loads(data)
        except Exception as error:
            ErrorHandler.printError(f"Could not read JSON from file at {self.path}. ({error})")
        return None
    def write(self, data : str):
        try:
            if not self.exists:
                raise FileNotFoundError(f"[Errno 2] No such file or directory: {self.path}")
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(data)
                return True
        except Exception as error:
            ErrorHandler.printError(f"Could not write to file at {self.path}. ({error})")
        return False    
    def rename(self, name : str):
        if not self.exists: return 
        if len(name) < 1: return
        old_path = self.getFullPath()
        self.file_name = name
        path = self.getFullPath(update=True)
        os.rename(old_path, path)
    def move(self, dir : str):
        if not self.exists: return 
        directory = os.path.dirname(dir)
        old_path = self.getFullPath()
        self.file_directory = directory
        new_path = self.getFullPath(update=True)
        shutil.move(old_path, new_path)
    def copy(self):
        if not self.exists: return 
        path = File.createPath(self.file_directory, self.file_name + "_copy", self.file_extension)
        data = self.read()
        file = File(path, create=True)
        file.write(data)
        return file
    def change_extension(self, extension : str):
        if not self.exists or len(extension) < 1: return
        extension = "." + extension if extension[0] != "." else extension
        old_path = self.getFullPath()
        self.file_extension = extension
        new_path = self.getFullPath(update=True)
        os.rename(old_path, new_path)
