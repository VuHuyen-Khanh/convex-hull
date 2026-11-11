import random
import json

def generate_random_points(n, max_val=1000):
    """Sinh n điểm ngẫu nhiên (x, y) trong khoảng [-max_val, max_val]"""
    return [(random.randint(-max_val, max_val), random.randint(-max_val, max_val)) for _ in range(n)]

def generate_edge_cases():
    """Sinh các trường hợp biên (ít điểm, thẳng hàng, trùng nhau)"""
    cases = {
        "empty": [],
        "one_point": [(5, 5)],
        "two_points": [(1, 2), (3, 4)],
        "collinear": [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
        "duplicates": [(0, 0), (1, 1), (0, 0), (1, 1), (2, 2)]
    }
    return cases

def save_to_json(data, filename):
    """Lưu dữ liệu ra file JSON để Nam dùng đi benchmark"""
    with open(f"data/{filename}.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    # Tạo thư mục data nếu chưa có
    import os
    if not os.path.exists("data"):
        os.makedirs("data")

    # Sinh data cho các trường hợp biên
    edge_cases = generate_edge_cases()
    for name, points in edge_cases.items():
        save_to_json(points, f"edge_{name}")
    
    # Sinh data ngẫu nhiên với số lượng điểm tăng dần
    for n in [10, 100, 1000]:
        points = generate_random_points(n)
        save_to_json(points, f"random_{n}")
        
    print("Đã sinh xong dữ liệu vào thư mục 'data/'")
