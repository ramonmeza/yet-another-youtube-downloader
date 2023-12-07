from collections import namedtuple
from customtkinter import CTk, CTkButton, CTkProgressBar, filedialog
from pytube import Playlist, YouTube
from urllib.parse import urlparse
from pathlib import Path
from .button_entry import ButtonEntry
from .constants import *
from .download_item import DownloadProgessCallback
from .download_list import DownloadList

ParsedUrl = namedtuple("ParsedUrl", ["url", "is_youtube", "is_playlist", "is_video"])


class App(CTk):
    youtube_url_button_entry: ButtonEntry | None
    download_list: DownloadList | None
    output_directory_picker: ButtonEntry | None
    download_button: CTkButton | None
    progress_bar: CTkProgressBar | None

    current_progress: float
    total_progress: float

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # initialize the window
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # initialize UI components
        self.youtube_url_button_entry = None
        self.download_list = None
        self.output_directory_picker = None
        self.download_button = None
        self.progress_bar = None

        # initialize variables
        self.total_progress = 1.0
        self.current_progress = 0.0

    def initialize_ui(self) -> None:
        self.initialize_youtube_url_button_entry()
        self.initialize_download_list()
        self.initialize_output_directory_picker()
        self.initialize_download_button()
        self.initialize_progress_bar()

    def initialize_youtube_url_button_entry(self) -> None:
        self.youtube_url_button_entry = ButtonEntry(
            self,
            "Enter a YouTube URL...",
            button_text="Add",
            command=self.add_url_to_download_list,
        )
        self.youtube_url_button_entry.grid(row=0, column=0, sticky="nsew")

    def add_url_to_download_list(self, url: str) -> None:
        parsed_url: ParsedUrl = self.parse_url(url)
        if parsed_url.is_youtube and parsed_url.is_playlist:
            print(f"Adding {parsed_url.url} to download list as a playlist")

            playlist: Playlist = Playlist(parsed_url.url)
            self.current_progress = 0.0
            self.total_progress = len(playlist.videos)
            for video in playlist.videos:
                self.download_list.add(video)
                self.update_download_progress(1.0)

        elif parsed_url.is_youtube and parsed_url.is_video:
            print(f"Adding {parsed_url.url} to download list as a video")
            self.download_list.add(YouTube(parsed_url.url))

        else:
            print(f"WARN: {parsed_url.url} is not a valid YouTube url!")

    def parse_url(self, url: str) -> ParsedUrl:
        if url is None or url == "" or url.isspace():
            return ParsedUrl("<whitespace>", False, False, False)

        parsed_url = urlparse(url)
        is_youtube: bool = "youtube.com" in parsed_url.hostname
        is_playlist: bool = parsed_url.path == "/playlist"
        is_video: bool = parsed_url.path == "/watch"
        return ParsedUrl(url, is_youtube, is_playlist, is_video)

    def initialize_download_list(self) -> None:
        self.download_list = DownloadList(self)
        self.download_list.grid(row=1, column=0, sticky="nsew")

    def initialize_output_directory_picker(self) -> None:
        self.output_directory_picker = ButtonEntry(
            self,
            "Choose an output directory...",
            button_text="Browse",
            command=self.browse_for_output_directory,
        )
        self.output_directory_picker.grid(row=2, column=0, sticky="nsew")

    def browse_for_output_directory(self, _: str) -> None:
        output_dir: str = filedialog.askdirectory()
        self.output_directory_picker.set_text(output_dir)

    def initialize_download_button(self) -> None:
        self.download_button = CTkButton(self, text="Download", command=self.download)
        self.download_button.grid(row=3, column=0, sticky="nsew")

    def download(self) -> None:
        output_dir = self.output_directory_picker.value
        if output_dir == "" or not Path(output_dir).exists():
            print("Must provide an existing output directory")
            return

        self.total_progress = float(len(self.download_list.items))
        self.current_progress = 0.0
        for item in self.download_list.items:
            item.download(
                self.output_directory_picker.value,
                on_progress=self.update_download_progress,
            )

    def initialize_progress_bar(self) -> None:
        self.progress_bar = CTkProgressBar(self)
        self.progress_bar.grid(row=4, column=0, sticky="nsew")
        self.progress_bar.set(0.0)

    def update_download_progress(self, progress: float) -> None:
        self.current_progress += progress
        self.progress_bar.set(self.current_progress / self.total_progress)
