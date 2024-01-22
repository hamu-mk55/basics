import glob
import os


def _show_dir(target_dir: str,
              depth: int,
              depth_max: int,
              file_max: int,
              depth_str: str = '---') -> None:
    if depth > depth_max: return

    files_and_dirs = glob.glob(f'{target_dir}/*')
    files_and_dirs.sort(key=lambda x: True if os.path.isfile(x) else False)

    file_cnt = 0
    for item in files_and_dirs:
        if os.path.isdir(item):
            print(f'{depth_str * depth}{os.path.basename(item)}')
            _show_dir(item, depth + 1, depth_max, file_max, depth_str)
        else:
            file_cnt += 1
            if file_cnt < file_max + 1:
                print(f'{depth_str * depth}{os.path.basename(item)}')
            elif file_cnt == file_max + 1:
                print(f'{depth_str * depth}etc...')
            else:
                break


def show_dir_items(data_dir: str = '.',
                   show_depth_num: int = 3,
                   show_file_num: int = 3) -> None:
    """
    ホルダ内のホルダ/ファイルを探索し、ホルダ構造を出力する
    :param data_dir: 探索する親ホルダ
    :param show_depth_num: どこまで深いホルダを探索するか
    :param show_file_num: 同一ホルダ内のファイルを何個出力するか
    :return:
    """
    _show_dir(data_dir, 0, show_depth_num, show_file_num, '\t')


if __name__ == '__main__':
    show_dir_items()
