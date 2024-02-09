import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    MainAxisAlignment,
    icons,
    TextField,
    Dropdown,
    dropdown,
    Row,
    Text,
    TextThemeStyle,
    Column,
    Container,
    CrossAxisAlignment,
)
import subprocess
from security import safe_command


def main(page: Page):
    page.title = "Spotify Downloader GUI"
    page.vertical_alignment = MainAxisAlignment.CENTER

    spotify_url = TextField(label="Enter Spotify URL")
    choose_dropdown = Dropdown(
        width=100,
        label="Bitrate",
        options=[
            dropdown.Option("128k"),
            dropdown.Option("160k"),
            dropdown.Option("192k"),
            dropdown.Option("224k"),
            dropdown.Option("256k"),
            dropdown.Option("320k"),
        ],
    )

    def install_spotdl(e):
        command = subprocess.check_output(
            "pip list | grep spotdl | cut -d ' ' -f 1",
            shell=True,
            encoding="utf-8",
        )
        if command != "spotdl":
            safe_command.run(subprocess.run, "pip install spotdl -U", shell=True)
        page.add(
            Row(
                [Text(f"{command}", text_align="center")],
                alignment=MainAxisAlignment.CENTER,
            )
        )
        page.update()

    def choose_bitrate():
        return choose_dropdown.value

    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path or "Cancelled!"
        directory_path.update()
        print(directory_path.value)

    def download(e):
        if not spotify_url.value:
            spotify_url.error_text = "Please enter Spotify link"
            page.update()
        else:
            url = spotify_url.value
            safe_command.run(subprocess.run, f"cd {directory_path.value} && spotdl --preload --bitrate {choose_bitrate()} {url}",
                shell=True,
            )

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    page.overlay.extend([get_directory_dialog])

    page.add(
        Row(
            [
                Container(
                    Text("SPOTIFY DOWNLOADER GUI", style=TextThemeStyle.DISPLAY_MEDIUM)
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                ElevatedButton("INSTALL SPOTDL", on_click=install_spotdl),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Column(
            [
                Container(choose_dropdown),
                Container(spotify_url),
                ElevatedButton("DOWNLOAD SONGS", on_click=download),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
        ),
    )
    page.update()


# flet.app(target=main, view=flet.WEB_BROWSER, port=8080)
flet.app(target=main)
# https://open.spotify.com/album/3MdiH74FL8mhlbnR6DcqJd?si=XjsufJmyS4OwMM9wyIaGwg
