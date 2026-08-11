"""Build dist/cwah.exe on Windows after installing the dev extra."""

import PyInstaller.__main__

PyInstaller.__main__.run(
    ["--onefile", "--name", "cwah", "--collect-all", "pyperclip", "src/cwah/cli.py"]
)
