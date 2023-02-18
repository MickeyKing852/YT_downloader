import requests, os, datetime, time, logging, traceback, inspect, pathlib, pytube
from pytube import Playlist, innertube, YouTube
from pytube import innertube
class YT_downloader_V2:

    @staticmethod
    def env_init() -> None:

        # env_init, infoLog, errorLog created for more faster start up speed
        # create Temp folder in current dir for log and token file
        rootPath = os.path.join(os.path.abspath(os.curdir),'Temp')
        logPath = os.path.join(rootPath, "log")
        cachePath = os.path.join(rootPath, "cache")

        if not os.path.exists(rootPath): os.mkdir(rootPath)
        if not os.path.exists(logPath): os.mkdir(logPath)
        if not os.path.exists(cachePath): os.mkdir(cachePath)

        #set path for token file
        innertube._cache_dir = cachePath
        innertube._token_file = os.path.join(innertube._cache_dir, 'tokens.json')


    @staticmethod
    def logging_config() -> None:

        # set format and path for log file
        logging.basicConfig(level=logging.INFO,
                            filename=f".\Temp\log\{datetime.datetime.now().strftime('%d-%m-%Y')}.log",
                            filemode='a',
                            format='%(asctime)s ---- [ %(pathname)s ---- %(levelname)s ] ---- %(message)s',
                            datefmt='%d-%m-%Y_%H.%M.%S'
                            )

    @staticmethod
    def infoLog(msg: str) -> None:

        logging.info(f'{inspect.stack()[1].function} ---- {msg}')


    @staticmethod
    def errorLog(eMsg: Exception) -> None:
        logging.error(f'{inspect.stack()[1].function} ---- {eMsg}')

    @staticmethod
    def criticalLog() -> None:
        logging.critical(traceback.format_exc().replace("\n", " "))
        logging.info('!!! Program stopped !!!')
        print('Please go check Temp/log')
        time.sleep(3)
        exit()

    def __urlNormalize(self, url: str) -> pytube:

        self.infoLog("stating URL Normalize")

        try:
            # check URL is playlist or not
            if 'playlist' in url: return Playlist(url)

            # removing args if video is a part of playlist
            url = url.split('&')
            [url.remove(i) for i in url if 'list=' in url]
            [url.remove(i) for i in url if 'index=' in url]

            # use_oauth for youtube age restriction
            # if token.json is not exist, authentication is required
            return YouTube([out for out in url][0], use_oauth=True)

        except Exception as e:
            self.criticalLog()

    def __getUrlFromPlaylist(self, object: Playlist) -> []: return object.video_urls

    def getInfo(self) -> dict:

        fps, qualityLabel, videoLink = [], [], []
        url_list, video_list = [], []
        video_info = {}
        mimeType = ""
        target = self.__urlNormalize(self.url)

        if "pytube.contrib.playlist.Playlist" in str(type(target)):
            logging.info("start Playlist mode")
            [url_list.append(self.__urlNormalize(i)) for i in self.__getUrlFromPlaylist(target)]

        if "pytube.__main__.YouTube" in str(type(target)):
            logging.info("start Normal mode")
            url_list.append(target)

        logging.info("getting video information from Youtube")

        for object in url_list:
            for versions in object.streaming_data['formats']:
                # gather elements from muitple versions
                fps.append(versions['fps'])
                qualityLabel.append(versions['qualityLabel'])
                videoLink.append(versions['url'])
                mimeType = versions['mimeType']

            video_info.update({
                "Title": object.title,
                "mimeType": mimeType,
                "fps": fps,
                "qualityLabel": qualityLabel,
                "URL": videoLink
            })
            # for return video info in playlist
            yield video_info

    def download(self) -> bool:
        # url must be the link in video_info
        try:
            # download content with youtube api
            r = requests.get(self.url, stream=True)

            self.infoLog(f'get into {self.path}')
            os.chdir(self.path)

            logging.info(f'create file {self.name}')
            with open(self.name, mode='wb') as writer:
                for chunk in r.iter_content(chunk_size=2048 * 2048):
                    if chunk:
                        writer.write(chunk)
                writer.close()

            self.infoLog("Downloaded video")
            return True

        except Exception as e:
            self.errorLog(e)
            return False

    def __init__(self, url: str, fileName=None, filePath=None):

        self.infoLog(f'start YT_Downloader for {url}')

        try:
            self.url = url
            self.path = [os.path.abspath(os.curdir) if filePath == None else filePath][0]
            self.name = [f"{datetime.datetime.now().strftime('%d-%m-%Y_%H.%M.%S')}.mp4" if fileName == None else fileName][0]

        except Exception:
            self.criticalLog()