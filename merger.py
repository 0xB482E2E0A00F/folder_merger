#! python3

import sys
import os
import shutil
import msvcrt
from log_config import setup_logger
from keypress import wait_for_keypress

logger = setup_logger(merged_folder)

def validate_folders(folders):
    logger.debug("Validate the list of selected folders")
    if len(folders) <= 1:
        raise ValueError("Please provide at least one directory.")
    else:
        for folder in folders:
            if not os.path.isdir(folder):
                raise ValueError(f"{folder} is not a valid directory.")
    logger.debug("Get the list of selected folders")
    return folders

def select_destination_folder(selected_folders):
    while True:
        try:
            for i, folder in enumerate(selected_folders):
                logger.info(f"{i}: {folder}")
            correct_index = int(input("Enter the index of the correct destination folder:"))
            if correct_index < 0 or correct_index >= len(selected_folders):
                raise ValueError
            return selected_folders[correct_index]
        except ValueError:
            logger.error("Invalid index entered. Please enter a valid index.")

def check_and_select_destination_folder(selected_folders):
    logger.debug("check that the first folder is the correct folder")
    dst_dir = selected_folders[0]
    destination_folder_confirmation  = input(f"Is {dst_dir} the correct destination folder? (y/n)")
    if destination_folder_confirmation.lower() == "y":
        return dst_dir
    else:
        return select_destination_folder(selected_folders)

def create_destination_folder(dst_dir):
    logger.debug("Create the destination directory if it doesn't exist")
    try:
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
            logger.debug(f"Destination folder {dst_dir} created.")
        else:
            logger.debug(f"Destination folder {dst_dir} already exists.")
    except Exception as e:
        raise ValueError(f"Error occured while creating destination folder: {e}")

def copy_file_to_dest(src_path, dst_path):
    if os.path.exists(dst_path):
        base_name, file_extension = os.path.splitext(dst_path)
        i = 1
        new_dst_path = f"{base_name}({i}){file_extension}"
        while os.path.exists(new_dst_path):
            i += 1
            new_dst_path = f"{base_name}({i}){file_extension}"
        dst_path = new_dst_path
    try:
        shutil.copy2(src_path, dst_path)
        logger.debug(f"Copied {os.path.basename(src_path)} to {os.path.dirname(dst_path)}.")
    except Exception as e:
        logger.error(f"Error occured: {e}")

def copy_files_to_destination(selected_folders, dst_dir):
    for folder in selected_folders[1:]:
        logger.debug(f"Processing folder {folder}")
        for subdir, dirs, files in os.walk(folder):
            for file in files:
                src_path = os.path.join(subdir, file)
                dst_path = os.path.join(dst_dir, file)
                copy_file_to_dest(src_path, dst_path)

def main():
    try:
        selected_folders = validate_folders(sys.argv[1:])

        dst_dir = check_and_select_destination_folder(selected_folders)

        create_destination_folder(dst_dir)

        copy_files_to_destination(selected_folders, dst_dir)
        logger.info("All images were successfully combined into one folder.")

    except Exception as e:
        logger.error(f"Error occured: {e}")

    wait_for_keypress()

if __name__ == "__main__":
    main()
