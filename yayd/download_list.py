from pytube import YouTube
from typing import Any, List
from customtkinter import CTkScrollableFrame
from .download_item import DownloadItem


class DownloadList(CTkScrollableFrame):
    """A `DownloadList` is a `CTkScrollableFrame` that contains a list of
    `DownloadItem`s.

    Pretty specific to this application.
    """

    items = List[DownloadItem]

    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.items = []

    def add(self, video: YouTube) -> None:
        self.items.append(DownloadItem(self, video))
        self.items[-1].grid(row=len(self.items), column=0)

    def remove(self, video: YouTube) -> None:
        self.items.remove(DownloadItem(self, video))
