import math
from common import cross, dedupe, normalize, reset_counter
def _sort_hull_points(points):
    if len(points)<3:
        return points
    cx = sum(p[0] for p in points)/ len(points)
    cy = sum(p[1] for p in points)/ len(points)
    return sorted(points,key=lambda p:(math.atan2(p[1]-cy,p[0]-cx),(p[0]-cx)**2+(p[1]-cy)**2))
def _is_all_collinear(points):
    """Hàm phụ: Kiểm tra xem tất cả các điểm có thẳng hàng không."""
    if len(points) < 3:
        return True
    p0, p1 = points[0], points[1]
    for i in range(2, len(points)):
        if cross(p0, p1, points[i]) != 0:
            return False
    return True

def hull(points, keep_collinear=False):
    """Thuật toán vét cạn tìm bao lồi (Brute Force)."""
    # 0. Reset bộ đếm mỗi lần chạy (Quy ước 7)
    reset_counter()
    
    # 1. Loại bỏ điểm trùng (Quy ước 4)
    points = dedupe(points)
    n = len(points)
    
    # 2. Xử lý trường hợp ít hơn 3 điểm (Quy ước 6)
    if n < 3:
        return normalize(points)
        
    # 3. Xử lý trường hợp tất cả thẳng hàng (Quy ước 6)
    if _is_all_collinear(points):
        if keep_collinear:
            return normalize(points) # Giữ tất cả
        else:
            return normalize([min(points), max(points)]) # Chỉ giữ 2 đầu mút

    hull_points = []

    # 4. Thuật toán vét cạn: Duyệt mọi cặp điểm (p1, p2)
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            p1, p2 = points[i], points[j]
            
            left_count = 0
            right_count = 0
            collinear_count = 0
            
            # Kiểm tra tất cả các điểm còn lại (p3) so với đường thẳng p1-p2
            for k in range(n):
                if k == i or k == j: 
                    continue
                p3 = points[k]
                val = cross(p1, p2, p3)
                
                if val > 0: 
                    left_count += 1
                elif val < 0: 
                    right_count += 1
                else: 
                    collinear_count += 1
            
            # 5. Xét điều kiện để p1-p2 là cạnh của bao lồi
            if keep_collinear:
                # Giữ cả điểm trên cạnh: Tất cả các điểm phải nằm cùng phía (bên trái hoặc bên phải), tính cả thẳng hàng
                if (left_count + collinear_count == n - 2) or (right_count + collinear_count == n - 2):
                    hull_points.append(p1)
            else:
                # Chỉ giữ đỉnh thật: Tuyệt đối không có điểm nào nằm trên đường thẳng p1-p2 (trừ p1, p2)
                if (left_count == n - 2) or (right_count == n - 2):
                    hull_points.append(p1)

    # 6. Chuẩn hóa kết quả trước khi return (Quy ước 3)
    # Phải dedupe lại lần nữa vì vòng lặp có thể thêm 1 điểm nhiều lần
    hull_points = dedupe(hull_points)
    hull_points = _sort_hull_points(hull_points) 
    return normalize(hull_points)


# --- Chạy thử nhanh (bạn có thể xóa phần này khi nộp bài) ---
if __name__ == "__main__":
    test_points = [(0, 0), (1, 1), (2, 0), (1, 0), (1, 2)]
    print("Kết quả vét cạn (không lấy điểm thẳng hàng):", hull(test_points, keep_collinear=False))
    print("Kết quả vét cạn (có lấy điểm thẳng hàng):  ", hull(test_points, keep_collinear=True))
