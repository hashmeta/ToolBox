import os
import subprocess

# Function to change video speed using FFmpeg
def change_video_speed_ffmpeg(input_path, output_path, speed_factor):
    # Calculate the PTS value based on the speed factor
    pts_value = 1 / speed_factor

    # Create the FFmpeg command to change video speed
    ffmpeg_command = [
        'ffmpeg', '-i', input_path,  # Input file
        '-filter:v', f"setpts={pts_value}*PTS",  # Adjust the video speed
        '-filter:a', f"atempo={speed_factor}",  # Adjust the audio speed
        output_path  # Output file
    ]

    # Run the FFmpeg command using subprocess
    subprocess.run(ffmpeg_command)

# Folder containing your videos
input_folder = "/Users/kalpesh/Documents/SAP_MRP"
output_folder = "/Users/kalpesh/Documents/SAP_MRP/files_speed_up"

# Speed factor (e.g., 2.0 for double speed, 0.5 for half speed)
speed_factor = 1.7

# Iterate over all video files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4") or filename.endswith(".avi"):  # You can add more extensions if needed
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"speed_{speed_factor}x_{filename}")

        # Call the function to change video speed
        change_video_speed_ffmpeg(input_path, output_path, speed_factor)

        print(f"Processed {filename} and saved to {output_path}")
