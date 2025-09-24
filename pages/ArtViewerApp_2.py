import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, \
    QFileDialog, QSizePolicy, QLineEdit, QSplitter
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class ArtGalleryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Colorful Art Viewer")
        self.setGeometry(100, 100, 1200, 900)  # Portrait-oriented window
        self.setStyleSheet("background-color: #1a202c; color: #e2e8f0;")

        self.IMAGE_URLS = [
            "https://placehold.co/600x800/FF5733/FFFFFF?text=Abstract+Art",
            "https://placehold.co/600x800/33FF57/FFFFFF?text=Landscape+Painting",
            "https://placehold.co/600x800/3357FF/FFFFFF?text=Digital+Illustration",
            "https://placehold.co/600x800/FF33A1/FFFFFF?text=Portrait+Sketch",
            "https://placehold.co/600x800/A1FF33/FFFFFF?text=Modern+Sculpture",
        ]
        self.image_index = 0
        self.art_data = self.load_data()

        self.setup_ui()
        self.display_image()

    def load_data(self):
        try:
            with open("art_data.json", "r") as f:
                data = json.load(f)
                # Initialize missing keys if data is incomplete
                for url in self.IMAGE_URLS:
                    if url not in data:
                        data[url] = {"likes": 0, "comments": []}
                if "favorites" not in data:
                    data["favorites"] = []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                url: {"likes": 0, "comments": []}
                for url in self.IMAGE_URLS
            } | {"favorites": []}

    def save_data(self):
        try:
            with open("art_data.json", "w") as f:
                json.dump(self.art_data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def setup_ui(self):
        # Create a central widget and a main layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Splitter to resize panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left Container for Ads and Features
        left_container = QWidget()
        left_container_layout = QVBoxLayout(left_container)
        left_container_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Ad Panel
        ad_panel = QWidget()
        ad_panel_layout = QVBoxLayout(ad_panel)
        self.ad_viewer = QWebEngineView()
        self.ad_viewer.setHtml("""
            <div style="font-family: Arial, sans-serif; background-color: #334155; color: #e2e8f0; padding: 10px; border-radius: 5px; text-align: center; height: 100%;">
                <h3 style="color: #6ee7b7; font-size: 1.2em; margin: 0;">Sponsored</h3>
                <p style="font-size: 0.9em;">Click to see our new offers!</p>
                <div style="font-size: 0.7em; color: #94a3b8;">Ad by ExampleCo</div>
            </div>
        """)
        ad_panel_layout.addWidget(self.ad_viewer)
        ad_panel.setFixedSize(250, 150)
        left_container_layout.addWidget(ad_panel)

        # Left Panel (Logo and Features)
        self.left_panel = QWidget()
        self.left_panel_layout = QVBoxLayout(self.left_panel)
        self.left_panel_layout.setAlignment(Qt.AlignCenter)

        # App Logo
        self.logo_label = QLabel()
        self.logo_label.setPixmap(
            QPixmap("https://placehold.co/144x144/9F7AEA/FFFFFF?text=Logo").scaledToWidth(144, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedSize(144, 144)
        self.left_panel_layout.addWidget(self.logo_label)

        # Upload Logo Button
        self.upload_logo_btn = self.create_button("Upload Logo", self.upload_logo)
        self.left_panel_layout.addWidget(self.upload_logo_btn)

        # New Features Layout
        features_layout = QVBoxLayout()
        features_layout.setSpacing(5)

        self.fullscreen_btn = self.create_button("Toggle Fullscreen", self.toggle_fullscreen)
        self.view_favorites_btn = self.create_button("View Favorites", self.toggle_favorites_view)
        self.back_to_gallery_btn = self.create_button("Back to Gallery", self.toggle_favorites_view)
        self.back_to_gallery_btn.hide()
        self.add_favorites_btn = self.create_button("Add to Favorites ❤️", self.add_to_favorites)
        self.share_qr_btn = self.create_button("Share via QR Code", self.generate_qr_code)

        features_layout.addWidget(self.fullscreen_btn)
        features_layout.addWidget(self.view_favorites_btn)
        features_layout.addWidget(self.back_to_gallery_btn)
        features_layout.addWidget(self.add_favorites_btn)
        features_layout.addWidget(self.share_qr_btn)

        self.left_panel_layout.addLayout(features_layout)

        # Social Media Buttons
        social_layout = QHBoxLayout()
        social_layout.setSpacing(5)
        self.twitter_share_btn = self.create_button("Share on X", self.share_on_twitter)
        self.facebook_share_btn = self.create_button("Share on FB", self.share_on_facebook)
        social_layout.addWidget(self.twitter_share_btn)
        social_layout.addWidget(self.facebook_share_btn)
        self.left_panel_layout.addLayout(social_layout)

        left_container_layout.addWidget(self.left_panel)

        # Right Panel (Main Gallery)
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setAlignment(Qt.AlignCenter)

        self.art_title_label = QLabel("Online Art Gallery")
        self.art_title_label.setFont(QFont("Inter", 24, QFont.Bold))
        self.art_title_label.setStyleSheet("color: #FACC15;")
        self.art_title_label.setAlignment(Qt.AlignCenter)
        right_panel_layout.addWidget(self.art_title_label)

        # Image Display Area (Using QWebEngineView for better rendering)
        self.image_viewer = QWebEngineView()
        self.image_viewer.setFixedSize(600, 800)
        self.image_viewer.setStyleSheet("border: 2px solid #4a5568; border-radius: 5px;")
        right_panel_layout.addWidget(self.image_viewer)

        # Navigation and Status
        nav_status_layout = QHBoxLayout()
        nav_status_layout.setSpacing(5)
        self.prev_btn = self.create_button("← Previous", self.previous_image)
        self.image_status_label = QLabel("Image 1 of 5")
        self.image_status_label.setStyleSheet("color: #A0AEC0;")
        self.image_status_label.setAlignment(Qt.AlignCenter)
        self.next_btn = self.create_button("Next →", self.next_image)
        nav_status_layout.addWidget(self.prev_btn)
        nav_status_layout.addWidget(self.image_status_label)
        nav_status_layout.addWidget(self.next_btn)
        right_panel_layout.addLayout(nav_status_layout)

        # Action Buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(5)
        self.like_btn = self.create_button("Like ❤️ (0)", self.like_image)
        self.ad_btn = self.create_button("Watch an Ad", self.watch_ad)
        self.exit_btn = self.create_button("Exit Gallery", self.exit_app)
        action_layout.addWidget(self.like_btn)
        action_layout.addWidget(self.ad_btn)
        action_layout.addWidget(self.exit_btn)
        right_panel_layout.addLayout(action_layout)

        # Comment Section
        comments_layout = QVBoxLayout()
        comments_layout.setSpacing(5)
        self.comment_label = QLabel("Comments")
        self.comment_label.setFont(QFont("Inter", 12, QFont.Bold))
        self.comment_label.setStyleSheet("color: #A020F0;")

        self.comments_display = QLabel("No comments yet.")
        self.comments_display.setStyleSheet(
            "background-color: #2d3748; border-radius: 5px; padding: 10px; border: 1px solid #4a5568;")
        self.comments_display.setWordWrap(True)
        self.comments_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Add a comment...")
        self.comment_input.setStyleSheet(
            "background-color: #2d3748; border: 1px solid #4a5568; color: #e2e8f0; padding: 5px; border-radius: 5px;")

        self.add_comment_btn = self.create_button("Add Comment", self.add_comment)

        comments_layout.addWidget(self.comment_label)
        comments_layout.addWidget(self.comments_display)
        comments_layout.addWidget(self.comment_input)
        comments_layout.addWidget(self.add_comment_btn, alignment=Qt.AlignCenter)

        right_panel_layout.addLayout(comments_layout)

        # Add the two panels to the splitter
        splitter.addWidget(left_container)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 900])  # Initial sizes for the panels

    def create_button(self, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        button.setFixedSize(120, 30)
        button.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border-radius: 3px;
                padding: 6px;
                font-size: 10pt;
                font-weight: bold;
                border: none;
                box-shadow: 0 4px #1D4ED8;
                transition: all 0.2s;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1E40AF;
                box-shadow: 0 2px #1D4ED8;
                transform: translateY(2px);
            }
        """)
        return button

    def display_image(self):
        url = self.IMAGE_URLS[self.image_index]
        html_content = f"""
        <html>
        <body style="margin:0; padding:0; background-color: #2d3748; display:flex; justify-content:center; align-items:center; height:100vh;">
            <img src="{url}" style="max-width:100%; max-height:100%; object-fit:contain; border-radius: 5px;">
        </body>
        </html>
        """
        self.image_viewer.setHtml(html_content, QUrl("about:blank"))

        self.image_status_label.setText(f"Image {self.image_index + 1} of {len(self.IMAGE_URLS)}")

        likes_count = self.art_data.get(url, {}).get("likes", 0)
        self.like_btn.setText(f"Like ❤️ ({likes_count})")

        comments = self.art_data.get(url, {}).get("comments", [])
        if comments:
            comments_text = "<br>".join(comments)
            self.comments_display.setText(comments_text)
        else:
            self.comments_display.setText("No comments yet.")

    def next_image(self):
        self.image_index = (self.image_index + 1) % len(self.IMAGE_URLS)
        self.display_image()

    def previous_image(self):
        self.image_index = (self.image_index - 1 + len(self.IMAGE_URLS)) % len(self.IMAGE_URLS)
        self.display_image()

    def like_image(self):
        url = self.IMAGE_URLS[self.image_index]
        if url not in self.art_data:
            self.art_data[url] = {"likes": 0, "comments": []}
        self.art_data[url]["likes"] += 1
        self.save_data()
        self.like_btn.setText(f"Like ❤️ ({self.art_data[url]['likes']})")

    def add_comment(self):
        comment = self.comment_input.text()
        if comment:
            url = self.IMAGE_URLS[self.image_index]
            if url not in self.art_data:
                self.art_data[url] = {"likes": 0, "comments": []}
            self.art_data[url]["comments"].append(comment)
            self.save_data()
            self.comment_input.clear()
            self.display_image()

    def watch_ad(self):
        # Placeholder for ad functionality
        self.show_message("A simulated ad would play here!", "Ad Service")

    def exit_app(self):
        self.close()

    def upload_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload App Logo", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                self.logo_label.setPixmap(pixmap.scaledToWidth(144, Qt.SmoothTransformation))
            else:
                self.show_message("Invalid image file. Please select a valid image.", "Error")

    def show_message(self, message, title):
        msg_box = QDialog(self)
        msg_box.setWindowTitle(title)
        msg_box.setStyleSheet("background-color: #2d3748; color: #e2e8f0;")
        layout = QVBoxLayout()
        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(msg_box.accept)
        layout.addWidget(ok_button, alignment=Qt.AlignCenter)
        msg_box.setLayout(layout)
        msg_box.exec_()

    # Implementations for new features
    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def toggle_favorites_view(self):
        pass  # Placeholder for this function

    def add_to_favorites(self):
        pass  # Placeholder for this function

    def generate_qr_code(self):
        pass  # Placeholder for this function

    def share_on_twitter(self):
        pass  # Placeholder for this function

    def share_on_facebook(self):
        pass  # Placeholder for this function

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArtGalleryApp()
    window.show()
    sys.exit(app.exec_())