# Auto File Organizer 📁

A Python automation application that automatically 
organizes files into categorized folders based on 
file type. Features undo support, preview mode, 
custom categories and detailed logging.

---

## Features

- ✅ Auto organizes files by type into folders
- ✅ Preview files before moving — confirm first!
- ✅ Undo last organize — restores all files back
- ✅ Custom categories — add your own file types
- ✅ Duplicate file handling — no overwriting
- ✅ Subfolder support — organize recursively
- ✅ Log file — tracks all moves to JSON
- ✅ Skips system and hidden files automatically
- ✅ Removes empty folders after organizing
- ✅ Summary report — shows files per category
- ✅ JSON config file — fully customizable

---

## Default Categories

| Category | Extensions |
|----------|------------|
| Images | .jpg .jpeg .png .gif .bmp .webp |
| PDFs | .pdf |
| Videos | .mp4 .mkv .avi .mov |
| Documents | .doc .docx .txt .ppt .pptx |
| Spreadsheets | .xls .xlsx .csv |
| Executables | .exe .msi |
| Compressed | .zip .rar .7z |
| Music | .mp3 .wav .aac |
| Code | .py .html .css .js .java .cpp .c |
| ML | .ipynb |
| Others | Everything else |

---

## Menu Options

| Option | Description |
|--------|-------------|
| 1 | Organize Files |
| 2 | Undo Last Organize |
| 3 | Add / Update Category |
| 4 | View All Categories |
| 5 | Exit |

---

## How to Run

1. Clone the repository:
git clone https://github.com/Mansoor-Mir1/FileOrganizer.git
cd FileOrganizer

2. Run the program:
python fileOrganizer.py

3. Enter folder path to organize

4. Preview files and confirm to proceed

---

## How It Works

1. User enters folder path
2. App scans all files in folder
3. Shows preview of where each file will move
4. User confirms — files move to category folders
5. Log saved for undo support
6. Summary shown at the end

---

## Technologies Used

- Python 3
- pathlib — modern file handling
- shutil — file moving
- json — config and logging
- No external dependencies required

---

## Author

Muhammad Mansoor
🔗 github.com/Mansoor-Mir1
