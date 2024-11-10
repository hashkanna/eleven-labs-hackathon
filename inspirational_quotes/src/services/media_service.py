import logging
from moviepy.editor import VideoFileClip, AudioFileClip

def combine_audio_video(video_path, audio_path, output_path, path_manager):
    """Combine audio and video files into final output."""
    logging.info("Combining audio and video...")
    video = VideoFileClip(str(video_path))
    audio = AudioFileClip(str(audio_path))
    
    if video.duration < audio.duration:
        video = video.loop(duration=audio.duration)
    else:
        video = video.subclip(0, audio.duration)
    
    final_video = video.set_audio(audio)
    logging.info(f"Writing final video to: {output_path}")
    final_video.write_videofile(
        str(output_path),
        codec='libx264',
        audio_codec='aac',
        fps=24
    )
    
    # Cleanup
    final_video.close()
    video.close()
    audio.close()
    
    logging.info("Video and audio combined successfully")