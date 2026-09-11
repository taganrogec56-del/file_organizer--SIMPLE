import shutil
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


def get_unique_filename(folder: Path, file_path: Path) -> Path | None:
    new_path = folder / file_path.name
    try:
        if not new_path.exists():
            return new_path
    except OSError as error:
        print(f'Ошибка системы {error}')

    i = 1
    scan_errors = 0
    while True:
        print('Попытка подобрать новое имя:')
        new_name = file_path.stem + f'_{i}' + file_path.suffix
        new_path = folder / new_name
        try:
            if not new_path.exists():
                print(f'Новое имя: {new_path.resolve()}')
                return new_path
        except OSError as error:
            scan_errors += 1
            i += 1
            if scan_errors <= 9:
                print(f'Ошибка системы {error}')
                continue
            else:
                print(f'Ошибка системы {error}')
                print(f'Подобрать новое имя для {file_path.name} не удалось')
                return None
        i += 1


def move_file(old_path: Path, new_path: Path) -> bool:
    try:
        shutil.move(old_path, new_path)
        return True
    except OSError as error:
        print(f'Произошла ошибка: {error}')
        return False


def show_report(
        moved_counter: int,
        moved_dict: dict | None,
        scan_errors: int,
) -> None:
    if moved_dict is None:
        if scan_errors:
            print('Из-за ошибок не удалось определить, есть ли файлы для сортировки')
        else:
            print('В папке нет файлов для сортировки')
    else:
        for cat, count in moved_dict.items():
            print(f'В категории {cat} перенесено {count} файлов')
        print(f'Всего перенесено: {moved_counter} файлов')

        if moved_counter == 0:
            print('Файлы есть, но ни один не перемещён')

    if scan_errors:
        print(f'Ошибок при чтении папки и проверке объектов: {scan_errors}')


def organize_files(path_folder: Path):
    scan_errors = 0
    try:
        items_from_folder = list(path_folder.iterdir())
    except OSError as error:
        print(f'Не удалось прочитать папку: {error}')
        return 0, None, 1

    files_from_folder = []
    for item in items_from_folder:
        try:
            if item.is_file():
                files_from_folder.append(item)
        except OSError as error:
            print(f'Не удалось проверить {item.name}: {error}')
            scan_errors += 1

    if not files_from_folder:
        return 0, None, scan_errors

    moved_counter = 0
    moved_dict = {}
    for file_path in files_from_folder:
        category = get_category(file_path.suffix)
        new_folder = create_category_folder(path_folder, category)

        if new_folder is not None:
            unique_filename_path = get_unique_filename(new_folder, file_path)
            if unique_filename_path is not None:

                move_status = move_file(file_path, unique_filename_path)
                if move_status:
                    print(f'{file_path.name} успешно перенесён в {unique_filename_path}')
                    moved_counter += 1
                    if category not in moved_dict:
                        moved_dict[category] = 1
                    else:
                        moved_dict[category] += 1
    return moved_counter, moved_dict, scan_errors


def main():
    while True:
        path = input('Введите путь к папке: ').strip()
        path_folder = get_folder_path(path)
        if path_folder is not None:
            print('Путь принят')
            user_answer = input(f'Будет обработана папка: {path_folder}\n'
                                f'Файлы будут распределены по подпапкам категорий.\n'
                                f'Начать сортировку? (y/n): ').strip().lower()
            if user_answer == 'y':
                moved_counter, moved_dict, scan_errors = organize_files(path_folder)
                show_report(moved_counter, moved_dict, scan_errors)
                break
            print('Сортировка отменена. До свидания.')
            return


if __name__ == '__main__':
    main()
