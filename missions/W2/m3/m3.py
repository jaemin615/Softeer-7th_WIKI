from multiprocessing import Queue


def main():
    colors = ["red", "green", "blue", "black"]
    item_queue = Queue()

    print("pushing items to queue")
    for idx, item in enumerate(colors):
        item_queue.put(item)
        print(f"item no: {idx + 1} {item}")

    print("popping items from queue")
    item_cnt = 0
    while not item_queue.empty():
        item = item_queue.get()
        print(f"item no: {item_cnt} {item}")
        item_cnt += 1


if __name__ == "__main__":
    main()
