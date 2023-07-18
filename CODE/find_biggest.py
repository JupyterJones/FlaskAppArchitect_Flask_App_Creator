import os

def list_files_over_40mb(directory_path):
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        raise ValueError(f"The directory '{directory_path}' does not exist.")

    large_files = []

    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Check if the file is a regular file (not a directory or symbolic link)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)

            # Check if the file size is greater than 40 megabytes (40 * 1024 * 1024 bytes)
            if file_size > 40 * 1024 * 1024:
                large_files.append((file_path, file_size))

    return large_files

# Example usage
directory_path = "/home/jack/Desktop/StoryMaker"
large_files = list_files_over_40mb(directory_path)

if large_files:
    print("Files larger than 40 megabytes:")
    for file_path, file_size in large_files:
        print(f"File: {file_path}, Size: {file_size} bytes")
else:
    print("No files over 40 megabytes found in the directory.")
