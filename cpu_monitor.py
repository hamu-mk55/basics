import time
import psutil


class CpuMonitor:
    def __init__(self, interval_sec=10):
        self.interval_sec = interval_sec

    def check_cpu(self):
        _cpu = psutil.cpu_percent()
        _mem_total = psutil.virtual_memory().total
        _mem_percent = psutil.virtual_memory().percent
        _swap_total = psutil.swap_memory().total
        _swap_percent = psutil.swap_memory().percent

        print(f'{_cpu},{_mem_total},{_mem_percent},{_swap_total},{_swap_percent}')

    def run(self):

        while True:
            self.check_cpu()
            time.sleep(self.interval_sec)


if __name__ == '__main__':
    app = CpuMonitor()
    app.run()







