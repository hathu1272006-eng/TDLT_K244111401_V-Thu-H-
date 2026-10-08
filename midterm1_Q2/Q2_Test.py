try:
    from review_midterm.midterm1.Q2 import (calc_unit_price, calc_dalat_value, calc_sapa_value,
                                            calc_total, format_money, DALAT_DISCOUNT_PERCENT,
                                            SAPA_DISCOUNT_PERCENT, SalesStatistics)
except ImportError:                      # chạy trực tiếp trong thư mục midterm1
    from Q2 import (calc_unit_price, calc_dalat_value, calc_sapa_value,
                    calc_total, format_money, DALAT_DISCOUNT_PERCENT, SAPA_DISCOUNT_PERCENT,
                    SalesStatistics)

print("Da Lat price per bouquet:", format_money(calc_unit_price(DALAT_DISCOUNT_PERCENT)))
print("Sapa price per bouquet  :", format_money(calc_unit_price(SAPA_DISCOUNT_PERCENT)))

dalat_qty, sapa_qty = 2, 3
dalat_value = calc_dalat_value(dalat_qty)
sapa_value = calc_sapa_value(sapa_qty)
print("Da Lat:", dalat_qty, "->", format_money(dalat_value))
print("Sapa  :", sapa_qty, "->", format_money(sapa_value))
print("Total :", format_money(calc_total(dalat_value, sapa_value)))

# kiểm tra tự động - 1 đơn
assert dalat_value == 170000
assert sapa_value == 300000
assert calc_total(dalat_value, sapa_value) == 470000
assert calc_dalat_value(0) == 0 and calc_sapa_value(0) == 0
assert format_money(1234567) == "1,234,567 VND"

# kiểm tra thống kê cộng dồn nhiều đơn
stats = SalesStatistics()
assert stats.record_order(2, 3) == 470000          # đơn 1
assert stats.record_order(1, 0) == 85000           # đơn 2
assert stats.dalat_sold == 3 and stats.dalat_value == 255000
assert stats.sapa_sold == 3 and stats.sapa_value == 300000
assert stats.total_revenue == 555000
assert stats.order_count == 2
stats.reset()
assert stats.total_revenue == 0 and stats.dalat_sold == 0
print("All tests passed")
