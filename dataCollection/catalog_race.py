from pathlib import Path


def renameFiles(sourceFile, newFileName):
    # Ensure the file exists
    if not sourceFile.is_file():
        print(f"Folder does not exist.")
        return

    # Get the file's parent directory and extension
    parentDir = sourceFile.parent
    fileExtension = sourceFile.suffix

    newName = newFileName + fileExtension  # Create the new file name with the desired name and extension

    newPath = parentDir / newName  # Construct the new path with the renamed file

    # Rename the file
    sourceFile.rename(newPath)
    print(f"Renamed '{sourceFile.name}' to '{newName}'.")
    return newPath

def moveFiles(sourceFile, destinationFolder):

    destinationPath = Path(destinationFolder)  # create path object to destination folder

    # Ensure both source and destination paths exist
    if not sourceFile.is_file():
        print(f"Source file does not exist.")
        return

    # create directory if it does not exist
    if not destinationPath.is_dir():
        destinationPath.mkdir(parents=True)

    # Move files from source to destination folder
    sourceFile.rename(destinationPath / sourceFile.name)
    print(f"Moved file '{sourceFile.name}' to '{destinationFolder}'.")