# ============================================================
# Q2 - "Thanh Than Flower" Shop
# Phần LOGIC (xử lý), không dính tới giao diện.
#
# Chọn kiểu dữ liệu:
#   - Số bó hoa   : int  (không thể bán 2,5 bó)
#   - Tiền (VND)  : int  (dùng số nguyên nên không bị sai số làm tròn của float)
#   - % giảm giá  : int  (15 nghĩa là 15%)
#   - Thống kê    : class SalesStatistics (cộng dồn các đơn hàng đã chốt)
# ============================================================

PRICE = 100000                 # giá mỗi bó hoa (VND) - như nhau cho cả 2 loại
DALAT_DISCOUNT_PERCENT = 15    # hoa Da Lat giảm 15%
SAPA_DISCOUNT_PERCENT = 0      # hoa Sapa không giảm giá


def calc_unit_price(discount_percent):
    """Giá 1 bó sau khi giảm: PRICE * (100 - %giảm) / 100."""
    return PRICE * (100 - discount_percent) // 100


def calc_dalat_value(qty):
    """Giá trị tiền của qty bó hoa Da Lat (đã giảm 15%)."""
    if qty < 0:
        raise ValueError("Quantity must not be negative")
    return qty * calc_unit_price(DALAT_DISCOUNT_PERCENT)


def calc_sapa_value(qty):
    """Giá trị tiền của qty bó hoa Sapa (không giảm giá)."""
    if qty < 0:
        raise ValueError("Quantity must not be negative")
    return qty * calc_unit_price(SAPA_DISCOUNT_PERCENT)


def calc_total(dalat_value, sapa_value):
    """Tổng tiền = tiền Da Lat + tiền Sapa."""
    return dalat_value + sapa_value


def format_money(amount):
    """1234567 -> '1,234,567 VND'."""
    return f"{amount:,} VND"


class SalesStatistics:
    """Lưu lịch sử bán hàng: cộng dồn mọi đơn đã bấm Calculate (chốt đơn).

    (2b) dalat_sold / dalat_value : số bó + tiền Da Lat đã bán
    (2c) sapa_sold  / sapa_value  : số bó + tiền Sapa đã bán
    (2d) total_revenue            : tổng doanh thu
    """

    def __init__(self):
        self.reset()

    def reset(self):
        self.dalat_sold = 0
        self.dalat_value = 0
        self.sapa_sold = 0
        self.sapa_value = 0
        self.order_count = 0

    def record_order(self, dalat_qty, sapa_qty):
        """Chốt 1 đơn hàng: cộng dồn vào thống kê, trả về tổng tiền của đơn đó."""
        dalat_value = calc_dalat_value(dalat_qty)
        sapa_value = calc_sapa_value(sapa_qty)
        self.dalat_sold += dalat_qty
        self.dalat_value += dalat_value
        self.sapa_sold += sapa_qty
        self.sapa_value += sapa_value
        self.order_count += 1
        return calc_total(dalat_value, sapa_value)

    @property
    def total_revenue(self):
        return calc_total(self.dalat_value, self.sapa_value)
