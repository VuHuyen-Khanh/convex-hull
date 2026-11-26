import time
import csv
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'codePY')))
import vetcan
import quickhull
from common import reset_counter, get_counter
def generate_points(n, dist_type="random"):
    """Sinh n điểm theo phân bố (ngẫu nhiên, đường tròn...)"""
    return [(random.randint(0, 100000), random.randint(0, 100000)) for _ in range(n)]

def run_benchmark():
    n_vetcan = [10, 50, 100, 200]
    n_quickhull = [100, 500, 1000, 5000, 10000, 50000]
    
    results = []
    for n in n_vetcan:
        points = generate_points(n)
        start_time = time.perf_counter()
        reset_counter()
        vetcan.hull(points)
        end_time = time.perf_counter()
        
        time_taken = end_time - start_time
        cross_count = get_counter()
        
        results.append(["Vet can", n, time_taken, cross_count])
        print(f"Vet can - n={n}: {time_taken:.4f}s, {cross_count} crosses")
    for n in n_quickhull:
        points = generate_points(n)
        
        start_time = time.perf_counter()
        reset_counter()
        quickhull.hull(points)
        end_time = time.perf_counter()
        
        time_taken = end_time - start_time
        cross_count = get_counter()
        
        results.append(["QuickHull", n, time_taken, cross_count])
        print(f"QuickHull - n={n}: {time_taken:.4f}s, {cross_count} crosses")
    with open('data/benchmark_results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Thuat_Toan", "So_Diem_n", "Thoi_Gian_Chay_s", "So_Phep_Toan_cross"])
        writer.writerows(results)
    print("Đã lưu kết quả vào data/benchmark_results.csv")

if __name__ == "__main__":
    run_benchmark()