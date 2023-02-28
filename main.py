import threading
import time
import random
from queue import Queue

RAM_size = 1000
free_RAM = RAM_size
request_queue = Queue()
num_requests = 3
num_threads = 3
lock = threading.Lock()
exit_flag = False


def handle_request(request):
    global free_RAM, request_queue
    thread_name, request_type, volume = request
    if request_type == 0:
        print(f"Received request from {thread_name} to allocate {volume} KB.")
        allocation_request(volume, thread_name)
    else:
        print(f"Received request from {thread_name} to utilize {volume} KB")
        utilization_request(volume, thread_name)


def allocation_request(volume, thread_name):
    global free_RAM
    with lock:
        if volume <= free_RAM:
            free_RAM -= volume
            print(f"Allocated {volume} KB of RAM to {thread_name}")
            print(f"{free_RAM} is available")
        else:
            print(f"Not enough RAM available to allocate {volume} KB to {thread_name}")
            print(f"{free_RAM} is available")


def utilization_request(volume, thread_name):
    global free_RAM
    with lock:
        if volume <= RAM_size - free_RAM:
            free_RAM += volume
            print(f"Utilized  {volume} KB of RAM by {thread_name}")
        else:
            print(f"Not enough RAM in use to utilize {volume} KB by {thread_name}")


def simulate_requests():
    for i in range(num_requests):
        thread_name = threading.current_thread().getName()
        request_type = random.choice([0, -1])
        volume = random.randint(1, 1024)
        request = (thread_name, request_type, volume)
        with lock:
            request_queue.put(request)
        time.sleep(random.uniform(0.1, 0.5))


def process_queue():
    while not exit_flag:
        request = None
        with lock:
            if not request_queue.empty():
                request = request_queue.get()

        if request:
            handle_request(request)
            request_queue.task_done()
        else:
            time.sleep(0.1)


def create_request_threads():
    for i in range(num_threads):
        request_thread = threading.Thread(target=simulate_requests)
        request_thread.start()


def create_queue_thread():
    queue_thread = threading.Thread(target=process_queue)
    queue_thread.start()
    return queue_thread


def stop_threads():
    global exit_flag
    exit_flag = True
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()


if __name__ == "__main__":
    queue_thread = create_queue_thread()
    create_request_threads()
    time.sleep(2)
    stop_threads()
