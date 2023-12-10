import os
import shutil

import cv2


class UsbCamera:
    """
    USBcameraに接続し、画像表示/保存を実施
    """

    def __init__(self,
                 camera_no: int = 0,
                 out_dir: str = './images'):
        """
        :param camera_no: USBカメラの接続番号
        :param out_dir: 画像保存先ホルダ
        """
        self.out_dir = out_dir
        if os.path.isdir(self.out_dir):
            shutil.rmtree(self.out_dir)
        os.makedirs(self.out_dir)

        self.cam = cv2.VideoCapture(camera_no)

    def set_params(self,
                   debug: bool = False):
        """
        :param debug: デバッグ出力
        :return:
        """
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 4000)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)

        if debug:
            self._show_params()

    def capture_loop(self):
        """
        カメラを連続撮像し、画像表示/保存を実施する。
        :return:
        """
        frame_cnt = 0
        while True:
            ret, frame = self.cam.read()

            if frame is None:
                print(f'ERROR: No Camera')
                break

            cv2.namedWindow('Camera View: Exit for q, Save for s', cv2.WINDOW_GUI_NORMAL)
            cv2.imshow('Camera View: Exit for q, Save for s', frame)

            # Key入力を確認し、終了or画像保存を実施
            _key = cv2.waitKey(1) & 0xFF
            if _key == ord('q'):
                break
            elif _key == ord('s'):
                cv2.imwrite(f'{self.out_dir}/{frame_cnt:03}.jpg', frame)
                frame_cnt += 1

        cv2.destroyAllWindows()

    def release(self):
        self.cam.release()

    def _show_params(self):
        print('BRIGHTNESS:', self.cam.get(cv2.CAP_PROP_BRIGHTNESS))
        print('GAIN:', self.cam.get(cv2.CAP_PROP_GAIN))
        print('SATURATION:', self.cam.get(cv2.CAP_PROP_SATURATION))
        print('SETTING:', self.cam.get(cv2.CAP_PROP_SETTINGS))
        print('WHITE BALANCE B:', self.cam.get(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U))
        print('WHITE BALANCE R:', self.cam.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V))
        print('WIDTH:', self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        print('HEIGHT:', self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print('EXPOSURE:', self.cam.get(cv2.CAP_PROP_EXPOSURE))
        print('MSEC:', self.cam.get(cv2.CAP_PROP_POS_MSEC))
        print('MODE:', self.cam.get(cv2.CAP_PROP_MODE))
        print('FPS:', self.cam.get(cv2.CAP_PROP_FPS))
        print('GUID:', self.cam.get(cv2.CAP_PROP_GUID))
        print('FOURCC:', self.cam.get(cv2.CAP_PROP_FOURCC))


if __name__ == '__main__':
    camera = UsbCamera(camera_no=0)
    camera.set_params()
    camera.capture_loop()
