from pathlib import Path
import logging
from datetime import datetime

class PathManager:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.videos_dir = self.base_dir / 'videos'
        self.temp_dir = self.base_dir / 'temp'
        self.logs_dir = self.base_dir / 'logs'
        self._setup_directories()
        self._setup_logging()

    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.videos_dir, self.temp_dir, self.logs_dir]:
            directory.mkdir(exist_ok=True)

    def _setup_logging(self):
        """Setup logging configuration."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = self.logs_dir / f'generation_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

    def get_temp_path(self, filename):
        """Get path for temporary files."""
        return self.temp_dir / filename

    def get_video_path(self):
        """Generate unique path for final video."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return self.videos_dir / f'inspiration_{timestamp}.mp4'

    def cleanup_temp(self):
        """Clean up temporary files."""
        for file in self.temp_dir.glob('*'):
            file.unlink() 