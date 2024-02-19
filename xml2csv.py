import glob
import csv
import xml.etree.ElementTree as ET


def save_csv_list(output_list: list, csv_file: str):
    """
    listの内容をcsvfileへ保存する
    :param output_list: 出力項目のリスト
    :param csv_file: 出力ファイル名
    :return:
    """

    f = open(csv_file, 'a')
    csvWriter = csv.writer(f, lineterminator='\n')

    for _item in output_list:
        csvWriter.writerow(_item)

    f.close()
    return 1


def xml2csv(data_dir: str = '.', res_file: str = 'results.csv', debug: bool = False):
    """
    dataホルダ中のxmlファイルを確認し、内容をCSVに出力する
    :param data_dir: データホルダ名
    :param res_file: 出力ファイル名
    :param debug: デバッグ出力するかどうか
    :return:
    """

    file_names = glob.glob(f"{data_dir}/*.xml")
    for file_name in file_names:
        print(file_name)

        xml = ET.parse(file_name)
        root = xml.getroot()

        if debug:
            print(root)
            print(root.tag)
            print(root.attrib)

        out_list = []
        for child1 in root:
            if debug:
                print(f'\t tag:{child1.tag}')
                print(f'\t attrib:{child1.attrib}')
                print(f'\t text:{child1.text}')

            out_list.append([file_name, "1st", child1.tag, child1.attrib, child1.text])

            if len(child1) == 0: continue
            for child2 in child1:
                if debug:
                    print(f'\t\t tag:{child2.tag}')
                    print(f'\t\t attrib:{child2.attrib}')
                    print(f'\t\t text:{child2.text}')

                out_list.append([file_name, "2nd", child2.tag, child2.attrib, child2.text])

                if len(child2) == 0: continue
                for child3 in child2:
                    if debug:
                        print(f'\t\t\t tag:{child3.tag}')
                        print(f'\t\t\t attrib:{child3.attrib}')
                        print(f'\t\t\t text:{child3.text}')

                    out_list.append([file_name, "3rd", child3.tag, child3.attrib, child3.text])

        save_csv_list(out_list, res_file)


if __name__ == '__main__':
    xml2csv(debug=True)
