import tkinter as tk
from tkinter import ttk
import threading
from pathlib import Path
from ..services import quote_service, speech_service, video_service, media_service
from .. import config

class QuoteGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inspirational Quote Video Generator")
        self.root.geometry("400x200")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.generate_btn = ttk.Button(
            main_frame, 
            text="Generate Quote Video", 
            command=self.start_generation
        )
        self.generate_btn.grid(row=0, column=0, pady=20)
        
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=1, column=0, pady=10)
        
        self.status_label = ttk.Label(
            main_frame,
            text="Click button to generate a video"
        )
        self.status_label.grid(row=2, column=0, pady=10)

    def start_generation(self):
        self.generate_btn.config(state='disabled')
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
        else:
            self.status_label.config(text="Generation completed but file not found")

    def generation_failed(self, error):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        self.status_label.config(text=f"Error: {error}") 