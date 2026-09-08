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
        path_folder: Path = Path(path).resolve()
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


def create_category_folder(path_folder: Path, category: str) -> Path | None:
    new_folder_path = path_folder / category
    try:
        new_folder_path.mkdir(exist_ok=True)
        return new_folder_path
    except OSError as error:
        print(f'Ошибка системы: {error}')
        return None


def main():
    while True:
        path = input('Введите путь к папке: ').strip()
        path_folder = get_folder_path(path)
        if path_folder is not None:
            print('Путь принят')
            user_answer = input(f' Будет обработана папка: {path_folder}\n'
                                f'Файлы будут распределены по подпапкам категорий.\n'
                                f'Начать сортировку? (y/n):\n').strip().lower()
            if user_answer == 'y':
                try:
                    files_from_folder = path_folder.iterdir()
                    for file_path in files_from_folder:
                        if file_path.is_file():
                            category = get_category(file_path.suffix)

                            new_folder = create_category_folder(path_folder, category)
                            if new_folder is not None:
                                print('TODO: Переместить файлы в новую папку')

                except OSError as error:
                    print(f'Системная ошибка: {error}')
                    continue
                break
            print('Сортировка отменена. До свидания.')
            return


if __name__ == '__main__':
    main()
