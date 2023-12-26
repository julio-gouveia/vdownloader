import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt5.QtCore import pyqtSlot
from pytube import YouTube

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video = None

    def initUI(self):
        # Initialize widgets
        self.linkLabel = QLabel('Link', self)
        self.linkInput = QLineEdit(self)

        self.dirLabel = QLabel('Directory', self)
        self.dirInput = QLineEdit(self)

        self.processLabel = QLabel('Process', self)
        self.mp4Button = QPushButton('MP4', self)
        self.mp3Button = QPushButton('MP3', self)
        
        # Initialize the progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)

        # Title
        self.titleLabel = QLabel('VDownloader | Made In Python')

        # Connect buttons to the same slot for now
        # self.processButton.clicked.connect(self.on_click)
        self.mp4Button.clicked.connect(self.download_mp4)
        self.mp3Button.clicked.connect(self.download_mp3)

        # Layout for MP4 and MP3 buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.mp4Button)
        buttonLayout.addWidget(self.mp3Button)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.linkLabel)
        layout.addWidget(self.linkInput)
        layout.addWidget(self.dirLabel)
        layout.addWidget(self.dirInput)
        layout.addWidget(self.processLabel)
        layout.addLayout(buttonLayout)  # Add the horizontal layout of MP4 and MP3
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

        # Window configurations
        self.setWindowTitle('VDownloader')
        self.setGeometry(0, 0, 300, 200)
        self.show()
    
    def reset_progress_bar(self):
        self.progressBar.setValue(0)
        
    @pyqtSlot(int)
    def update_progress_bar(self, stream, chunk, bytes_remaining):
        # Calculate the percentage completion
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int(bytes_downloaded / total_size * 100)
        self.progressBar.setValue(percentage)

    def download_mp4(self):
        self.reset_progress_bar()
        video_url = self.linkInput.text()
        if video_url:
            try:
                yt = YouTube(video_url, on_progress_callback=self.update_progress_bar)
                video_stream = yt.streams.filter(file_extension='mp4').first()
                video_stream.download(output_path=self.dirInput.text())
                print(f"Downloaded MP4: {yt.title}")
            except Exception as e:
                print(f"Error: {e}")

    def download_mp3(self):
        self.reset_progress_bar()
        video_url = self.linkInput.text()
        if video_url:
            try:
                yt = YouTube(video_url, on_progress_callback=self.update_progress_bar)
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=self.dirInput.text())
                print(f"Downloaded MP3: {yt.title}")
            except Exception as e:
                print(f"Error: {e}")

    def on_click(self):
        # Handle button click event for all buttons
        sender = self.sender()
        link_text = self.linkInput.text()
        dir_text = self.dirInput.text()
        print(f"{sender.text()} clicked:")
        print("Link:", link_text)
        print("Directory:", dir_text)

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
