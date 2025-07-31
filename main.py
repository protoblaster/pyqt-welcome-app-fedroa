import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class WelcomeUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fedora Welcome")
        self.setFixedSize(300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Fedora!", self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(QFont("Arial", 14))

        update_button = QPushButton("Run System Update", self)
        update_button.clicked.connect(self.run_update)

        layout.addWidget(welcome_label)
        layout.addStretch()
        layout.addWidget(update_button)
        layout.addStretch()

        self.setLayout(layout)

    def run_update(self):
        reply = QMessageBox.question(
            self,
            "Confirm Update",
            "Do you want to run a system update?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                subprocess.run(["pkexec", "dnf", "upgrade", "-y"], check=True)
                QMessageBox.information(self, "Update Complete", "System update completed successfully.")
            except subprocess.CalledProcessError:
                QMessageBox.critical(self, "Update Failed", "Failed to run system update.")
            except FileNotFoundError:
                QMessageBox.critical(self, "Error", "Required command not found. Make sure `dnf` and `pkexec` are installed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeUpdater()
    window.show()
    sys.exit(app.exec_())
