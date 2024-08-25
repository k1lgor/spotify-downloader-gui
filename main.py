import os
import subprocess
import sys

import flet as ft


def check_and_install_spotdl():
    try:
        # Check if spotdl is installed
        subprocess.run(
            ["spotdl", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        # spotdl is not installed
        return False


def install_spotdl():
    # Install spotdl using pip
    subprocess.run([sys.executable, "-m", "pip", "install", "spotdl"], check=True)


def download_album(url, bitrate, save_dir):
    # Ensure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Construct the spotdl command
    command = [
        "spotdl",
        "--output",
        os.path.join(save_dir),
        "--audio",
        "youtube",
        "--bitrate",
        bitrate,
        url,
    ]

    # Run the command
    subprocess.run(command)


def main(page: ft.Page):
    page.title = "Spotify Album Downloader"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.theme = ft.Theme(
        color_scheme_seed="indigo",
    )

    page.theme_mode = ft.ThemeMode.SYSTEM

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    theme_toggle = ft.IconButton(
        ft.icons.LIGHT_MODE,
        selected=False,
        selected_icon=ft.icons.DARK_MODE,
        on_click=toggle_theme,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Spotify Album Downloader"),
        center_title=True,
        actions=[theme_toggle],
    )

    def on_result(e):
        save_dir_input.value = e.path or ""
        page.update()

    url_input = ft.TextField(label="Spotify Album URL", width=600)
    bitrate_input = ft.Dropdown(
        label="Select Bitrate",
        width=600,
        options=[
            ft.dropdown.Option("128k", "128 kbps"),
            ft.dropdown.Option("192k", "192 kbps"),
            ft.dropdown.Option("256k", "256 kbps"),
            ft.dropdown.Option("320k", "320 kbps"),
        ],
    )
    save_dir_input = ft.TextField(
        label="Save Directory",
        width=600,
        disabled=False,
    )

    file_picker = ft.FilePicker(on_result=on_result)

    choose_dir_button = ft.ElevatedButton(
        text="Choose Directory",
        on_click=lambda e: file_picker.get_directory_path(),
    )

    def start_download(e):
        if not check_and_install_spotdl():
            page.snack_bar = ft.SnackBar(ft.Text("spotdl not found. Installing..."))
            page.snack_bar.open = True
            page.update()

            install_spotdl()

            page.snack_bar = ft.SnackBar(
                ft.Text("spotdl installed successfully!"),
                open=True,
            )
            page.update()

        download_album(
            url_input.value,
            bitrate_input.value,
            save_dir_input.value,
        )

    download_button = ft.ElevatedButton(
        text="Download Album",
        on_click=start_download,
    )

    page.add(
        url_input,
        bitrate_input,
        save_dir_input,
        choose_dir_button,
        download_button,
        file_picker,
    )


ft.app(target=main)
