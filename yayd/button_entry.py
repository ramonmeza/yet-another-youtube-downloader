from typing import Any, Callable, Optional
from customtkinter import CTkFrame, CTkEntry, CTkButton, StringVar


class ButtonEntry(CTkFrame):
    """A `ButtonEntry` is a `CTkFrame` that is composed of a `CTkEntry` and a
    `CTkButton`.

    It provides a way for users to submit input entry after pressing a button.
    """

    text_variable: StringVar
    entry: CTkEntry
    button: CTkButton
    _button_command: Optional[Callable[[str], None]]

    def __init__(
        self,
        master: Any,
        placeholder_text: str,
        button_text: str,
        command: Optional[Callable[[str], None]] = None,
        **kwargs
    ):
        super().__init__(
            master, bg_color="transparent", fg_color="transparent", **kwargs
        )
        # configure grid
        self.grid_columnconfigure(0, weight=9)
        self.grid_columnconfigure(1, weight=1)

        # define text variable for holding the user input text
        self.text_variable = StringVar()

        # entry is used to provide an interface for the user to the text_variable
        self.entry = CTkEntry(
            self, placeholder_text=placeholder_text, textvariable=self.text_variable
        )
        self.entry.grid(row=0, column=0, sticky="nsew")

        # if the user provides their own button command
        self._button_command = command

        # button allows users to "submit" their string, once they are complete
        self.button = CTkButton(self, text=button_text, command=self._button_callback)
        self.button.grid(row=0, column=1, sticky="nsew")

    def _button_callback(self) -> None:
        # since CTkButton command doesn't provide a string, we use our own callback
        # to give users the entry text value
        if self._button_command is not None:
            self._button_command(self.value)

    @property
    def value(self) -> str:
        return self.text_variable.get()

    def set_text(self, text: str) -> None:
        self.text_variable.set(text)
