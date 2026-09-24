from pathlib import Path

from pyforge.tools.files.core import directory_statistics, find_large_files

root = Path.cwd()
print(directory_statistics(root))
print(find_large_files(root, minimum_bytes=10_000_000))
