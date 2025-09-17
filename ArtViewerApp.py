import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTextEdit, QSizePolicy)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Configuration and Data
IMAGE_URLS = [
    "https://naijasteed.blogspot.com/2025/09/art-7.html",
    "https://placehold.co/600x800/33FF57/FFFFFF?text=Landscape+Painting",
    "https://placehold.co/600x800/3357FF/FFFFFF?text=Digital+Illustration",
    "https://placehold.co/600x800/FF33A1/FFFFFF?text=Portrait+Sketch",
    "https://placehold.co/600x800/A1FF33/FFFFFF?text=Modern+Sculpture",
]

DATA_FILE = "art_data.json"

class ArtViewerApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Jopper - A Colorful Art Viewer Inspired By AI")
        self.setGeometry(50, 50, 400, 600)
        self.setStyleSheet("background-color: #1a202c; color: #e2e8f0;")

        self.image_index = 0
        self.art_data = self.load_art_data()

        self.setup_ui()
        self.display_image()
        self.update()

    @staticmethod
    def load_art_data():
        """Loads likes and comments from a local JSON file."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        else:
            # Initialize data structure if file doesn't exist
            return {
                url: {"likes": 0, "comments": []} for url in IMAGE_URLS
            }

    def save_art_data(self):
        """Saves current likes and comments to the local JSON file."""
        with open(DATA_FILE, "w") as f:
            json.dump(self.art_data, f, indent=4)

    def setup_ui(self):
        """Sets up the main layout and widgets for the application."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Logo Section
        '''logo_layout = QVBoxLayout()
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(50, 50)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("border-radius: 75px;")

        upload_logo_button = self.create_button("Upload Logo", self.upload_logo,
                                                "#9F7AEA", "#805AD5")
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(upload_logo_button, alignment=Qt.AlignCenter | Qt.AlignTop)
        main_layout.addLayout(logo_layout)'''

        # Title Label
        title_label = QLabel("Online Art Gallery")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Inter", 15, QFont.Bold))
        title_label.setStyleSheet("color: #FBBF24;")
        main_layout.addWidget(title_label)

        # Logo Section
        logo_layout = QVBoxLayout()
        self.setLayout(logo_layout)

        # Create a QLabel
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_label)
        main_layout.addLayout(logo_layout)

        # Load the image and display it
        # Replace 'logo.png' with your file path
        self.upload_logo('C:\\Users\\Springrose\\Downloads\\Gemini_Generated_Image_2.png')

        # Image Display Area (Using QWebEngineView for better rendering)
        self.image_panel = QWebEngineView()
        self.image_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_panel.setStyleSheet("border-radius: 15px; border: 5px solid #4a5568;")

        # Adjusting the aspect ratio for portrait images
        self.image_panel.setMinimumSize(200, 400)
        self.image_panel.setMaximumSize(300, 500)
        self.image_panel.setStyleSheet("background-color: #2d3748; border-radius: 8px; padding: 10px;")
        main_layout.addWidget(self.image_panel, alignment=Qt.AlignCenter)

        # Navigation and Status
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)

        self.prev_button = self.create_button("<< Previous", self.previous_image, "#2563EB", "#1D4ED8")
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Inter", 15))
        self.status_label.setStyleSheet("color: #a0aec0;")
        self.next_button = self.create_button("Next >>", self.next_image, "#2563EB", "#1D4ED8")

        nav_layout.addWidget(self.prev_button)
        nav_layout.addSpacing(40)
        nav_layout.addWidget(self.status_label)
        nav_layout.addSpacing(40)
        nav_layout.addWidget(self.next_button)

        main_layout.addLayout(nav_layout)

        # Action Buttons Section
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)

        # Likes Layout
        likes_layout = QVBoxLayout()

        # Like Button
        self.like_button = self.create_button("Like ❤️", self.like_image, "#F56565", "#E53E3E")
        likes_layout.addWidget(self.like_button)

        # Ad Button
        ad_button = self.create_button("Watch an Ad", self.watch_ad, "#F6AD55", "#ED8936")

        # Exit Button
        exit_button = self.create_button("Exit App", self.exit_app, "#F56565", "#E53E3E")

        # All buttons are now placed in the same horizontal layout for alignment
        bottom_layout.addWidget(self.like_button)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(ad_button)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(exit_button)

        main_layout.addLayout(bottom_layout)

        # Comments Section
        comments_layout = QVBoxLayout()
        comments_layout.setSpacing(5)
        comment_label = QLabel("Comments:")
        comment_label.setFont(QFont("Inter", 12, QFont.Bold))
        comment_label.setStyleSheet("color: #9f7aea;")

        self.comment_display = QTextEdit()
        self.comment_display.setReadOnly(True)
        self.comment_display.setStyleSheet("background-color: #2d3748; border-radius: 8px; padding: 10px;")

        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Add a comment...")
        self.comment_input.setStyleSheet("background-color: #2d3748; border-radius: 8px; padding: 5px;")
        self.comment_input.setMaximumHeight(50)

        add_comment_button = self.create_button("Add Comment", self.add_comment, "#48BB78", "#38A169")

        # Create a new layout to center the 'Add Comment' button
        add_comment_button_layout = QHBoxLayout()
        add_comment_button_layout.addWidget(add_comment_button, alignment=Qt.AlignCenter)

        # Likes and Comments Section
        comments_layout.addWidget(comment_label)
        comments_layout.addWidget(self.comment_display)
        comments_layout.addWidget(self.comment_input)
        comments_layout.addLayout(add_comment_button_layout)

        main_layout.addLayout(comments_layout)

    @staticmethod
    def create_button(text, command, color, hover_color):
        """Helper function to create styled buttons."""
        button = QPushButton(text)
        button.setFixedSize(140, 45)
        button.setFont(QFont("Inter", 12, QFont.Bold))
        button.clicked.connect(command)

        style = f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 22px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.2s ease-in-out;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                transform: scale(1.05);
            }}
            QPushButton:pressed {{
                transform: scale(0.95);
            }}
        """
        button.setStyleSheet(style)
        return button

    '''def upload_logo(self):
        """Opens a file dialog to allow the user to upload a logo."""
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Logo File")
        file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg *.svg)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                pixmap = QPixmap()
                if pixmap.load(file_path):
                    scaled_pixmap = pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
                else:
                    print("Error: The selected file is not a valid image.")'''

    def upload_logo(self, image_path):
        """Loads an image from a file and displays it in the QLabel."""
        try:
            # Create a QPixmap from the image file
            pixmap = QPixmap(image_path)

            # Check if the image loaded successfully
            if pixmap.isNull():
                print(f"Error: Unable to load image from {image_path}")
                # You might want to display a placeholder or text instead
                self.logo_label.setText("Image not found")
                return

            # Optionally, scale the image to fit the label
            scaled_pixmap = pixmap.scaled(150, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)

            # Set the QPixmap to the QLabel
            self.logo_label.setPixmap(pixmap)

        except Exception as e:
            print(f"An error occurred: {e}")
            self.logo_label.setText("An error occurred")

    def display_image(self):
        """Displays the image at the current index and updates social data."""
        url = IMAGE_URLS[self.image_index]
        self.image_panel.setUrl(QUrl(url))

        # Image counter
        self.status_label.setText(f"{self.image_index + 1} of {len(IMAGE_URLS)}")

        # Update social features
        current_image_data = self.art_data.get(url, {"likes": 0, "comments": []})
        self.like_button.setText(f"Like ❤️ ({current_image_data['likes']})")
        self.comment_display.setText("\n".join(current_image_data["comments"]))

    def next_image(self):
        """Displays the next image."""
        self.image_index = (self.image_index + 1) % len(IMAGE_URLS)
        self.display_image()

    def previous_image(self):
        """Displays the previous image."""
        self.image_index = (self.image_index - 1 + len(IMAGE_URLS)) % len(IMAGE_URLS)
        self.display_image()

    def like_image(self):
        """Handles liking an image."""
        url = IMAGE_URLS[self.image_index]
        if url not in self.art_data:
            self.art_data[url] = {"likes": 0, "comments": []}
        self.art_data[url]["likes"] += 1
        self.like_button.setText(f"Like ❤️ ({self.art_data[url]['likes']})")
        self.save_art_data()

    @staticmethod
    def watch_ad():
        """Simulates an ad view."""
        # For a real app, this would integrate with an ad network.
        # Here, it simply updates the UI to simulate the process.
        print("Simulated ad request. A commercial would play now.")

    def exit_app(self):
        """Closes the application."""
        self.close()

    def add_comment(self):
        """Handles adding a comment to an image."""
        comment_text = self.comment_input.toPlainText().strip()
        if comment_text:
            url = IMAGE_URLS[self.image_index]
            if url not in self.art_data:
                self.art_data[url] = {"likes": 0, "comments": []}
            self.art_data[url]["comments"].append(comment_text)
            self.comment_display.append(comment_text)
            self.comment_input.clear()
            self.save_art_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ArtViewerApp()
    viewer.show()
    sys.exit(app.exec_())