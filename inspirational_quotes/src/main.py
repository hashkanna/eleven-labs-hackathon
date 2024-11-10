from moviepy.config import change_settings
from .ui.main_window import QuoteGeneratorUI
from .config import FFMPEG_PATH
import tkinter as tk

def main():
    # Configure FFMPEG
    change_settings({"FFMPEG_BINARY": FFMPEG_PATH})
    
    # Start UI
    root = tk.Tk()
    app = QuoteGeneratorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()