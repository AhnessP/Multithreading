import threading
import time
import random
from queue import Queue

RAM_size = 1000 
current_RAM = RAM_size  
RAM_semaphore = threading.Semaphore(1)  
request_queue = Queue() 
num_requests = 2
request_thread = None
queue_thread = None


def handle_request(request):
    global current_RAM, request_queue
    thread_name, request_type, volume = request
    RAM_semaphore.acquire()
    if request_type == 0:
        print(f"Received request from {thread_name} to allocate {volume} KB.")
    else:
        print(f"Received request from {thread_name} to utilize {volume} KB")
    t = threading.Thread(target=allocation_request if request_type == 0 else utilization_request(), args=(request,))
    t.start()
    RAM_semaphore.release()


def allocation_request(request):
    global current_RAM
    thread_name, request_type, volume = request
    if volume <= current_RAM:
        current_RAM -= volume
        print(f"Allocated {volume} KB of RAM to {thread_name}")
    else:
        print(f"Not enough RAM available to allocate {volume} KB to {thread_name}")


def utilization_request(request):
    global current_RAM

    thread_name, request_type, volume = request
    if volume <= RAM_size - current_RAM:
        current_RAM += volume
        print(f"Utilized  {volume} KB of RAM by {thread_name}")
    else:
        print(f"Not enough RAM taken to utilize {volume} KB by {thread_name}")

def simulate_requests():
        thread_name = f"Thread{i}"
        request_type = random.choice([0, -1])
        volume = random.randint(1, 1024)
        request = (thread_name, request_type, volume)
        RAM_semaphore.acquire()
        request_queue.put(request)
        RAM_semaphore.release()
        time.sleep(random.uniform(0.1, 0.5))

def process_queue():
    while True:
        if not request_queue.empty():
            request = request_queue.get()
            handle_request(request)
            request_queue.task_done()
        else:
            time.sleep(0.1)

def create_request_threads():
    global request_thread
    for _ in range(num_requests):
        request_thread = threading.Thread(target=simulate_requests)
        request_thread.start()

def create_queue_thread():
    global queue_thread
    queue_thread = threading.Thread(target=process_queue)
    queue_thread.start()
    return queue_thread

def stop_threads():
    global request_thread, queue_thread
    request_thread.join()
    queue_thread.join()

if __name__ == "__main__":
    for i in range(num_requests):
       create_request_threads()
    queue_thread = create_queue_thread()
    time.sleep(5)
    stop_threads()
