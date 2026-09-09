import sys
from pathlib import Path

# Add MainApp to sys.path
ROOT_DIR = Path(__file__).resolve().parent
MAINAPP_DIR = ROOT_DIR / 'MainApp'
if str(MAINAPP_DIR) not in sys.path:
    sys.path.insert(0, str(MAINAPP_DIR))

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from MainApp.main import main

if __name__ == '__main__':
    main()
