import os
import shutil

def truncate_folder_name(name, length=8):
    """Truncate the folder name to the given length."""
    return name[:length]

def get_unique_name(name, existing_names):
    """Ensure the file name is unique by appending a two-digit number if needed."""
    if name not in existing_names:
        return name
    # Try appending numbers to make the name unique
    for i in range(1, 100):
        unique_name = f"{name[:6]}{str(i).zfill(2)}"
        if unique_name not in existing_names:
            return unique_name
    raise ValueError(f"Unable to generate a unique name for {name}")

def flatten_and_rename_files(source_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Keep track of already used file names
    used_names = set()

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        # Get the relative path (from source_dir) of the current folder
        relative_path = os.path.relpath(root, source_dir)
        # Split the path into directories
        path_parts = relative_path.split(os.sep)

        # Truncate each part to 8 characters, make sure names are unique
        truncated_parts = []
        for part in path_parts:
            truncated_name = truncate_folder_name(part)
            unique_name = get_unique_name(truncated_name, used_names)
            used_names.add(unique_name)
            truncated_parts.append(unique_name)

        # For each file in the current directory
        for file in files:
            # Build the new file name with truncated folder names
            new_file_name = "_".join(truncated_parts + [file])
            # Full path of the source file
            source_file_path = os.path.join(root, file)
            # Full path for the renamed file in the output directory
            output_file_path = os.path.join(output_dir, new_file_name)
            # Copy the file to the new location
            shutil.copy2(source_file_path, output_file_path)
            print(f"Copied {source_file_path} to {output_file_path}")

# Call the function to flatten the directory structure
flatten_and_rename_files(r'E:\Coursera Learn English Advanced Grammar and Punctuation\Coursera Learn English Advanced Grammar and Punctuation', r'E:\Coursera Learn English Advanced Grammar and Punctuation\Coursera Learn English Advanced Grammar and Punctuation_New')
