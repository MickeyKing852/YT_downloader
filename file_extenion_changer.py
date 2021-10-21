import os,tkinter

class file_extenion_changer:
    def __init__(self,old_extention:str,new_extention:str,path:str):
        file = self.scan_directory(path)
        self.rename_extention(old_extention,new_extention,file)

    def scan_directory(self,dir_path:str)->list:
        file = []

        if os.path.isdir(dir_path):
            for item in os.scandir(dir_path):
                if os.path.isfile(item.path):
                    file.append(item)
        return file

    def rename_extention(self,old_extention:str,new_extention:str,file:list):
        new_file_name = []
        for item in file:
            os.rename(item.path, str(item.path).replace(old_extention,new_extention))



path = "C:\\Users\\micke\\Music\\YT_downloader\\Hololive"
o_extent = 'mp3'
n_extent = 'mp4'
obj = file_extenion_changer(o_extent,n_extent,path)