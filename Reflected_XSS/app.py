"""
Root Runner for XSS Security Lab
Allows executing the application directly from the root workspace directory:
    python app.py
"""
import os
import sys
from pathlib import Path

# Set working directory and module path to XSS-Security-Lab
BASE_DIR = Path(__file__).resolve().parent / "XSS-Security-Lab"
sys.path.insert(0, str(BASE_DIR))
os.chdir(BASE_DIR)

from app import app

if __name__ == '__main__':
    print("=" * 70)
    print(" Starting XSS Security Lab from root workspace...")
    print(" Local address: http://127.0.0.1:5000")
    print("=" * 70)
    app.run(host='127.0.0.1', port=5000, debug=True)
