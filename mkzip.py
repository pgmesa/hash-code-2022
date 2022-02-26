
import os
from pathlib import Path
from zipfile import ZipFile

submission_path = Path('submission.zip').resolve()
files_to_submit = ['solver.py', 'classes.py', 'requirements.txt']

def mkzip():
    if os.path.exists(submission_path):
        print("Deleting last submission...")
        os.remove(submission_path)
    print("Creating submission .zip file...")
    zipObj = ZipFile(submission_path, 'w')
    # Add the files
    for file in files_to_submit:
        zipObj.write(file)
    # Close the Zip file
    zipObj.close()
    print(f"Done!! -> {submission_path}")

if __name__ == "__main__":
    mkzip()