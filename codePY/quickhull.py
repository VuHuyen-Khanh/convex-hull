from common import cross, dedupe, normalize, reset_counter

def _find_hull(points, p1, p2, hull_points, keep_collinear):
    """Hàm đệ quy tìm các đỉnh bao lồi ở một phía của đường thẳng p1-p2"""
    if not points:
        return

    # 1. Tìm điểm xa nhất so với đường thẳng p1-p2
    farthest = points[0]
    max_dist = abs(cross(p1, p2, farthest))
    
    for p in points[1:]:
        dist = abs(cross(p1, p2, p))
        if dist > max_dist:
            max_dist = dist
            farthest = p

    hull_points.append(farthest)

    # 2. Chia các điểm còn lại thành 2 tập con
    left1 = [] # Tập điểm nằm bên trái đoạn (p1, farthest)
    left2 = [] # Tập điểm nằm bên trái đoạn (farthest, p2)
    
    for p in points:
        if p == farthest:
            continue
            
        val1 = cross(p1, farthest, p)
        val2 = cross(farthest, p2, p)
        
        if val1 > 0:
            left1.append(p)
        elif val2 > 0:
            left2.append(p)
        elif keep_collinear:
            # Xử lý điểm thẳng hàng nếu cần giữ lại
            if val1 == 0 and min(p1[0], farthest[0]) <= p[0] <= max(p1[0], farthest[0]) and min(p1[1], farthest[1]) <= p[1] <= max(p1[1], farthest[1]):
                hull_points.append(p)
            elif val2 == 0 and min(farthest[0], p2[0]) <= p[0] <= max(farthest[0], p2[0]) and min(farthest[1], p2[1]) <= p[1] <= max(farthest[1], p2[1]):
                hull_points.append(p)

    # 3. Đệ quy cho 2 tập con
    _find_hull(left1, p1, farthest, hull_points, keep_collinear)
    _find_hull(left2, farthest, p2, hull_points, keep_collinear)


def hull(points, keep_collinear=False):
    """Thuật toán QuickHull tìm bao lồi."""
    reset_counter()
    
    # 1. Tiền xử lý
    points = dedupe(points)
    n = len(points)
    
    if n < 3:
        return normalize(points)
        
    # Kiểm tra tất cả thẳng hàng (mượn logic của bạn)
    p0, p1 = points[0], points[1]
    is_collinear = all(cross(p0, p1, p) == 0 for p in points[2:])
    if is_collinear:
        if keep_collinear:
            return normalize(points)
        else:
            return normalize([min(points), max(points)])

    # 2. Tìm điểm trái nhất và phải nhất
    p_left = min(points)
    p_right = max(points)

    # 3. Chia tập điểm thành 2 nửa (trên và dưới)
    upper = []
    lower = []
    collinear = []

    for p in points:
        if p == p_left or p == p_right:
            continue
        val = cross(p_left, p_right, p)
        if val > 0:
            upper.append(p)
        elif val < 0:
            lower.append(p)
        else:
            collinear.append(p)

    hull_points = [p_left, p_right]

    # 4. Đệ quy tìm bao lồi nửa trên và nửa dưới
    _find_hull(upper, p_left, p_right, hull_points, keep_collinear)
    # Đảo chiều p_right, p_left để cross luôn dương ở nửa dưới
    _find_hull(lower, p_right, p_left, hull_points, keep_collinear) 

    # 5. Thêm các điểm thẳng hàng trên trục chính (nếu có)
    if keep_collinear:
        for p in collinear:
            if min(p_left[0], p_right[0]) <= p[0] <= max(p_left[0], p_right[0]):
                hull_points.append(p)

    # 6. Chuẩn hóa kết quả
    return normalize(dedupe(hull_points))


# --- Chạy thử nhanh ---
if __name__ == "__main__":
    test_points = [(0, 0), (1, 1), (2, 0), (1, 0), (1, 2)]
    print("QuickHull (không lấy điểm thẳng hàng):", hull(test_points, keep_collinear=False))
    print("QuickHull (có lấy điểm thẳng hàng):  ", hull(test_points, keep_collinear=True))