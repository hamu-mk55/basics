import pandas as pd

def _find_start_cell(df: pd.DataFrame,
                     start_key: str):

    # strip
    df = df.map(lambda x: str(x).strip() if pd.notna(x) else x)
    start_key = start_key.strip()

    # start_keyが含まれているか判別。含まれてなければNoneを返す
    matched_cells = (df == start_key)
    if not matched_cells.any().any():
        return None

    # 左上の行番号・列番号を返す
    rows, cols = matched_cells.to_numpy().nonzero()
    row_no = int(rows.min())
    col_no = int(cols[rows == row_no].min())

    return row_no, col_no

def _clean_dataframe(df_org: pd.DataFrame, row0: int, col0: int) -> pd.DataFrame:

    df = df_org.iloc[row0:, col0:].copy()

    # 先頭行をヘッダーへ
    header = df.iloc[0].astype(str).str.strip()
    df = df.iloc[1:].reset_index(drop=True)
    df.columns = header

    # 全NaNの行をドロップ。列は保持しておく。
    df = df.dropna(axis=0, how='all')

    return df

def main():
    sheets = pd.read_excel("データ.xlsx", sheet_name=None)

    for sheet_name, df in sheets.items():
        print(sheet_name)

        ret = _find_start_cell(df, start_key='検査日')

        if ret is None:
            continue

        df = _clean_dataframe(df,ret[0], ret[1])
        print(df.head(100))


if __name__ == '__main__':
    main()

