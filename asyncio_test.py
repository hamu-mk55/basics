import asyncio
import time
import shutil
import os

import cv2
import numpy as np


class Timer:
    def __init__(self):
        self._start_time = time.time()

    def start(self):
        self._start_time = time.time()

    def wait(self, wait_msec: float, dt_msec: float | None = 10):

        while True:
            time_from_start = time.time() - self._start_time

            if time_from_start * 1000 > wait_msec:
                break

            if dt_msec is None:
                continue

            time.sleep(dt_msec / 1000)

    def show(self):
        _time = time.time() - self._start_time

        return _time * 1000


def save_image(img_path: str, img: np.array):
    cv2.imwrite(img_path, img)


def example(debug: bool = False):
    out_dir = './out'
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    img_path = '0_org.jpg'
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    cnt = 0
    timer = Timer()
    while True:
        cnt += 1

        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, save_image, f'{out_dir}/debug_{cnt:05d}.png', img)

        timer.wait(10, dt_msec=None)

        if debug:
            print(cnt, '\t', f'{timer.show() - 10:.3f}')

        timer.start()

        if cnt > 100:
            return


if __name__ == '__main__':
    example()
