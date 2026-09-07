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
    try:
        path_folder = Path(path).resolve()
        if not path_folder.exists():
            print('Ошибка: указанная папка не существует')
            return None
        if not path_folder.is_dir():
            print('Ошибка: указанный путь не является папкой')
            return None
        return path_folder
    except OSError as error:
        print(f'Системная ошибка: {error}')
        return None


def get_category(suffix: str) -> str:
    suffix = suffix.lower()
    for category, exts in FILE_CATEGORIES.items():
        if suffix in exts:
            return category
    return 'Other'


def main():
    while True:
        path = input('Введите путь к папке: ').strip()
        path_folder = get_folder_path(path)
        if path_folder is not None:
            print('Путь принят')
            try:
                files_from_folder = path_folder.iterdir()
                for file_path in files_from_folder:
                    if file_path.is_file():
                        category = get_category(file_path.suffix)
                        print(category)
            except OSError as error:
                print(f'Системная ошибка: {error}')
                continue
            break


if __name__ == '__main__':
    main()
