import sys
import os
import re
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QSlider
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class FullScreenVideoWindow(QWidget):
    def __init__(self, parent, media_player):
        super().__init__()
        self.parent = parent
        self.media_player = media_player
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Full Screen")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        layout = QVBoxLayout()
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)
        layout.addWidget(self.video_widget)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)  # 更新视频进度
        layout.addWidget(self.slider)

        control_layout = QHBoxLayout()
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.media_player.pause)
        control_layout.addWidget(self.pause_button)

        self.play_button = QPushButton("Continue")
        self.play_button.clicked.connect(self.media_player.play)
        control_layout.addWidget(self.play_button)

        self.exit_button = QPushButton("Exit Full Screen")
        self.exit_button.clicked.connect(self.exit_fullscreen)
        control_layout.addWidget(self.exit_button)

        layout.addLayout(control_layout)
        self.setLayout(layout)

        # 连接positionChanged信号，确保进度条同步
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.set_slider_range)

    def update_slider(self, position):
        self.slider.setValue(position)  # 更新进度条位置

    def set_slider_range(self, duration):
        self.slider.setRange(0, duration)  # 设置进度条范围

    def set_position(self, position):
        # 更新进度条时，设置视频的播放进度
        self.media_player.setPosition(position)

    def exit_fullscreen(self):
        self.media_player.setVideoOutput(self.parent.video_widget)
        self.close()
        self.parent.show()


class IELTSHelperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Listening Practice')
        self.setGeometry(100, 100, 800, 600)
        self.current_video = None
        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget(self)
        self.fullscreen_window = None
        self.sentences = []
        self.timer = QTimer(self)
        self.timer.setInterval(50)  # 设置定时器的更新时间间隔
        self.timer.timeout.connect(self.sync_position)  # 定时器触发时更新视频进度
        self.is_dragging = False  # 用来标记是否正在拖动进度条
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.select_video_button = QPushButton("Choose Video")
        self.select_video_button.clicked.connect(self.select_video)
        layout.addWidget(self.select_video_button)

        layout.addWidget(self.video_widget)
        self.media_player.setVideoOutput(self.video_widget)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.sliderPressed.connect(self.slider_pressed)  # 开始拖动时触发
        self.slider.sliderReleased.connect(self.slider_released)  # 松开鼠标时触发
        self.slider.sliderMoved.connect(self.set_position)  # 拖动时更新视频进度
        layout.addWidget(self.slider)

        control_layout = QHBoxLayout()
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.media_player.play)
        control_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.media_player.pause)
        control_layout.addWidget(self.pause_button)

        self.fullscreen_button = QPushButton("Full Screen")
        self.fullscreen_button.clicked.connect(self.open_fullscreen)
        control_layout.addWidget(self.fullscreen_button)

        self.show_sentences_button = QPushButton("Show Sentences")
        self.show_sentences_button.clicked.connect(self.show_sentences)
        control_layout.addWidget(self.show_sentences_button)

        layout.addLayout(control_layout)
        self.setLayout(layout)

        # 连接positionChanged信号，确保进度条同步
        self.media_player.positionChanged.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.set_slider_range)

    def update_slider(self, position):
        if not self.is_dragging:  # 如果没有拖动进度条，更新进度条
            self.slider.setValue(position)  # 更新主窗口的进度条位置

    def set_slider_range(self, duration):
        self.slider.setRange(0, duration)  # 设置主窗口的进度条范围

    def set_position(self, position):
        if self.is_dragging:  # 只有在拖动进度条时才更新播放进度
            self.media_player.setPosition(position)

    def sync_position(self):
        # 使用定时器来同步进度条和视频播放进度
        if self.is_dragging:
            self.media_player.setPosition(self.slider.value())

    def slider_pressed(self):
        self.is_dragging = True  # 开始拖动进度条时设置标记

        # 启动定时器
        self.timer.start()

    def slider_released(self):
        self.is_dragging = False  # 松开进度条时设置标记

        # 停止定时器
        self.timer.stop()

        # 在松开时立即更新视频进度
        self.media_player.setPosition(self.slider.value())

    def select_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi *.mkv)")
        if file_name:
            self.current_video = file_name
            media_content = QMediaContent(QUrl.fromLocalFile(file_name))
            self.media_player.setMedia(media_content)
            self.media_player.play()

    def open_fullscreen(self):
        if not self.fullscreen_window:
            self.fullscreen_window = FullScreenVideoWindow(self, self.media_player)
        self.fullscreen_window.showFullScreen()

    def split_sentences(self, text):
        sentences = re.split(r'[。！？]', text)
        return [s.strip() for s in sentences if s.strip()]

    def show_sentences(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "选择文本文件", os.getcwd(), "文本文件 (*.txt)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as f:
                text = f.read()
                self.sentences = self.split_sentences(text)
                self.sentence_viewer = SentenceViewer(self.sentences)
                self.sentence_viewer.show()


class SentenceViewer(QWidget):
    def __init__(self, sentences):
        super().__init__()
        self.sentences = sentences
        self.selected_sentences = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Helper")
        self.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setText("\n".join(self.sentences))
        layout.addWidget(self.text_display)

        self.add_button = QPushButton("Add Selected Sentence")
        self.add_button.clicked.connect(self.add_selected_sentence)
        layout.addWidget(self.add_button)

        self.new_text_display = QTextEdit()
        layout.addWidget(self.new_text_display)

        self.export_button = QPushButton("Export Text")
        self.export_button.clicked.connect(self.export_text)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def add_selected_sentence(self):
        selected_text = self.text_display.textCursor().selectedText()
        if selected_text and selected_text not in self.selected_sentences:
            self.selected_sentences.append(selected_text)
            self.new_text_display.setText("\n".join(self.selected_sentences))

    def export_text(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文本", "sentences.txt", "文本文件 (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write("\n".join(self.selected_sentences))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IELTSHelperApp()
    window.show()
    sys.exit(app.exec_())