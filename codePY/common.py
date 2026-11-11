"""
common.py - module dùng chung cho cả 4 thuật toán bao lồi (vét cạn, Jarvis, Graham, QuickHull).
QUY ƯỚC CHUNG (cả nhóm phải theo):
1. Điểm là tuple số nguyên (x, y).
2. Mọi thuật toán có chữ ký:  hull(points, keep_collinear=False)
3. Kết quả: list các đỉnh bao lồi, ngược chiều kim đồng hồ (CCW), bắt đầu từ điểm thấp nhất bên trái (x nhỏ nhất, hòa thì y nhỏ nhất).
Dùng normalize() trước khi return để mọi thuật toán cho cùng định dạng.
4. Điểm trùng nhau: bị loại trước khi tính (dùng dedupe()).
5. keep_collinear=False: chỉ giữ đỉnh "thật" của bao lồi.
   keep_collinear=True : giữ cả điểm nằm trên cạnh bao (LeetCode 587 cần cái này).
6. n < 3 hoặc tất cả thẳng hàng: trả về các điểm đầu mút (xem normalize()).
7. MỌI phép kiểm tra hướng phải gọi cross() để bộ đếm đúng.
"""
# Tích có hướng + bộ đếm phép toán cơ bản
_cross_count = 0

def reset_counter():
    """Đặt bộ đếm về 0 (gọi trước mỗi lần chạy thuật toán)."""
    global _cross_count
    _cross_count = 0

def get_counter():
    """Số lần cross() đã được gọi từ lần reset gần nhất."""
    return _cross_count

def cross(o, a, b):
    """ Tích có hướng của vector OA và OB.
      > 0 : o -> a -> b rẽ TRÁI (ngược chiều kim đồng hồ)
      < 0 : rẽ PHẢI
      = 0 : ba điểm thẳng hàng
    Dùng số nguyên nên không có sai số số thực."""

    global _cross_count
    _cross_count += 1
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# Tiền xử lý và chuẩn hóa kết quả

def dedupe(points):
    """Loại điểm trùng, trả về list tuple đã sắp xếp theo (x, y)."""
    return sorted(set(tuple(p) for p in points))


def _signed_area2(poly):
    """2 lần diện tích có dấu (dương nếu CCW). Không đếm vào bộ đếm."""
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return s


def normalize(hull):
    """
    Đưa kết quả của mọi thuật toán về cùng một dạng:
    CCW, bắt đầu từ điểm nhỏ nhất theo (x, y). Dùng để so khớp 2 kết quả.
    """
    hull = [tuple(p) for p in hull]
    if len(hull) < 3:
        return sorted(hull)
    if _signed_area2(hull) < 0:      # đang theo chiều kim đồng hồ -> đảo lại
        hull.reverse()
    start = hull.index(min(hull))
    return hull[start:] + hull[:start]


def same_hull(h1, h2):
    """So sánh 2 bao lồi sau khi chuẩn hóa."""
    return normalize(h1) == normalize(h2)


# ---------------------------------------------------------------
# Chạy thử: python common.py
# ---------------------------------------------------------------
if __name__ == "__main__":
    reset_counter()
    print(cross((0, 0), (1, 0), (1, 1)))    # 1  -> rẽ trái
    print(cross((0, 0), (1, 0), (1, -1)))   # -1 -> rẽ phải
    print(cross((0, 0), (1, 1), (2, 2)))    # 0  -> thẳng hàng
    print("số lần gọi cross:", get_counter())  # 3

    print(dedupe([(1, 1), (0, 0), (1, 1)]))    # [(0, 0), (1, 1)]
    # Hình vuông, liệt kê theo chiều kim đồng hồ, bắt đầu từ điểm khác
    print(normalize([(1, 1), (1, 0), (0, 0), (0, 1)]))
    # -> [(0, 0), (1, 0), (1, 1), (0, 1)]
