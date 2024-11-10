import tkinter as tk
from tkinter import ttk
import threading
from pathlib import Path
import cv2
from PIL import Image, ImageTk
from ..services import quote_service, speech_service, video_service, media_service
from .. import config

class QuoteGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inspirational Quote Video Generator")
        self.root.geometry("800x600")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Video display
        self.video_label = ttk.Label(main_frame)
        self.video_label.grid(row=0, column=0, pady=10)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=1, column=0, pady=10)
        
        self.generate_btn = ttk.Button(
            controls_frame, 
            text="Generate Quote Video", 
            command=self.start_generation
        )
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = ttk.Button(
            controls_frame,
            text="Play",
            command=self.toggle_play,
            state='disabled'
        )
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=2, column=0, pady=10)
        
        self.status_label = ttk.Label(
            main_frame,
            text="Click button to generate a video"
        )
        self.status_label.grid(row=3, column=0, pady=10)
        
        # Video playback variables
        self.cap = None
        self.is_playing = False
        self.current_video = None

    def toggle_play(self):
        if self.is_playing:
            self.is_playing = False
            self.play_btn.config(text="Play")
        else:
            self.is_playing = True
            self.play_btn.config(text="Pause")
            self.play_video()

    def play_video(self):
        if not self.is_playing or self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            # If reached end, loop back to start
            if frame is None:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            # Convert frame to PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 360))
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
            
            # Schedule next frame
            self.root.after(33, self.play_video)  # ~30 fps
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.play_video()

    def load_video(self, video_path):
        if self.cap is not None:
            self.cap.release()
        
        self.current_video = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.play_btn.config(state='normal')
        self.is_playing = True
        self.play_video()

    def start_generation(self):
        self.generate_btn.config(state='disabled')
        self.play_btn.config(state='disabled')
        self.progress.start(10)
        self.status_label.config(text="Generating video... Please wait")
        
        thread = threading.Thread(target=self.generate_video_thread)
        thread.daemon = True
        thread.start()

    def generate_video_thread(self):
        try:
            # Generate quote
            quote = quote_service.generate_quote(config.OPENAI_API_KEY)
            self.root.after(0, lambda: self.status_label.config(text="Generated quote..."))
            
            # Generate audio
            audio_path = speech_service.text_to_speech(quote, config.ELEVEN_API_KEY)
            self.root.after(0, lambda: self.status_label.config(text="Generated audio..."))
            
            # Generate video
            video_path = video_service.generate_video(quote, config.LUMA_API_KEY)
            self.root.after(0, lambda: self.status_label.config(text="Generated video..."))
            
            # Combine
            output_path = 'final_inspiration.mp4'
            media_service.combine_audio_video(video_path, audio_path, output_path)
            
            self.root.after(0, self.generation_complete)
            
        except Exception as e:
            self.root.after(0, self.generation_failed, str(e))

    def generation_complete(self):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        output_path = Path('final_inspiration.mp4')
        if output_path.exists():
            self.status_label.config(
                text=f"Video generated successfully!\nSaved as: {output_path}"
            )
            self.load_video(str(output_path))
        else:
            self.status_label.config(text="Generation completed but file not found")

    def generation_failed(self, error):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        self.status_label.config(text=f"Error: {error}")

    def __del__(self):
        if self.cap is not None:
            self.cap.release()