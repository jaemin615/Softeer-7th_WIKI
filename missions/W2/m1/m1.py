from multiprocessing import Pool
import time


def work_log(params: dict):
    """
    Executes a specific task based on the provided parameters.

    Args:
        params (dict): A dictionary containing task configuration.
            name (str): The name of the task.
            duration (int): The time in seconds the task should run.

    """
    try:
        task_name = params["name"]
        running_time = params["duration"]
        print(f"Process {task_name} waiting {running_time} seconds")
        time.sleep(running_time)
        print(f"Process {task_name} finished")
    except KeyError as e:
        print(f"Error: The key '{e.args[0]}' was not found in the dictionary.")


if __name__ == "__main__":
    work = [
        {"name": "A", "duration": 5},
        {"name": "B", "duration": 1},
        {"name": "C", "duration": 3},
        {"name": "D", "duration": 2},
        {"name": "E", "duration": 1},
    ]

    with Pool(processes=len(work)) as pool:
        result = pool.map(func=work_log, iterable=work)
