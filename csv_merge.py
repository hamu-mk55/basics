import glob
import csv
import os


def csv_merge(data_dir: str = './data',
              merge_file: str = 'merge.csv'
              ) -> None:
    """
    data_dirの中のCSVファイルをマージして出力する。
    マージファイルには、元ファイルのホルダ名/ファイル名も出力する。
    :param data_dir: データホルダ名
    :param merge_file: マージファイル名
    :return:
    """

    # mergeファイルがあれば消去する
    if os.path.isfile(merge_file):
        os.remove(merge_file)

    # ファイル探索
    filenames = glob.glob(f'{data_dir}/**/*.csv', recursive=True)
    for file_cnt, filename in enumerate(filenames):
        print(filename)
        _dir = os.path.dirname(filename)
        _file = os.path.basename(filename)

        fr = open(filename, "r")
        log = csv.reader(fr, delimiter=',', lineterminator='\n')

        fw = open(merge_file, 'a')
        csvWriter = csv.writer(fw, lineterminator='\n')
        for row_cnt, row in enumerate(log):
            # 最初のファイルの場合、ヘッダを出力
            if file_cnt == 0 and row_cnt == 0:
                row = ['dir_name', 'file_name'] + row
                csvWriter.writerow(row)

            # データ出力
            elif row_cnt > 0:
                row = [_dir, _file] + row
                csvWriter.writerow(row)

        fw.close()
        fr.close()


if __name__ == '__main__':
    csv_merge()
