import os, logging
from moviepy.editor import *

class RcList:

    def addRc(self, message:str) -> None:
        self.rcList.append(message)

    def getResult(self) -> bool:

        if len(self.rcList) >0:
            return False
        else:
            return True

    def toString(self) -> str:

        for rc in self.rcList:
            self.out += f"{rc}, "

        return self.out

    def __init__(self) -> None:
        self.rcList = []
        self.out = ""

class Converter:

    def __int__(self, fileName: str, sourcePath: str, savePath: str):

        self.fileName = fileName
        self.sourcePath = sourcePath
        self.savePath = savePath

        self.sourceFile = self.__sourceFile()
        self.saveFile = self.__saveFile()

    @staticmethod
    def mp4ToMp3(sourcePath: str, savePath: str):

        source = VideoFileClip(sourcePath)
        source.audio.write_audiofile(savePath)
        source.close()

    def __saveFile(self) -> str:

        fileName = self.fileName
        if ".mp3" not in fileName:
            fileName += ".mp3"
        return os.path.join(self.savePath, fileName)

    def __sourceFile(self) -> str:

        fileName = self.fileName

        if ".mp4" not in fileName:
            fileName += ".mp4"
        return os.path.join(self.sourcePath, fileName)

    def isPathOk(self) -> RcList:

        rcList = RcList()

        if not os.path.exists(self.sourcePath):
            rcList.addRc("Source path does not exist")

        if not os.path.exists(self.savePath):
            rcList.addRc("Save path does not exist")

        if not os.path.exists(self.sourceFile):
            rcList.addRc("Source file does not exist")

        return rcList
