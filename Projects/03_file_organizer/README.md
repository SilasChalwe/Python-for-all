# 📁 File Organizer

Automatically organize files in a directory by sorting them into subfolders based on their file type.

## Features
- Sort files by extension into categorized subfolders
- Dry-run mode (preview changes without moving files)
- Undo functionality (move files back)
- Custom extension-to-category mapping
- Detailed operation log

## Usage
```bash
# Organize current directory (dry run first!)
python file_organizer.py --dry-run /path/to/folder

# Actually organize
python file_organizer.py /path/to/folder

# Undo last organization
python file_organizer.py --undo /path/to/folder
```

## Categories
| Folder | Extensions |
|--------|-----------|
| Images/ | .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp |
| Documents/ | .pdf, .doc, .docx, .txt, .odt, .xlsx, .csv |
| Videos/ | .mp4, .avi, .mov, .mkv, .wmv |
| Audio/ | .mp3, .wav, .flac, .aac, .ogg |
| Code/ | .py, .js, .ts, .html, .css, .java, .cpp |
| Archives/ | .zip, .tar, .gz, .7z, .rar |
| Other/ | everything else |
