from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KH Logistics · Libra System")
        self.setMinimumSize(900, 500)

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title = QLabel("Bảng điều khiển hệ thống")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        main_layout.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(20)

        # Mỗi "thẻ" là một QWidget riêng
        cards = [
            ("Cài đặt", "KH logistics · Quản trị hệ thống", "#3b82f6"),
            ("Giao việc", "Giao việc liên phòng ban", "#22c55e"),
            ("Tạm ứng", "Quản lý tạm ứng & hoàn ứng", "#f97316"),
            ("Tài chính", "Báo cáo doanh thu · chi phí theo lô hàng", "#ec4899"),
            ("Báo cáo dòng tiền", "Thu · Chi · Logistics & Libra Pet", "#6366f1"),
            ("KPI của tôi", "Hiệu suất công việc cá nhân", "#0ea5e9"),
        ]

        for title_text, subtitle_text, color in cards:
            card = self.create_card(title_text, subtitle_text, color)
            row.addWidget(card)

        main_layout.addLayout(row)
        self.setCentralWidget(central)

    def create_card(self, title_text: str, subtitle_text: str, color: str) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")

        subtitle = QLabel(subtitle_text)
        subtitle.setFont(QFont("Segoe UI", 9))
        subtitle.setStyleSheet("color: #e5e7eb;")
        subtitle.setWordWrap(True)

        btn = QPushButton("Mở")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #111827;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignRight)

        w.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: 12px;
            }}
        """)

        return w


def main():
    app = QApplication(sys.argv)
    win = DashboardWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
