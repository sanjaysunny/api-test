import concurrent.futures
import requests
import time


URL = 'http://example.com/api'

def load_test(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise exception if the request fails
    return response.status_code

def run_load_test(num_requests):
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = {executor.submit(load_test, URL) for _ in range(num_requests)}
        for future in concurrent.futures.as_completed(futures):
            try:
                status_code = future.result()
                print(f'GET returned status code {status_code} for request {num_requests}')
            except Exception as exc:
                end_time = time.time()
                print(f'Generated an exception: {exc}')
                print(f'Time taken until exception: {end_time - start_time} seconds for {num_requests} requests')
                return False

    end_time = time.time()
    print(f'Time taken: {end_time - start_time} seconds for {num_requests} requests')
    return True

num_requests = 1
while True:
    print(f'Running load test with {num_requests} requests...')
    success = run_load_test(num_requests)
    if not success:
        break
    num_requests *= 2  # Double the number of requests for the next iteration
