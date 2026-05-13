# ==============================
#       AUTO FILE ORGANIZER
# ==============================

import shutil
import pathlib
import json

# ===== ASK USER FOR VALID TARGET FOLDER =====
while True:
    folder_input = input("Enter folder path to organize (or type 'exit'): ").strip()
    if folder_input.lower() == "exit":
        print("Program terminated.")
        exit()
    target_folder = pathlib.Path(folder_input)
    if target_folder.exists() and target_folder.is_dir():
        break
    print("Invalid folder path. Please try again.\n")

# ===== LOAD / CREATE CONFIG FILE =====
config_file = pathlib.Path("config.json")
if not config_file.exists():
    default_config = {
        "Images":      [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
        "PDFs":        [".pdf"],
        "Videos":      [".mp4", ".mkv", ".avi", ".mov"],
        "Documents":   [".doc", ".docx", ".txt", ".ppt", ".pptx"],
        "Spreadsheets":[".xls", ".xlsx", ".csv"],
        "Executables": [".exe", ".msi"],
        "Compressed":  [".zip", ".rar", ".7z"],
        "Music":       [".mp3", ".wav", ".aac"],
        "Code":        [".py", ".html", ".css", ".js", ".java", ".cpp", ".c"],
        "ML":          [".ipynb"]
    }
    with open(config_file, "w") as f:
        json.dump(default_config, f, indent=4)
    print("Config file created: config.json\n")

with open(config_file, "r") as f:
    file_categories = json.load(f)

default_folder = "Others"

# ===== HANDLE DUPLICATE FILE NAMES =====
def get_unique_name(folder, filename):
    file_path = folder / filename
    if not file_path.exists():
        return filename
    base = file_path.stem
    ext = file_path.suffix
    counter = 1
    while True:
        new_name = f"{base}({counter}){ext}"
        new_path = folder / new_name
        if not new_path.exists():
            return new_name
        counter += 1

# ===== SKIP SYSTEM / TEMP FILES =====
def should_skip(file_path):
    name = file_path.name
    skip_files = ["organizer_log.json", "config.json"]
    if name.startswith("."):      # Hidden files like .DS_Store
        return True
    if name.startswith("~$"):     # Word/Excel temp files
        return True
    if name in skip_files:        # Our own files
        return True
    return False

# ===== UNDO LAST ORGANIZE =====
def undo_last_organize():
    log_file = target_folder / "organizer_log.json"
    if not log_file.exists():
        print("\nNo log file found. Nothing to undo.")
        return
    with open(log_file, "r") as f:
        log = json.load(f)
    if not log:
        print("\nLog is empty. Nothing to undo.")
        return
    print(f"\nRestoring {len(log)} file(s)...\n")
    restored = 0
    for entry in reversed(log):
        src = pathlib.Path(entry["destination"])
        dest = target_folder / entry["file"]
        if src.exists():
            try:
                shutil.move(str(src), str(dest))
                print(f"Restored: {entry['file']}")
                restored += 1
            except Exception as e:
                print(f"Error restoring {entry['file']}: {e}")
        else:
            print(f"File not found (skipped): {entry['file']}")
    # Delete empty folders after undo
    for folder in target_folder.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            print(f"Removed empty folder: {folder.name}")
    # Delete log after undo
    log_file.unlink()
    print(f"\nUndo complete. {restored} file(s) restored.")

# ===== ADD NEW CATEGORY =====
def add_category():
    print("\n--- Add New Category ---")
    name = input("Category name (e.g. Ebooks): ").strip()
    if not name:
        print("Category name cannot be empty.")
        return
    exts_input = input("Extensions separated by space (e.g. .epub .mobi): ").strip()
    if not exts_input:
        print("Extensions cannot be empty.")
        return
    exts = [e if e.startswith(".") else f".{e}" for e in exts_input.split()]
    if name in file_categories:
        file_categories[name].extend(exts)
        file_categories[name] = list(set(file_categories[name]))  # Remove duplicates
        print(f"Updated '{name}' with {exts}")
    else:
        file_categories[name] = exts
        print(f"Added new category '{name}' with {exts}")
    with open(config_file, "w") as f:
        json.dump(file_categories, f, indent=4)
    print("Config saved.")

# ===== SHOW ALL CATEGORIES =====
def show_categories():
    print("\n--- Current Categories ---")
    for category, exts in file_categories.items():
        print(f"{category}: {', '.join(exts)}")
    print()

# ===== MAIN ORGANIZER FUNCTION =====
def organize_files():
    moved_count = 0
    moved_log = []
    category_counts = {}
    preview_moves = []

    # ===== ASK ABOUT SUBFOLDERS =====
    sub_choice = input("\nInclude files inside subfolders? (yes/no): ").strip().lower()
    if sub_choice == "yes":
        all_files = [f for f in target_folder.rglob("*") if f.is_file()]
    else:
        all_files = [f for f in target_folder.iterdir() if f.is_file()]

    print(f"\nScanning Folder: {target_folder}\n")

    # ===== PREVIEW MOVES =====
    for file_path in all_files:
        if should_skip(file_path):
            continue
        filename = file_path.name
        extension = file_path.suffix.lower()
        matched = False
        for category, extensions in file_categories.items():
            if extension in extensions:
                preview_moves.append((filename, category))
                matched = True
                break
        if not matched:
            preview_moves.append((filename, default_folder))

    # ===== IF NO FILES FOUND =====
    if not preview_moves:
        print("No files found to organize.")
        return

    # ===== SHOW PREVIEW =====
    print("Preview of Files to Move:\n")
    for file, destination in preview_moves:
        print(f"  {file}  →  {destination}")

    # ===== CONFIRMATION =====
    confirm = input("\nProceed with moving files? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return

    # ===== MOVE FILES =====
    for file_path in all_files:
        if should_skip(file_path):
            continue
        filename = file_path.name
        extension = file_path.suffix.lower()
        matched = False
        for category, extensions in file_categories.items():
            if extension in extensions:
                category_folder = target_folder / category
                category_folder.mkdir(exist_ok=True)
                unique_name = get_unique_name(category_folder, filename)
                destination = category_folder / unique_name
                try:
                    shutil.move(str(file_path), str(destination))
                    print(f"Moved: {filename}  →  {category}")
                    moved_count += 1
                    category_counts[category] = category_counts.get(category, 0) + 1
                    moved_log.append({"file": filename, "destination": str(destination)})
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
                matched = True
                break
        if not matched:
            other_folder = target_folder / default_folder
            other_folder.mkdir(exist_ok=True)
            unique_name = get_unique_name(other_folder, filename)
            destination = other_folder / unique_name
            try:
                shutil.move(str(file_path), str(destination))
                print(f"Moved: {filename}  →  {default_folder}")
                moved_count += 1
                category_counts[default_folder] = category_counts.get(default_folder, 0) + 1
                moved_log.append({"file": filename, "destination": str(destination)})
            except Exception as e:
                print(f"Error moving {filename}: {e}")

    # ===== REMOVE EMPTY FOLDERS =====
    for folder in target_folder.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            print(f"Removed empty folder: {folder.name}")

    # ===== SAVE LOG =====
    if moved_log:
        log_file = target_folder / "organizer_log.json"
        with open(log_file, "w") as f:
            json.dump(moved_log, f, indent=4)
        print(f"\nLog saved to: {log_file}")
    else:
        print("\nNo files moved. No log file created.")

    # ===== FINAL SUMMARY =====
    print("\n==============================")
    print("      ORGANIZATION COMPLETE")
    print("==============================")
    print(f"\nTotal Files Moved: {moved_count}\n")
    if category_counts:
        print("Files Per Category:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} file(s)")

# ===== MAIN MENU =====
def main_menu():
    while True:
        print("\n==============================")
        print("      AUTO FILE ORGANIZER")
        print("==============================")
        print("1. Organize Files")
        print("2. Undo Last Organize")
        print("3. Add / Update Category")
        print("4. View All Categories")
        print("5. Exit")
        print("==============================")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            organize_files()
        elif choice == "2":
            undo_last_organize()
        elif choice == "3":
            add_category()
        elif choice == "4":
            show_categories()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 to 5.")

# ===== RUN =====
if __name__ == "__main__":
    main_menu()