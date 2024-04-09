"""
This part is created for testing purposes, for video and or gif
inclusion into the background of the text being shown on screen
and not just a still image.
"""

from PIL import Image, ImageSequence
from moviepy.editor import VideoFileClip

def convert_video_to_gif(video_path, gif_path, start_time=0, duration=None):
    """
    Converts a video to a GIF (It is pretty self explanitory).

    Parameters:
    - video_path: Path to the source video file.
    - gif_path: Path where the GIF should be saved.
    - start_time: Start time for the GIF in seconds.
    - duration: Duration of the GIF in seconds.
    """
    # Load the video file
    clip = VideoFileClip(video_path)

    if duration is not None:
        # Trim the clip according to the start_time and duration
        clip = clip.subclip(start_time, start_time + duration)
    else:
        # Trim the clip from start_time to the end
        clip = clip.subclip(start_time)

    # Write the resulting clip to a GIF file.
    clip.write_gif(gif_path, fps=10)  # You can adjust the fps (frames per second) as needed

# Example usage
video_path = 'vid.mp4'  # Replace with the path to your video
gif_path = 'output.gif'  # Replace with your desired output GIF path
convert_video_to_gif(video_path, gif_path)  # Converts 5 seconds of the video starting from the 10th second

def split_gif_into_frames(gif_path, output_folder):
    with Image.open(gif_path) as img:
        # Make sure the output_folder ends with a slash
        if not output_folder.endswith('/'):
            output_folder += '/'
        
        # Iterate through each frame of the gif
        for frame_number, frame in enumerate(ImageSequence.Iterator(img)):
            # Make a new image file for each frame, and save it
            frame.save(output_folder + f"frame_{frame_number}.png")

# Example usage:
output_folder = "folder"  # Replace with your desired output folder
split_gif_into_frames(gif_path, output_folder)



