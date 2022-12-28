from flet import *
from alive_progress import alive_bar
import subprocess


def main(page: Page):
    page.title = "Spotify Downloader GUI"
    page.vertical_alignment = MainAxisAlignment.CENTER

    folder_name = TextField(label="Enter folder name")
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
            subprocess.run("pip install spotdl -U", shell=True)
        page.add(
            Row(
                [Text(f"{command}", text_align="center")],
                alignment=MainAxisAlignment.CENTER,
            )
        )
        page.update()

    def create_folder(e):
        if not folder_name.value:
            folder_name.error_text = "Please enter folder name"
            page.update()
        else:
            name = folder_name.value
            if os.path.exists(name):
                folder_name.error_text = "Folder already exists"
            else:
                subprocess.run(f"mkdir {name}", shell=True)
                page.add(
                    Row(
                        [Text(f"Folder {name} created")],
                        alignment=MainAxisAlignment.CENTER,
                    )
                )
            page.update()

    def choose_bitrate():
        return choose_dropdown.value

    def download(e):
        if not spotify_url.value:
            spotify_url.error_text = "Please enter Spotify link"
            page.update()
        else:
            url = spotify_url.value
            subprocess.run(
                f"cd {folder_name.value} && spotdl --preload --bitrate {choose_bitrate()} {url}",
                shell=True,
            )

    page.add(
        Row(
            [
                ElevatedButton("INSTALL", on_click=install_spotdl),
                Text(value="Install spotdl package", text_align="center", width=150),
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [ElevatedButton("CREATE FOLDER", on_click=create_folder), folder_name],
            alignment=MainAxisAlignment.CENTER,
        ),
        Row(
            [
                ElevatedButton("DOWNLOAD SONGS", on_click=download),
                choose_dropdown,
                spotify_url,
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    )
    page.update()


# app(target=main, view=WEB_BROWSER, port=8080)
app(target=main)
# https://open.spotify.com/album/3MdiH74FL8mhlbnR6DcqJd?si=XjsufJmyS4OwMM9wyIaGwg
