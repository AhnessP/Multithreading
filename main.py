import threading
import time
import random
from queue import Queue

RAM_size = 1000
current_RAM = RAM_size
request_queue = Queue()
num_requests = 2
lock = threading.Lock()
exit_flag = False


def handle_request(request):
    global current_RAM, request_queue
    thread_name, request_type, volume = request
    if request_type == 0:
        print(f"Received request from {thread_name} to allocate {volume} KB.")
        allocation_request(volume, thread_name)
    else:
        print(f"Received request from {thread_name} to utilize {volume} KB")
        utilization_request(volume, thread_name)


def allocation_request(volume, thread_name):
    global current_RAM
    lock.acquire()  # Acquire the lock before accessing shared variable
    if volume <= current_RAM:
        current_RAM -= volume
        print(f"Allocated {volume} KB of RAM to {thread_name}")
        print(f"Current RAM is {current_RAM}")
    else:
        print(f"Not enough RAM available to allocate {volume} KB to {thread_name}")
        print(f"Current RAM is {current_RAM}")
    lock.release()  # Release the lock after accessing shared variable


def utilization_request(volume, thread_name):
    global current_RAM
    lock.acquire()  # Acquire the lock before accessing shared variable
    if volume <= RAM_size - current_RAM:
        current_RAM += volume
        print(f"Utilized  {volume} KB of RAM by {thread_name}")
    else:
        print(f"Not enough RAM taken to utilize {volume} KB by {thread_name}")
    lock.release()  # Release the lock after accessing shared variable


def simulate_requests():
    for i in range(num_requests):
        thread_name = threading.current_thread().getName()
        request_type = random.choice([0, -1])
        volume = random.randint(1, 1024)
        request = (thread_name, request_type, volume)
        request_queue.put(request)
        time.sleep(random.uniform(0.1, 0.5))


def process_queue():
    while not exit_flag:
        if not request_queue.empty():
            request = request_queue.get()
            handle_request(request)
            request_queue.task_done()
        else:
            time.sleep(0.1)


def create_request_threads():
    for i in range(num_requests):
        request_thread = threading.Thread(target=simulate_requests)
        request_thread.start()


def create_queue_thread():
    queue_thread = threading.Thread(target=process_queue)
    queue_thread.start()
    return queue_thread


def stop_threads():
    global exit_flag  # use the global flag variable
    exit_flag = True  # set the flag to signal the threads to exit
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()


if __name__ == "__main__":
    # create and start the request threads
    create_request_threads()
    # create and start the queue thread
    queue_thread = create_queue_thread()
    # wait for 5 seconds before stopping the threads
    time.sleep(2)
    # stop the threads
    stop_threads()
