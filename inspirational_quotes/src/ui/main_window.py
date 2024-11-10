import tkinter as tk
from tkinter import ttk
import threading
import logging
from PIL import Image, ImageTk
import cv2
import os
import subprocess
import platform
from pathlib import Path
from ..services import quote_service, speech_service, video_service, media_service
from ..utils.path_manager import PathManager
from .. import config

class QuoteGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inspirational Quote Video Generator")
        self.root.geometry("800x600")
        
        self.path_manager = PathManager()
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Preview label
        self.preview_label = ttk.Label(main_frame)
        self.preview_label.grid(row=0, column=0, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        # Generate button
        self.generate_btn = ttk.Button(
            button_frame, 
            text="Generate New Quote Video", 
            command=self.start_generation
        )
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        # Play button
        self.play_btn = ttk.Button(
            button_frame,
            text="Play in Media Player",
            command=self.play_in_player,
            state='disabled'
        )
        self.play_btn.grid(row=0, column=1, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=2, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Click button to generate a video"
        )
        self.status_label.grid(row=3, column=0, pady=10)
        
        self.current_video = None

    def play_in_player(self):
        """Open the video in system's default media player"""
        if self.current_video and Path(self.current_video).exists():
            if platform.system() == 'Darwin':       # macOS
                subprocess.run(['open', self.current_video])
            elif platform.system() == 'Windows':    # Windows
                os.startfile(self.current_video)
            else:                                   # Linux
                subprocess.run(['xdg-open', self.current_video])

    def update_preview(self, video_path):
        """Update the preview image from the video"""
        cap = cv2.VideoCapture(str(video_path))
        ret, frame = cap.read()
        if ret:
            # Resize frame to fit UI
            height, width = frame.shape[:2]
            max_size = 400
            ratio = min(max_size/width, max_size/height)
            new_size = (int(width*ratio), int(height*ratio))
            frame = cv2.resize(frame, new_size)
            
            # Convert to PIL format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            
            # Update label
            self.preview_label.configure(image=img_tk)
            self.preview_label.image = img_tk  # Keep a reference
        
        cap.release()

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
            audio_path = speech_service.text_to_speech(
                quote, 
                config.ELEVEN_API_KEY,
                self.path_manager
            )
            self.root.after(0, lambda: self.status_label.config(text="Generated audio..."))
            
            # Generate video
            video_path = video_service.generate_video(
                quote, 
                config.LUMA_API_KEY,
                self.path_manager
            )
            self.root.after(0, lambda: self.status_label.config(text="Generated video..."))
            
            # Combine
            output_path = self.path_manager.get_video_path()
            media_service.combine_audio_video(
                video_path, 
                audio_path, 
                output_path,
                self.path_manager
            )
            
            self.root.after(0, lambda: self.generation_complete(output_path))
            
        except Exception as e:
            logging.error(f"Error during generation: {str(e)}")
            self.root.after(0, self.generation_failed, str(e))

    def generation_complete(self, output_path):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        if output_path.exists():
            msg = f"Video generated successfully!\nSaved as: {output_path}"
            logging.info(msg)
            self.status_label.config(text=msg)
            self.current_video = str(output_path)
            self.update_preview(output_path)
            self.play_btn.config(state='normal')
        else:
            msg = "Generation completed but file not found"
            logging.error(msg)
            self.status_label.config(text=msg)

    def generation_failed(self, error):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        self.status_label.config(text=f"Error: {error}")

    def __del__(self):
        self.path_manager.cleanup_temp()