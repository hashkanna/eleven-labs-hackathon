import os
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip

def combine_audio_video(video_path, audio_path, output_path):
    """Combine audio and video files into final output."""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    if video.duration < audio.duration:
        video = video.loop(duration=audio.duration)
    else:
        video = video.subclip(0, audio.duration)
    
    final_video = video.set_audio(audio)
    final_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=24
    )
    
    # Cleanup
    final_video.close()
    video.close()
    audio.close()
    
    for file in [video_path, audio_path]:
        if Path(file).exists():
            os.remove(file) 