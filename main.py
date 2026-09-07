from pathlib import Path

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"],
    "Documents": [
        ".txt",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".csv",
    ],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".webm"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".md"],
}


def get_folder_path(path: str) -> Path | None:
    path_folder = Path(path).resolve()
    if not path_folder.exists():
        print('Ошибка: указанная папка не существует')
        return
    if not path_folder.is_dir():
        print('Ошибка: указанный путь не является папкой')
        return
    return path_folder


def main():
    while True:
        path = input('Введите путь к папке: ').strip()
        path_folder = get_folder_path(path)
        if path_folder is not None:
            print('Путь принят')
            break


if __name__ == '__main__':
    main()
