import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QGraphicsScene, QGraphicsView, QFrame)

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    from review_midterm.midterm1.Q2 import (calc_dalat_value, calc_sapa_value, calc_total,
                                            format_money, SalesStatistics)
except ImportError:                      # chạy trực tiếp trong thư mục midterm1
    sys.path.insert(0, HERE)
    from Q2 import calc_dalat_value, calc_sapa_value, calc_total, format_money, SalesStatistics

UI_DIR = os.path.join(HERE, "Q2UI")
UI_FILE = os.path.join(UI_DIR, "FlowerMainWindow.ui")

DESIGN_W, DESIGN_H = 900, 569      # kích thước thiết kế gốc của giao diện (.ui)


class FlowerShopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        os.chdir(UI_DIR)                 # để đường dẫn ảnh "../images/..." trong file .ui luôn đúng
        uic.loadUi(UI_FILE, self)

        # giãn chữ cho dòng phụ đề ở header (giống thiết kế mẫu)
        font = self.subtitleLabel.font()
        font.setLetterSpacing(QFont.AbsoluteSpacing, 2.0)
        self.subtitleLabel.setFont(font)

        # thu nhỏ cả giao diện cho vừa màn hình (giao diện giữ nguyên, chỉ đổi kích thước cửa sổ)
        self.fit_window_to_screen()

        # dữ liệu: lịch sử các đơn đã chốt
        self.stats = SalesStatistics()

        # (2a) chọn số lượng -> Current order + Total payment cập nhật NGAY
        self.dalatSpinBox.valueChanged.connect(self.update_current_order)
        self.sapaSpinBox.valueChanged.connect(self.update_current_order)

        # nối sự kiện cho 3 nút
        self.calculateButton.clicked.connect(self.calculate)
        self.clearButton.clicked.connect(self.clear)
        self.closeButton.clicked.connect(self.close)

        self.update_current_order()
        self.update_statistics()

    # ---------------------------------------------------------------- kích thước cửa sổ
    def fit_window_to_screen(self):
        """Chiếm khoảng 57% chiều rộng / 72% chiều cao màn hình, giữ đúng tỉ lệ thiết kế."""
        area = QApplication.primaryScreen().availableGeometry()
        scale = min(1.0, 0.57 * area.width() / DESIGN_W, 0.72 * area.height() / DESIGN_H)

        central = self.takeCentralWidget()          # lấy toàn bộ giao diện cũ ra
        central.setFixedSize(DESIGN_W, DESIGN_H)    # giữ nguyên bố cục gốc
        scene = QGraphicsScene(self)
        scene.addWidget(central)
        view = QGraphicsView(scene, self)
        view.setFrameShape(QFrame.NoFrame)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing |
                            QPainter.SmoothPixmapTransform)
        view.scale(scale, scale)
        self.setCentralWidget(view)

        w, h = round(DESIGN_W * scale), round(DESIGN_H * scale)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        self.setFixedSize(w, h)
        self.move(area.center().x() - w // 2, area.center().y() - h // 2)

    # ---------------------------------------------------------------- 2. Current order
    def update_current_order(self):
        """Chạy mỗi khi đổi số bó hoa: hiện tiền từng loại và Total payment."""
        dalat_value = calc_dalat_value(self.dalatSpinBox.value())   # int (VND)
        sapa_value = calc_sapa_value(self.sapaSpinBox.value())      # int (VND)
        self.orderDalatEdit.setText(format_money(dalat_value))
        self.orderSapaEdit.setText(format_money(sapa_value))
        self.totalPaymentLabel.setText(format_money(calc_total(dalat_value, sapa_value)))

    # ---------------------------------------------------------------- 3. Sales statistics
    def update_statistics(self):
        s = self.stats
        self.dalatSoldEdit.setText(str(s.dalat_sold))              # 2b: số bó Da Lat đã bán
        self.dalatValueEdit.setText(format_money(s.dalat_value))   # 2b: giá trị Da Lat
        self.sapaSoldEdit.setText(str(s.sapa_sold))                # 2c: số bó Sapa đã bán
        self.sapaValueEdit.setText(format_money(s.sapa_value))     # 2c: giá trị Sapa
        self.totalRevenueLabel.setText(format_money(s.total_revenue))  # 2d: tổng doanh thu

    # ---------------------------------------------------------------- nút Calculate
    def calculate(self):
        """Chốt đơn: cộng đơn hiện tại vào lịch sử thống kê, rồi làm mới đơn cho khách kế tiếp."""
        dalat_qty = self.dalatSpinBox.value()
        sapa_qty = self.sapaSpinBox.value()
        if dalat_qty == 0 and sapa_qty == 0:
            QMessageBox.warning(self, "No flowers selected",
                                "Please choose the quantity of flower bouquets first!")
            return

        order_total = self.stats.record_order(dalat_qty, sapa_qty)
        self.update_statistics()
        QMessageBox.information(self, "Order confirmed",
                                f"Da Lat: {dalat_qty} bouquet(s)\n"
                                f"Sapa: {sapa_qty} bouquet(s)\n\n"
                                f"Total payment: {format_money(order_total)}")
        self.clear()

    # ---------------------------------------------------------------- nút Clear
    def clear(self):
        """Xóa đơn đang chọn (thống kê đã chốt vẫn được giữ lại)."""
        self.dalatSpinBox.setValue(0)    # tự gọi update_current_order -> về 0 VND
        self.sapaSpinBox.setValue(0)
        self.dalatSpinBox.setFocus()


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = FlowerShopWindow()
    window.show()
    sys.exit(app.exec_())
