# Inspirational Quote Video Generator

A Python application that generates inspirational videos by combining AI-generated quotes, text-to-speech audio, and AI-generated video content.

## Features

- Generates unique inspirational quotes using OpenAI GPT-3.5
- Converts quotes to natural-sounding speech using ElevenLabs
- Creates thematic video content using LumaAI
- Combines audio and video into a final MP4 file
- Simple GUI interface built with Tkinter
- Progress tracking and preview functionality

## Prerequisites

- Python 3.8+
- FFmpeg installed on your system
- API keys for:
  - OpenAI
  - ElevenLabs 
  - LumaAI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd inspirational-quote-generator
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
OPENAI_API_KEY=your_openai_key
ELEVEN_API_KEY=your_elevenlabs_key
LUMA_API_KEY=your_lumaai_key
FFMPEG_PATH=/path/to/ffmpeg
```

## Usage

1. Run the application:
```bash
python run.py
```

2. Click "Generate New Quote Video" in the GUI

3. Wait for the generation process to complete (typically 1-2 minutes)

4. The final video will be saved in the `videos` directory and can be played directly from the GUI

## Project Structure

```
.
├── src/
│   ├── services/         # Core service modules
│   ├── ui/              # GUI components
│   └── utils/           # Utility functions
├── temp/                # Temporary files
├── videos/              # Generated videos
├── logs/               # Application logs
├── run.py              # Application entry point
└── requirements.txt    # Dependencies
```

## Technical Details

- Uses OpenAI's GPT-3.5 for creative quote generation
- ElevenLabs API for realistic text-to-speech conversion
- LumaAI for generating thematic video content
- MoviePy for video processing and combining audio/video
- Tkinter for the graphical user interface
- Logging system for debugging and tracking generation process

## Error Handling

- Validates environment variables on startup
- Handles API failures gracefully
- Cleans up temporary files after processing
- Provides user feedback through GUI for all operations

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
