from multiprocessing import Process, Queue
import time
import queue


def execute_task(process_no, tasks_to_accomplish, tasks_that_are_done):
    """Retrieves tasks from a queue and stores completion messages in another queue."""
    while True:
        try:
            task = tasks_to_accomplish.get_nowait()
            time.sleep(0.5)
            completion_message = f"{task} is done by Process-{process_no}"
            tasks_that_are_done.put(completion_message)
            print(completion_message)

        except queue.Empty:
            break


def main():
    tasks_to_accomplish = Queue()
    tasks_that_are_done = Queue()

    for task_no in range(10):
        task_creation_message = f"Task no {task_no}"
        tasks_to_accomplish.put(task_creation_message)
        print(task_creation_message)

    processes = []
    for process_no in range(1, 5):
        p = Process(
            target=execute_task,
            args=(process_no, tasks_to_accomplish, tasks_that_are_done),
        )
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
