from pytube import YouTube
from pytube import Playlist
import tkinter
import tkinter.ttk
import tkinter.filedialog
import threading
import ffmpeg
import logging
import re
import os


class YT_downloader:

    def __init__(self,mode='gui'):
        if mode == 'gui':
            self.gui()
        elif mode == 'cli':
            self.cli()
        else: pass

        self.log_setup()

    @staticmethod
    def log_setup():
        log_format = '%(asctime)s -- %(levelname)s -- %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_format, datefmt='%d/%m/%Y-%H:%M')

    @staticmethod
    def caption(url: str, lan: str, filename: str = '', out_path: str = '') -> None:
        url = url.split('&')

        target = YouTube(url)
        subtitle = target.captions.get(lan)

        if filename == '':
            filename = f'{target.title.replace("|", "")}'
        elif '|' in filename:
            filename = filename.replace('|', '')

        logging.info(f'downloading {filename} subtitle -- caption')

        if out_path == '':
            file = open(f'{filename}.srt', 'w')
        else:
            file = open(f'{out_path}/{filename}.srt', 'w')
        file.write(subtitle.generate_srt_captions())
        file.close()

        logging.info('finish -- caption')

    def vdo(self, url: str, resolution: str, fps: int, filename: str = '', out_path: str = ''):
        url = self.playlist_url_normalization(url)
        target = YouTube(url)

        if filename == '':
            filename = f'{target.title.replace("|", "")}'
        elif '|' in filename:
            filename = filename.replace('|', '')

        logging.info(f'downloading {target.title} ({url}) -- vdo')
        if out_path == '':
            target.streams.filter(subtype='mp4', resolution=resolution, fps=fps)[0].download(filename=filename)
            self.vdo_path = f'{filename}.mp4'
        else:
            target.streams.filter(subtype='mp4', resolution=resolution, fps=fps)[0].download(output_path=out_path,
                                                                                             filename=filename)
            self.vdo_path = f'{out_path}/{filename}.mp4'
        logging.info('Finish -- vdo')

    def sound(self, url: str, filename: str = '', out_path: str = ''):

        target = YouTube(url)

        if filename == '':
            filename = f'audio_{target.title.replace("|", "")}'
        elif '|' in filename:
            filename = filename.replace('|', '')

        logging.info(f'downloading {target.title} ({url}) -- sound')
        # change filename
        if out_path == '':
            target.streams.filter(type='audio').first().download(filename=filename)
            self.audio_path = f'{filename}.mp4'
        else:
            target.streams.filter(type='audio').first().download(output_path=out_path, filename=filename)
            self.audio_path = f'{out_path}/{filename}.mp4'
        logging.info('Finish -- sound')

    def merge(self, vdo_path: str, audio_path: str, filename: str, out_path: str) -> None:

        vdo_stream = ffmpeg.input(vdo_path)
        audio_stream = ffmpeg.input(audio_path)
        ffmpeg.output(vdo_stream, audio_stream, f'{filename}.mp4').run()
        os.remove(vdo_path)
        os.remove(audio_path)
        os.replace(f'{filename}.mp4', f'{out_path}/{filename}.mp4')

        logging.info('Finish -- merge')

    def playlist_url_normalization(self,url:str)->str:
        out_string = ''
        url = url.split('&')

        for i in url:
            if 'list=' in i:
               url.remove(i)

        for i in url:
            if 'index=' in i:
               url.remove(i)

        for i in url:
            out_string += i

        return out_string

    def vdo_info(self, url: str):
        target = YouTube(url)
        time = target.length
        captions = target.captions
        title = target.title
        author = target.author
        info = target.streams.filter(mime_type='video/mp4', progressive=False)
        lan_code = []
        self.exist_fps = []
        self.exist_res = []

        for data in info:
            if not re.search(' progressive="True" ', str(data)):
                out = str(data).split()
                self.exist_res.append(out[3].replace('res=', '').replace('"', '')) if out[3].replace('res=',
                                                                                                     '').replace('"',
                                                                                                                 '') not in self.exist_res else None
                self.exist_fps.append(out[4].replace('fps=', '').replace('"', '')) if out[4].replace('fps=',
                                                                                                     '').replace('"',
                                                                                                                 '') not in self.exist_fps else None

        self.captions = str(list(captions)).replace('Caption lang=', '').replace(' code=', '').replace('<"',
                                                                                                       '').replace('">',
                                                                                                                   '').replace(
            '""', ',').replace(' ', '').replace('[', '').replace(']', '').split(',')
        [lan_code.append(self.captions[i]) for i in range(1, len(self.captions), 2)]
        [self.captions.remove(i) for i in lan_code]

        self.lan = {}
        for i in range(len(self.captions)):
            self.lan.update({self.captions[i]: lan_code[i]})

        print(f' {title} | {author} | {time}s\n Available res option: ',end = '')
        [print(f'{i}',end=' | ') for i in self.exist_res]
        print('\n Available fps option: ',end = '')
        [print(f'{i}', end=' | ') for i in self.exist_fps]
        print('\n Available subtitle option: ',end = '')
        [print(f'{i}',end = ' | ') for i in self.captions]
        print()
        [print(f'{i}',end=' | ') for i in lan_code]
        print(self.lan)

    def gui(self):

        def res_value_assign(event):
            res_lb['values'] = self.exist_res
            res_lb.update()

        def fps_value_assign(event):
            fps_lb['values'] = self.exist_fps
            fps_lb.update()

        def caption_value_assign(event):
            caption_lb['values'] = self.captions
            caption_lb.update()

        def path_asking(event):
            file_path = tkinter.filedialog.askdirectory()
            path_in.delete(0, 'end')
            path_in.insert(0, file_path)
            path_in.update()

        def run():
            def thread_merge():
                waiting = True

                while waiting:
                    if thread_vdo.is_alive() or thread_audio.is_alive():
                        pass
                    else:
                        waiting = False
                        threading.Thread(target=self.merge,
                                         args=[self.vdo_path, self.audio_path, name_box.get(), path_in.get()]).start()

            if v.get() == 1:
                thread_vdo = threading.Thread(target=self.vdo,
                                              args=[link_box.get(), res_lb.get(),
                                                    int(str(fps_lb.get()).replace('fps', '')),
                                                    f'vdo_{name_box.get()}'])
                thread_audio = threading.Thread(target=self.sound, args=[link_box.get(), f'audio_{name_box.get()}'])


                if caption_lb.get() in self.captions:
                    threading.Thread(target=self.caption,
                                     args=[link_box.get(), self.lan.get(caption_lb.get()), name_box.get(),
                                           path_in.get()]).start()

                thread_vdo.start()
                thread_audio.start()
                threading.Thread(target=thread_merge).start()

            elif v.get() == 2:
                threading.Thread(target=self.sound, args=[link_box.get(), name_box.get(), path_in.get()]).start()

        root = tkinter.Tk()
        root.title('YT Downloader')
        root.geometry('350x190')

        upper = tkinter.Frame(root)
        upper.pack(side=tkinter.TOP)

        title = tkinter.Frame(upper)
        title.pack(side=tkinter.LEFT, anchor=tkinter.W)

        input = tkinter.Frame(upper)
        input.pack(side=tkinter.LEFT, anchor=tkinter.CENTER)

        link_l = tkinter.Label(title, text='URL:')
        link_box = tkinter.Entry(input, width=35)
        link_box.bind('<FocusOut>', lambda event: threading.Thread(
            self.vdo_info(link_box.get())).start() if link_box.get() is not None else None)
        link_box.bind('<Return>', lambda event: threading.Thread(
            self.vdo_info(link_box.get())).start() if link_box.get() is not None else None)
        link_l.pack(side=tkinter.TOP)
        link_box.pack()

        name_l = tkinter.Label(title, text='File Name:')
        name_box = tkinter.Entry(input, width=35)
        name_l.pack(side=tkinter.TOP)
        name_box.pack()

        path_l = tkinter.Label(title, text='Path:')
        path_in = tkinter.Entry(input, width=35)
        path_in.bind('<Double-Button-1>', path_asking)
        path_in.bind('<Return>', path_asking)
        path_l.pack()
        path_in.pack()

        caption_l = tkinter.Label(title, text='caption:')
        caption_lb = tkinter.ttk.Combobox(input, height=1, width=25)
        caption_lb.bind('<Button-1>', caption_value_assign)
        caption_l.pack()
        caption_lb.pack()

        res_l = tkinter.Label(title, text='Resoulion:')
        res_lb = tkinter.ttk.Combobox(input, height=1, width=15)
        res_lb.bind('<Button-1>', res_value_assign)
        res_l.pack()
        res_lb.pack()

        fps_l = tkinter.Label(title, text='FPS:')
        fps_lb = tkinter.ttk.Combobox(input, height=1, width=10)
        fps_lb.bind('<Button-1>', fps_value_assign)
        fps_l.pack()
        fps_lb.pack()

        input_type = tkinter.Frame(input)
        input_type.pack()
        v = tkinter.IntVar()
        v.set(1)
        type_l = tkinter.Label(title, text='Type:')
        type_vdo = tkinter.Radiobutton(input_type, text='MP4', variable=v, value=1)
        type_audio = tkinter.Radiobutton(input_type, text='MP3', variable=v, value=2)
        type_l.pack()
        type_vdo.pack(side=tkinter.LEFT)
        type_audio.pack(side=tkinter.RIGHT)

        self.err_message = ''

        run = tkinter.Button(root, text='Download', command=run)
        display = tkinter.Label(root, text=f' {self.err_message}')
        run.pack(side=tkinter.LEFT)

        display.pack(side=tkinter.BOTTOM)

        root.mainloop()

    def cli(self):
        url = "https://www.youtube.com/watch?v=8nI1CDsNZI0&list=PLs9xv9XcDYotfNqp5X8GYo7vlcI0u11nT&index=6&ab_channel=MoriCalliopeCh.hololive-EN"
        url = url.split('&')

        for i in url:
            if 'list=' in i:
               url.remove(i)

        for i in url:
            if 'index=' in i:
               url.remove(i)





app = YT_downloader()

