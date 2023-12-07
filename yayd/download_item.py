import os

from typing import Any, Callable, Optional
from customtkinter import CTkFrame, CTkLabel, CTkImage, StringVar
from PIL import Image
from pytube import YouTube, Stream
from pathlib import Path
from moviepy.editor import AudioFileClip
from tktooltip import ToolTip


# type hinting
DownloadSuccessCallback = Optional[Callable[[None], None]]
DownloadFailureCallback = Optional[Callable[[None], None]]
DownloadProgessCallback = Optional[Callable[[float], None]]


# constants
IMG_DIR: Path = (Path(__file__).parent / "img").resolve()
SUCCESS_ICON: CTkImage = CTkImage(Image.open(IMG_DIR / "blue_checkmark.png"))
FAILURE_ICON: CTkImage = CTkImage(Image.open(IMG_DIR / "red_cross.png"))


# class def
class DownloadItem(CTkFrame):
    # properties
    video: YouTube
    label: CTkLabel
    download_icon: CTkLabel
    tooltip: ToolTip

    # user defined callbacks
    download_success_command: DownloadSuccessCallback
    download_failure_command: DownloadFailureCallback

    # methods
    def __init__(
        self,
        master: Any,
        video: YouTube,
        download_success_command: DownloadSuccessCallback = None,
        download_failure_command: DownloadFailureCallback = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.video = video

        self.download_success_command = download_success_command
        self.download_failure_command = download_failure_command

        self.label = CTkLabel(self, text=video.title)
        self.label.grid(row=0, column=0, sticky="nsew")

        self.download_icon = CTkLabel(self, text=None)
        self.download_icon.grid(row=0, column=2, sticky="nse")
        self.tooltip = ToolTip(self.download_icon)

    def download(
        self, output_dir: str, on_progress: Callable[[int], None] | None = None
    ) -> None:
        print(f"Downloading into {output_dir}...")

        try:
            on_progress(0)

            # download audio only .mp4
            print(f"Downloading {self.video.title}")
            stream: Stream = self.video.streams.filter(only_audio=True).first()
            downloaded_path: str = stream.download(output_dir)

            on_progress(0.4)

            # convert
            print(f"Converting {downloaded_path} into an MP3")
            audio: AudioFileClip = AudioFileClip(downloaded_path)
            base, ext = os.path.splitext(downloaded_path)
            filename = f"{base}.mp3"
            audio.write_audiofile(filename)

            on_progress(0.7)

            # remove original mp4
            print(f"Removing {downloaded_path}")
            if os.path.exists(downloaded_path):
                os.remove(downloaded_path)

            on_progress(1)

            # display success as a checkmark and update tooltip with output path
            print(f"Successfully downloaded: {self.video.title}")
            self.tooltip.msg = f"Successfully downloaded into {filename}"
            self.download_icon._image = SUCCESS_ICON
            self.download_icon._update_image()
            self.on_download_success()
        except Exception as e:
            # display error as red X and a update tooltip to show error
            print(f"Failed to download: {self.video.title}")
            self.tooltip.msg = f"Failed to download: {e}"
            self.download_icon._image = FAILURE_ICON
            self.download_icon._update_image()
            self.on_download_failure()

    def on_download_failure(self) -> None:
        if self.download_failure_command is not None:
            self.download_failure_command()

    def on_download_success(self) -> None:
        if self.download_success_command is not None:
            self.download_success_command()
