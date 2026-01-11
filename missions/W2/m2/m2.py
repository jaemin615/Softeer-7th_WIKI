from multiprocessing import Process


def print_continent_name(continent: str = "Asia"):
    print(f"The name of continet is : {continent}")


if __name__ == "__main__":
    processes = []
    continent_list = ["America", "Europe", "Africa"]

    for continent in continent_list:
        processes.append(Process(target=print_continent_name, args=(continent,)))

    processes.append(Process(target=print_continent_name, args=()))

    for process in processes:
        process.start()

    for process in processes:
        process.join()
