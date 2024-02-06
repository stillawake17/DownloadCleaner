import os
import shutil

# Define default file categories and their corresponding extensions and target directories
default_file_categories = {
    'Documents': {'extensions': ['.doc', '.docx', '.pdf', '.txt', '.rtf', '.odt'], 'target_dir': 'Documents'},
    'Images': {'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'], 'target_dir': 'Images'},
    'Videos': {'extensions': ['.mp4', '.mkv', '.mov', '.avi'], 'target_dir': 'Videos'},
    'Music': {'extensions': ['.mp3', '.wav', '.aac'], 'target_dir': 'Music'},
    # Add more categories as needed
}

user_defined_categories = {
    'Programming': {'extensions': ['.py', '.js'], 'target_dir': 'Code'},
    'Documents': {'extensions': ['.md'], 'target_dir': 'Markdown_Docs'},  # This will add .md to Documents and update its target directory
}

import os

def list_file_extensions(directory):
    """
    List all unique file extensions in the given directory.

    :param directory: Path to the directory to scan.
    :return: A set of unique file extensions.
    """
    extensions = set()
    for filename in os.listdir(directory):
        # Ignore directories
        if os.path.isfile(os.path.join(directory, filename)):
            _, ext = os.path.splitext(filename)
            if ext:  # Ensure there is an extension
                extensions.add(ext.lower())  # Add extension in lowercase to ensure uniqueness
    return extensions




def shorten_filename(filename, max_length=150):
    """Shortens a filename if it exceeds the given max_length, preserving the file extension."""
    name, ext = os.path.splitext(filename)
    if len(name) > max_length - len(ext) - 3:
        name = name[:max_length - len(ext) - 3] + "..."
    return name + ext

def merge_categories(defaults, user_provided):
    """Merges user-provided categories with default categories."""
    for category, details in user_provided.items():
        if category in defaults:
            # Update extensions and remove duplicates
            defaults[category]['extensions'] = list(set(defaults[category]['extensions'] + details.get('extensions', [])))
            # Update target directory if provided
            if 'target_dir' in details:
                defaults[category]['target_dir'] = details['target_dir']
        else:
            defaults[category] = details
    return defaults

def sort_downloads(downloads_path, user_categories={}):
    """Sorts files in the downloads directory based on merged categories."""
    merged_categories = merge_categories(default_file_categories.copy(), user_categories)
    processed_files = []

    # Ensure the target directories exist
    for details in merged_categories.values():
        os.makedirs(os.path.join(downloads_path, details['target_dir']), exist_ok=True)

    # Iterate over each file in the downloads directory
    for filename in os.listdir(downloads_path):
        filepath = os.path.join(downloads_path, filename)
        if os.path.isfile(filepath):
            file_extension = os.path.splitext(filename)[1].lower()
            destination_folder = None
            for category, details in merged_categories.items():
                if file_extension in details['extensions']:
                    destination_folder = details['target_dir']
                    break
            
            if destination_folder:
                new_filename = shorten_filename(filename)
                new_path = os.path.join(downloads_path, destination_folder, new_filename)
                shutil.move(filepath, new_path)
                processed_files.append({'original_name': filename, 'new_name': new_filename, 'destination_folder': destination_folder})
            else:
                print(f"File {filename} doesn't match any category.")
    
    return processed_files
