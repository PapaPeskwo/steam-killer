import psutil
import time
import os
import sys

def find_steam_process():
    for process in psutil.process_iter(['name']):
        if process.info['name'] and process.info['name'].lower() == 'steam.exe':
            return process
    return None

def kill_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
    except psutil.NoSuchProcess:
        print("Process not found.")

def countdown_timer(remaining_time):
    sys.stdout.write("\rTime remaining: %02d:%02d" % divmod(remaining_time, 60))
    sys.stdout.flush()

def main():
    print("Monitoring for Steam process...")

    start_time = None
    max_duration = 60 * 30  # 30 min in seconds
    check_interval = 1

    while True:
        steam_process = find_steam_process()

        if steam_process:
            if start_time is None:
                start_time = time.time()
                print("Steam process found. Started monitoring.")
            
            elapsed_time = time.time() - start_time
            remaining_time = max_duration - elapsed_time

            if remaining_time <= 0:
                print("\n1 hour has passed. Terminating Steam process.")
                kill_process(steam_process.pid)
                break

            countdown_timer(int(remaining_time))
        else:
            start_time = None

        time.sleep(check_interval)

if __name__ == '__main__':
    main()
