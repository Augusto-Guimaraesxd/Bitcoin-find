from threading import Thread, Event
from bitcoin_find import encontrar_bitcoins

def worker_thread(key, min_value, max_value, should_stop):
    encontrar_bitcoins(key, min_value, max_value, should_stop.is_set)

if __name__ == "__main__":
    import sys
    import json

    worker_data = json.loads(sys.argv[1])
    should_stop_event = Event()

    worker = Thread(target=worker_thread, args=(worker_data["key"], worker_data["min"], worker_data["max"], should_stop_event))
    worker.start()

    try:
        worker.join()
    except KeyboardInterrupt:
        should_stop_event.set()
        worker.join()