from YT_Downloader import YT_downloader_V2
from YT_DownloaderExpection import *
import os.path, re, time

class CLI(YT_downloader_V2):


    def optionNormalize(self, option:str)-> list:

        # return list only with digit
        out = []
        option = option.replace(' ', '').split(',')
        [out.append(i) if i.isdigit() else None for i in option].remove(None)
        option.sort()

        return out

    @staticmethod
    def fileNameCheck(filename:str) -> bool:
        return False if re.match(r'[\\\/\|\:\*\?\<\>\"]',filename) else True

    @staticmethod
    def pathCheck(path:str) -> bool:
       return os.path.exists(path)

    def __listinfo(self) -> list:

        URL = []
        counter = 0

        try:
            for i in self.getInfo():

                # merge fps and resolution as resolutionInfo
                # playlist.qualityLabel + playlist.fps
                resolutionInfo = []
                [resolutionInfo.append(i['qualityLabel'][j] + str(i['fps'][j])) for j in range(len(i['qualityLabel']))]
                resolutionInfo.sort()

                # store video link in youtube api
                [URL.append(link) for link in i['URL']]

                for info in resolutionInfo:
                    print(f"{counter}) {i['Title']} {info}")
                    counter += 1

            return URL

        except Exception:
            self.criticalLog()

    def __choiceCheck(self, choice: str) -> None:

        self.infoLog(f'Choice: {choice}')

        try:
            if not choice.isdigit():
                raise InvaildChoiceError

            if int(choice) > len(self.URL):
                raise InvaildChoiceError

        except InvaildChoiceError as e:
            print(f'{choice}, {e}')
            self.errorLog(e)
            exit()

    def __fileNameSetup(self, choice:str):

        end = False
        fileName = ""

        self.infoLog(f'Choice: {choice}')

        while not end:
            try:
                name = input(f"What is the filename of vdo ({choice}):")
                self.infoLog(f'User inputted fileName: {name}')

                if name == '' or name == ' ':
                    self.infoLog('return None')
                    return None

                if not self.fileNameCheck(name):
                    raise InvaildFileNameError
                else:
                    self.infoLog('return name')
                    return name

            except InvaildFileNameError as e:
                print(e)
                self.errorLog(e)

            except Exception:
                self.criticalLog()

    def __filePathSetup(self, choice:str):

        end = False
        self.infoLog(f'Choice: {choice}')

        while not end:
            try:
                path = input(f"Where for saving vdo ({choice}):")
                self.infoLog(f'User inputted filePath: {path}')

                if path == '' or path == ' ':
                    self.infoLog('return None')
                    return None

                if not self.pathCheck(path):
                    raise PathNotExistError
                else:
                    self.infoLog('return path')
                    return path

            except PathNotExistError as e:
                print(e)
                self.errorLog(e)

            except Exception :
                self.criticalLog()


    def main(self):

        try:
            self.URL = self.__listinfo()
            filename, filepath = [], []
            self.option = self.optionNormalize( str(input('Download which vdo(s): ')))
            self.infoLog(f'{self.main.__name__} ---- User inputted option: {self.option}')

            if len(self.option) <= 0:
                self.infoLog('Option is empty')
                print('Option is empty')
                raise InvaildChoiceError


            # change for playlist mode
            self.infoLog('start filename & path insert step')

            for i in self.option:

                self.__choiceCheck(i)

                name = self.__fileNameSetup(i)
                path = self.__filePathSetup(i)

                filename.append(name)
                filepath.append(path)

            self.infoLog(f'filepath: {filepath}')
            self.infoLog(f'filename: {filename}')


            self.infoLog('filename & path insert step end')

            self.infoLog('start download step')
            for i in range( len(self.option) ):
                name = 'Default Name' if filename[int(i)] == None else filename[int(i)]
                path = 'Default Path' if filepath[int(i)] == None else filepath[int(i)]

                self.infoLog(f'Downloading vdo({self.option[i]}): path: {path} {name}')
                print(f"Downloading your video({self.option[i]}): path: {path} {name} ...\nPlease wait OR go check {os.path.abspath(os.curdir)}\Temp\log for more information")

                result = YT_downloader_V2(self.URL[int(self.option[i])],
                                          None if filename[i] == '' else filename[int(i)],
                                          None if filepath[i] == '' else filepath[int(i)]
                                          ).download()
                print(f"{'Downloaded video' if result else 'Error cursed check Temp/log for more information'}")

            self.infoLog('download step end')

        except Exception as e:
            self.errorLog(e)

        finally:
            print('All download task is finished\nThis program will auto close at 5s')
            time.sleep(5)
            self.infoLog('Program closed')

    def __init__(self):

        self.option = []

        self.env_init()
        self.logging_config()

        self.infoLog('start getting information for YT_Downloader_CLI')
        super().__init__(url=input("Please enter URL for your Vdo: "))
        self.main()

if  __name__ == "__main__":
    CLI()