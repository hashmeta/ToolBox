import os
from moviepy.editor import VideoFileClip
import argparse
def get_total_video_duration(folder_path):
    total_duration = 0 
    for filename in os.listdir(folder_path):
        if filename.endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Add more extensions if needed
            video_path = os.path.join(folder_path, filename)
            try:
                video = VideoFileClip(video_path)
                total_duration += video.duration  # duration in seconds
                video.close()  # Always close the video file after opening
            except Exception as e:
                print(f"Could not process {filename}: {e}")
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    return hours, minutes

def rename_folder_with_duration(folder_path):
    hours, minutes = get_total_video_duration(folder_path)
    parent_directory = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    new_folder_name = f"{folder_name}_{hours}h_{minutes}m"
    new_folder_path = os.path.join(parent_directory, new_folder_name)
    try:
        os.rename(folder_path, new_folder_path)
        print(f"Folder renamed to: {new_folder_name}")
    except Exception as e:
        print(f"Error renaming folder: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate total watch time and rename folder")
    parser.add_argument("folder_path", help="Path to the folder containing videos")
    args = parser.parse_args()
    rename_folder_with_duration(args.folder_path)