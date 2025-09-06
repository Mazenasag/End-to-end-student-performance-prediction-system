import requests
import time
import numpy as np
import concurrent.futures
import psutil
import threading

# ✅ Replace with your deployed Elastic Beanstalk URL
URL = "http://cloudproject-env.eba-kxven3e8.us-east-1.elasticbeanstalk.com/predictdata"

# Example input data (adjust based on your Flask form fields)
FORM_DATA = {
    "gender": "male",
    "ethnicity": "group A",
    "parental_level_of_education": "bachelor's degree",
    "lunch": "standard",
    "test_preparation_course": "completed",
    "writing_score": "70",
    "reading_score": "72"
}

# Number of requests and concurrency
TOTAL_REQUESTS = 1000
CONCURRENCY = 50

cpu_readings = []
ram_readings = []

def monitor_system(pid):
    """Monitors CPU and RAM usage of the given process."""
    process = psutil.Process(pid)
    while True:
        try:
            cpu = process.cpu_percent(interval=0.5)  # CPU %
            ram = process.memory_percent()           # RAM %
            cpu_readings.append(cpu)
            ram_readings.append(ram)
        except psutil.NoSuchProcess:
            break

def send_request():
    """Sends a POST request and measures response time."""
    start = time.time()
    try:
        response = requests.post(URL, data=FORM_DATA, timeout=10)
    except requests.exceptions.RequestException:
        return None, None, 0
    end = time.time()

    inference_time = None
    if response.status_code == 200:
        try:
            data = response.json()
            inference_time = data.get("inference_time", None)
        except Exception:
            pass

    return end - start, inference_time, response.status_code

def run_load_test():
    times = []
    inference_times = []
    success = 0

    # Start monitoring CPU/RAM in background
    pid = psutil.Process().ppid()  # parent process (Flask)
    monitor_thread = threading.Thread(target=monitor_system, args=(pid,), daemon=True)
    monitor_thread.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = [executor.submit(send_request) for _ in range(TOTAL_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                t, inf_time, status = result
                if t is not None:
                    times.append(t)
                if inf_time is not None:
                    inference_times.append(inf_time)
                if status == 200:
                    success += 1

    times = np.array(times)
    avg_time = np.mean(times) if len(times) > 0 else 0
    median_time = np.median(times) if len(times) > 0 else 0
    throughput = TOTAL_REQUESTS / np.sum(times) if len(times) > 0 else 0

    avg_inf = np.mean(inference_times) if inference_times else None
    avg_cpu = np.mean(cpu_readings) if cpu_readings else 0
    avg_ram = np.mean(ram_readings) if ram_readings else 0

    print("\n📊 Load Test Results:")
    print(f"Total Requests: {TOTAL_REQUESTS}")
    print(f"Concurrency: {CONCURRENCY}")
    print(f"Successful Responses: {success}/{TOTAL_REQUESTS}")
    print(f"Avg. Response Time: {avg_time:.4f} s")
    print(f"Median Response Time: {median_time:.4f} s")
    print(f"Throughput: {throughput:.2f} requests/sec")
    if avg_inf:
        print(f"Avg. Inference Time: {avg_inf:.4f} s")
    print(f"Avg. CPU Utilization: {avg_cpu:.2f}%")
    print(f"Avg. RAM Utilization: {avg_ram:.2f}%")

if __name__ == "__main__":
    run_load_test()
