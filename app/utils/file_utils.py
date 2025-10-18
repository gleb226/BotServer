import os
from app.common.config import main_categories, USER_FILES_DIR


def get_folder_path(user_id, category, subcategory_path=None):
    category_path = main_categories[category]["path"]
    full_path = os.path.join(USER_FILES_DIR, str(user_id), category_path)

    if subcategory_path:
        if isinstance(subcategory_path, list):
            for subcat in subcategory_path:
                full_path = os.path.join(full_path, subcat)
        else:
            full_path = os.path.join(full_path, subcategory_path)

    return full_path


def get_user_files(user_id, category, subcategory_path=None):
    full_path = get_folder_path(user_id, category, subcategory_path)

    if not os.path.exists(full_path):
        return []

    files = []
    for file in os.listdir(full_path):
        file_path = os.path.join(full_path, file)
        if os.path.isfile(file_path):
            files.append(file)

    return sorted(files)


def delete_file(user_id, category, subcategory_path, filename):
    try:
        full_path = get_folder_path(user_id, category, subcategory_path)
        file_path = os.path.join(full_path, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False


def delete_all_files(user_id, category, subcategory_path=None):
    try:
        full_path = get_folder_path(user_id, category, subcategory_path)

        if not os.path.exists(full_path):
            return 0

        files = get_user_files(user_id, category, subcategory_path)
        deleted_count = 0

        for file in files:
            file_path = os.path.join(full_path, file)
            try:
                os.remove(file_path)
                deleted_count += 1
            except:
                pass

        return deleted_count
    except Exception:
        return 0


def save_text_to_file(user_id, category, subcategory_path, text):
    full_path = get_folder_path(user_id, category, subcategory_path)
    os.makedirs(full_path, exist_ok=True)

    file_path = os.path.join(full_path, f"{category}.txt")

    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(text + "\n")


def is_valid_file_extension(category, extension):
    allowed_extensions = main_categories[category]["extensions"]
    return extension in allowed_extensions