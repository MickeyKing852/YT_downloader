import tkinter


class CmdPanel:

    def screenInit(self):

        self.root = tkinter.Tk()
        self.root.geometry("900x300")
        self.root.title('YT_Downloader_CLI')
        self.root.iconbitmap(r'C:\Users\micke\PycharmProjects\YT_downloader\youtube-downloader-icon.ico')
        self.__mainPage()
        self.root.mainloop()

    def __mainPage(self):
        displayArea = tkinter.Text(self.root, width=90, height=30)

        displayArea.grid()


    def __init__(self):
        self.screenInit()




if __name__ == '__main__':
    CmdPanel()