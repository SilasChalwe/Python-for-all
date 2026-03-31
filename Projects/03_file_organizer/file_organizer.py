"""
Project — File Organizer
==========================
Automatically sorts files into categorized subfolders.

Features:
  - Sort by file extension
  - Dry-run mode (preview without moving)
  - Undo last organization
  - Detailed logging
  - Custom category mappings

Skills: os, shutil, pathlib, argparse, logging, JSON
"""

import os
import shutil
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Extension → category mapping
EXTENSION_MAP = {
    # Images
    ".jpg":  "Images",  ".jpeg": "Images",  ".png":  "Images",
    ".gif":  "Images",  ".bmp":  "Images",  ".svg":  "Images",
    ".webp": "Images",  ".tiff": "Images",  ".ico":  "Images",
    # Documents
    ".pdf":  "Documents", ".doc":  "Documents", ".docx": "Documents",
    ".txt":  "Documents", ".odt":  "Documents", ".xlsx": "Documents",
    ".xls":  "Documents", ".csv":  "Documents", ".pptx": "Documents",
    ".md":   "Documents", ".rtf":  "Documents",
    # Videos
    ".mp4":  "Videos",  ".avi":  "Videos",  ".mov":  "Videos",
    ".mkv":  "Videos",  ".wmv":  "Videos",  ".flv":  "Videos",
    ".webm": "Videos",
    # Audio
    ".mp3":  "Audio",   ".wav":  "Audio",   ".flac": "Audio",
    ".aac":  "Audio",   ".ogg":  "Audio",   ".m4a":  "Audio",
    # Code
    ".py":   "Code",    ".js":   "Code",    ".ts":   "Code",
    ".html": "Code",    ".css":  "Code",    ".java": "Code",
    ".cpp":  "Code",    ".c":    "Code",    ".go":   "Code",
    ".rs":   "Code",    ".rb":   "Code",    ".php":  "Code",
    ".sh":   "Code",    ".sql":  "Code",    ".json": "Code",
    ".yaml": "Code",    ".yml":  "Code",    ".toml": "Code",
    # Archives
    ".zip":  "Archives", ".tar":  "Archives", ".gz":   "Archives",
    ".7z":   "Archives", ".rar":  "Archives", ".bz2":  "Archives",
    # Executables
    ".exe":  "Executables", ".msi": "Executables", ".dmg": "Executables",
    ".deb":  "Executables", ".rpm": "Executables",
}

DEFAULT_CATEGORY = "Other"
UNDO_LOG_FILE    = ".organizer_undo.json"


class FileOrganizer:
    """Organizes files in a directory into categorized subfolders."""

    def __init__(self, target_dir: str, extension_map: dict = None):
        self.target_dir    = Path(target_dir).resolve()
        self.extension_map = extension_map or EXTENSION_MAP
        self.undo_log_path = self.target_dir / UNDO_LOG_FILE

    def get_category(self, filepath: Path) -> str:
        """Return the category for a given file path."""
        ext = filepath.suffix.lower()
        return self.extension_map.get(ext, DEFAULT_CATEGORY)

    def _gather_files(self) -> list:
        """Return all files in target_dir (non-recursive, non-hidden)."""
        files = []
        for item in self.target_dir.iterdir():
            if item.is_file() and not item.name.startswith("."):
                files.append(item)
        return files

    def preview(self) -> dict:
        """Return a dict of {category: [filename, ...]} without moving files."""
        plan = defaultdict(list)
        for filepath in self._gather_files():
            cat = self.get_category(filepath)
            plan[cat].append(filepath.name)
        return dict(plan)

    def organize(self, dry_run: bool = False) -> dict:
        """
        Move files into category subfolders.

        Args:
            dry_run: If True, log actions but don't move any files.

        Returns:
            Dict of {category: count} showing files moved per category.
        """
        files = self._gather_files()
        if not files:
            print("  📭 No files to organize.")
            return {}

        results  = defaultdict(int)
        undo_log = []

        print(f"\n  {'DRY RUN — ' if dry_run else ''}Organizing {len(files)} files...")
        print("  " + "-" * 50)

        for filepath in sorted(files):
            cat       = self.get_category(filepath)
            cat_dir   = self.target_dir / cat
            dest_path = cat_dir / filepath.name

            # Handle filename collisions
            if dest_path.exists() and not dry_run:
                stem = filepath.stem
                suf  = filepath.suffix
                ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
                dest_path = cat_dir / f"{stem}_{ts}{suf}"

            action = "Would move" if dry_run else "Moving"
            print(f"  {action}: {filepath.name} → {cat}/")

            if not dry_run:
                cat_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(filepath), str(dest_path))
                undo_log.append({
                    "original": str(filepath),
                    "moved_to": str(dest_path),
                })

            results[cat] += 1

        if not dry_run and undo_log:
            with open(self.undo_log_path, "w") as f:
                json.dump(undo_log, f, indent=2)
            print(f"\n  Undo log saved: {self.undo_log_path}")

        print("\n  Summary:")
        for cat, count in sorted(results.items()):
            print(f"    {cat:<15} {count} file(s)")

        total = sum(results.values())
        print(f"\n  {'Would organize' if dry_run else 'Organized'} {total} files.")
        return dict(results)

    def undo(self):
        """Move files back to their original locations using the undo log."""
        if not self.undo_log_path.exists():
            print("  ⚠️  No undo log found. Nothing to undo.")
            return

        with open(self.undo_log_path, "r") as f:
            undo_log = json.load(f)

        print(f"\n  Undoing {len(undo_log)} file move(s)...")
        errors = 0

        for entry in undo_log:
            src  = Path(entry["moved_to"])
            dest = Path(entry["original"])

            if not src.exists():
                print(f"  ⚠️  Not found: {src.name} (may have been moved/deleted)")
                errors += 1
                continue

            print(f"  Restoring: {src.name} → {dest.parent.name}/")
            shutil.move(str(src), str(dest))

        # Remove empty category folders
        for item in self.target_dir.iterdir():
            if item.is_dir() and not any(item.iterdir()):
                item.rmdir()
                print(f"  Removed empty folder: {item.name}/")

        self.undo_log_path.unlink()
        print(f"\n  Undo complete. {len(undo_log) - errors} files restored.")


def parse_args():
    parser = argparse.ArgumentParser(description="Organize files into categorized folders.")
    parser.add_argument("directory",  nargs="?",    default=".",
                        help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run",  action="store_true",
                        help="Preview changes without moving files")
    parser.add_argument("--undo",     action="store_true",
                        help="Undo the last organization")
    parser.add_argument("--preview",  action="store_true",
                        help="Show what would be organized")
    return parser.parse_args()


def main():
    args      = parse_args()
    organizer = FileOrganizer(args.directory)

    print("=" * 50)
    print("  📁  FILE ORGANIZER")
    print("=" * 50)
    print(f"  Target: {organizer.target_dir}")

    if args.undo:
        organizer.undo()
    elif args.preview:
        plan = organizer.preview()
        print("\n  Preview:")
        for cat, files in sorted(plan.items()):
            print(f"  {cat}/  ({len(files)} files)")
            for f in files[:5]:
                print(f"    - {f}")
            if len(files) > 5:
                print(f"    ... and {len(files) - 5} more")
    else:
        organizer.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
