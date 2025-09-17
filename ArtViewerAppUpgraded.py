import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTextEdit, QSizePolicy)
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Third-party libraries for new features
import qrcode
from PIL import Image
from io import BytesIO

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
        self.setGeometry(100, 100, 300, 500)
        self.setStyleSheet("background-color: #1a202c; color: #e2e8f0;")

        self.image_index = 0
        self.is_favorites_view = False
        self.current_image_urls = IMAGE_URLS
        self.art_data = self.load_art_data(self)

        self.setup_ui()
        self.display_image()
        #self.update()

    @staticmethod
    def load_art_data(self):
        """Loads likes, comments, and favorites from a local JSON file."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    # Ensure all URLs have data, and initialize favorites if missing
                    for url in IMAGE_URLS:
                        if url not in data:
                            data[url] = {"likes": 0, "comments": []}
                    if "favorites" not in data:
                        data["favorites"] = []
                    return data
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading data file: {e}. Starting with empty data.")
                return {"favorites": {}}
        else:
            # Initialize data structure if file doesn't exist
            return {
                "favorites": [],
                **{url: {"likes": 0, "comments": []} for url in IMAGE_URLS}
            }

    def save_art_data(self):
        """Saves current likes, comments, and favorites to the local JSON file."""
        try:
            with open(DATA_FILE, "w") as f:
                json.dump(self.art_data, f, indent=4)
        except IOError as e:
            print(f"Error saving data file: {e}")

    def setup_ui(self):
        """Sets up the main layout and widgets for the application."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(23, 23, 23, 23)
        main_layout.setSpacing(30)

        '''# Title Label
        title_layout = QVBoxLayout()
        self.setLayout(title_layout)
        title_label = QLabel("Online Art Gallery")
        title_label.setAlignment(Qt.AlignTop)
        title_label.setFont(QFont("Inter", 15, QFont.Bold))
        title_label.setStyleSheet("color: #FBBF24;")
        main_layout.addWidget(title_label)'''

        # --- Left Panel for New Features ---
        left_panel_layout = QVBoxLayout()
        left_panel_layout.setAlignment(Qt.AlignTop)

        self.fullscreen_button = self.create_button("Toggle Fullscreen", self.toggle_fullscreen, "#4A5568", "#2D3748")
        self.view_favorites_button = self.create_button("View Favorites", self.toggle_favorites_view, "#667EEA",
                                                        "#4C51BF")
        self.back_to_gallery_button = self.create_button("Back to Gallery", self.toggle_favorites_view, "#F56565",
                                                         "#E53E3E")
        self.back_to_gallery_button.hide()  # Initially hide this button
        self.add_to_favorites_button = self.create_button("Add to Favorites ❤️", self.add_to_favorites, "#ECC94B",
                                                          "#D69E2E")
        self.share_button = self.create_button("Share via QR Code", self.share_qr_code, "#38B2AC", "#319795")

        left_panel_layout.addWidget(self.fullscreen_button)
        left_panel_layout.addWidget(self.view_favorites_button)
        left_panel_layout.addWidget(self.back_to_gallery_button)
        left_panel_layout.addWidget(self.add_to_favorites_button)
        left_panel_layout.addWidget(self.share_button)
        left_panel_layout.addStretch()

        # --- Right Panel for Gallery Content ---
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setContentsMargins(0, 0, 0, 0)
        right_panel_layout.setSpacing(8)

        # Logo Section
        '''logo_layout = QVBoxLayout()
        self.setLayout(logo_layout)

        # Create a QLabel
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_label)
        main_layout.addLayout(logo_layout)

        # Load the image and display it
        # Replace 'logo.png' with your file path
        self.upload_logo('C:\\Users\\Springrose\\Downloads\\Gemini_Generated_Image_2.png')'''

        # Logo and Title Section
        logo_title_layout = QVBoxLayout()
        self.setLayout(logo_title_layout)
        self.logo_label = QLabel()
        #self.logo_label.setFixedSize(150, 150)
        self.logo_label.setAlignment(Qt.AlignTop)
        self.logo_label.setStyleSheet("border-radius: 75px;")

        logo_title_layout.addWidget(self.logo_label)
        #logo_layout.addWidget(self.logo_label)
        logo_title_layout.addWidget(self.logo_label)
        main_layout.addLayout(logo_title_layout)

        upload_logo_button = self.create_button("Upload Logo", self.upload_logo, "#9F7AEA", "#805AD5")

        #logo_title_layout.addWidget(self.logo_label)

        title_label = QLabel("Online Art Gallery")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Inter", 15, QFont.Bold))
        title_label.setStyleSheet("color: #FBBF24;")

        title_layout = QVBoxLayout()
        title_layout.addWidget(title_label)
        title_layout.addSpacing(-10)  # Reduce space between title and image

        logo_title_layout.addLayout(title_layout)
        logo_title_layout.addWidget(upload_logo_button, alignment=Qt.AlignRight | Qt.AlignTop)

        #right_panel_layout.addLayout(logo_title_layout)
        #right_panel_layout.setSpacing(8)  # Reduced spacing here

        # Image Display Area (Using QWebEngineView for better rendering)
        self.image_panel = QWebEngineView()
        self.image_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_panel.setStyleSheet("border-radius: 5px; border: 2px solid #4a5568;")
        self.image_panel.setMinimumSize(200, 400)
        self.image_panel.setMaximumSize(300, 500)
        right_panel_layout.addWidget(self.image_panel, alignment=Qt.AlignCenter)

        # Navigation and Status
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignCenter)

        self.prev_button = self.create_button("← Previous", self.previous_image, "#2563EB", "#1D4ED8")
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Inter", 14))
        self.status_label.setStyleSheet("color: #a0aec0;")
        self.next_button = self.create_button("Next →", self.next_image, "#2563EB", "#1D4ED8")

        nav_layout.addWidget(self.prev_button)
        nav_layout.addSpacing(40)
        nav_layout.addWidget(self.status_label)
        nav_layout.addSpacing(40)
        nav_layout.addWidget(self.next_button)

        right_panel_layout.addLayout(nav_layout)

        # Action Buttons Section
        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignCenter)

        self.like_button = self.create_button("Like ❤️", self.like_image, "#F56565", "#E53E3E")
        ad_button = self.create_button("Watch an Ad", self.watch_ad, "#F6AD55", "#ED8936")
        exit_button = self.create_button("Exit App", self.exit_app, "#F56565", "#E53E3E")

        bottom_layout.addWidget(self.like_button)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(ad_button)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(exit_button)

        right_panel_layout.addLayout(bottom_layout)

        # Comments Section
        comments_layout = QVBoxLayout()
        comments_layout.setSpacing(5)
        comment_label = QLabel("Comments")
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

        add_comment_button_layout = QHBoxLayout()
        add_comment_button_layout.addWidget(add_comment_button, alignment=Qt.AlignCenter)

        comments_layout.addWidget(comment_label)
        comments_layout.addWidget(self.comment_display)
        comments_layout.addWidget(self.comment_input)
        comments_layout.addLayout(add_comment_button_layout)

        right_panel_layout.addLayout(comments_layout)

        main_layout.addLayout(left_panel_layout)
        main_layout.addLayout(right_panel_layout)

    @staticmethod
    def create_button(text, command, color, hover_color):
        """Helper function to create styled buttons."""
        button = QPushButton(text)
        button.setFixedSize(160, 45)
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
        if not self.current_image_urls:
            self.image_panel.setUrl(QUrl("about:blank"))
            self.status_label.setText("No images to display.")
            self.like_button.setText("Like ❤️ (0)")
            self.comment_display.setText("No comments.")
            self.add_to_favorites_button.hide()
            self.like_button.hide()
            return

        url = self.current_image_urls[self.image_index]
        self.image_panel.setUrl(QUrl(url))
        self.status_label.setText(f"Image {self.image_index + 1} of {len(self.current_image_urls)}")

        # Update social features
        current_image_data = self.art_data.get(url, {"likes": 0, "comments": []})
        self.like_button.setText(f"Like ❤️ ({current_image_data['likes']})")
        self.comment_display.setText("\n".join(current_image_data["comments"]))

    def next_image(self):
        """Displays the next image."""
        self.image_index = (self.image_index + 1) % len(self.current_image_urls)
        self.display_image()

    def previous_image(self):
        """Displays the previous image."""
        self.image_index = (self.image_index - 1 + len(self.current_image_urls)) % len(self.current_image_urls)
        self.display_image()

    def like_image(self):
        """Handles liking an image."""
        url = self.current_image_urls[self.image_index]
        if url not in self.art_data:
            self.art_data[url] = {"likes": 0, "comments": []}
        self.art_data[url]["likes"] += 1
        self.like_button.setText(f"Like ❤️ ({self.art_data[url]['likes']})")
        self.save_art_data()

    def add_comment(self):
        """Handles adding a comment to an image."""
        comment_text = self.comment_input.toPlainText().strip()
        if comment_text:
            url = self.current_image_urls[self.image_index]
            if url not in self.art_data:
                self.art_data[url] = {"likes": 0, "comments": []}
            self.art_data[url]["comments"].append(comment_text)
            self.comment_display.append(comment_text)
            self.comment_input.clear()
            self.save_art_data()

    @staticmethod
    def watch_ad():
        """Simulates an ad view."""
        # For a real app, this would integrate with an ad network.
        print("Simulated ad request. A commercial would play now.")

    def exit_app(self):
        """Closes the application."""
        self.close()

    def toggle_fullscreen(self):
        """Toggles fullscreen mode."""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def add_to_favorites(self):
        """Adds the current image URL to the favorites list."""
        url = self.current_image_urls[self.image_index]
        if url not in self.art_data["favorites"]:
            self.art_data["favorites"].append(url)
            self.save_art_data()
            print(f"Added {url} to favorites.")
        else:
            print(f"{url} is already in favorites.")

    def toggle_favorites_view(self):
        """Toggles between the main gallery and the favorites view."""
        if not self.is_favorites_view:
            self.is_favorites_view = True
            self.current_image_urls = self.art_data.get("favorites", [])
            self.view_favorites_button.hide()
            self.back_to_gallery_button.show()
            self.add_to_favorites_button.hide()
            self.like_button.hide()
            self.image_index = 0
            self.display_image()
        else:
            self.is_favorites_view = False
            self.current_image_urls = IMAGE_URLS
            self.back_to_gallery_button.hide()
            self.view_favorites_button.show()
            self.add_to_favorites_button.show()
            self.like_button.show()
            self.image_index = 0
            self.display_image()

    def share_qr_code(self):
        """Generates and displays a QR code for the current image URL."""
        if not self.current_image_urls:
            return

        url = self.current_image_urls[self.image_index]
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="white", back_color="#1a202c")

        # Convert PIL image to QPixmap
        buffer = BytesIO()
        img.save(buffer, "PNG")
        pixmap = QPixmap()
        pixmap.loadFromData(buffer.getvalue(), "PNG")

        # Create a new dialog to display the QR code
        qr_dialog = QDialog(self)
        qr_dialog.setWindowTitle("Share Image")
        qr_dialog.setStyleSheet("background-color: #1a202c; color: #e2e8f0;")

        dialog_layout = QVBoxLayout(qr_dialog)
        qr_label = QLabel()
        qr_label.setPixmap(pixmap)
        qr_label.setAlignment(Qt.AlignCenter)

        info_label = QLabel("Scan this code to view the image on your phone!")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Inter", 12))

        dialog_layout.addWidget(info_label)
        dialog_layout.addWidget(qr_label)

        qr_dialog.exec_()

if __name__ == "__main__":
        app = QApplication(sys.argv)
        viewer = ArtViewerApp()
        viewer.show()
        sys.exit(app.exec_())
