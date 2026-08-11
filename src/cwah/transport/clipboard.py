from __future__ import annotations

from typing import Protocol

import pyperclip


class ClipboardError(RuntimeError):
    pass


class Clipboard(Protocol):
    def copy(self, text: str) -> None: ...
    def paste(self) -> str: ...


class SystemClipboard:
    def copy(self, text: str) -> None:
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException as exc:
            raise ClipboardError(str(exc)) from exc

    def paste(self) -> str:
        try:
            return str(pyperclip.paste())
        except pyperclip.PyperclipException as exc:
            raise ClipboardError(str(exc)) from exc

    def available(self) -> bool:
        try:
            pyperclip.copy("")
            return True
        except pyperclip.PyperclipException:
            return False


class MemoryClipboard:
    def __init__(self, value: str = ""):
        self.value = value

    def copy(self, text: str) -> None:
        self.value = text

    def paste(self) -> str:
        return self.value
