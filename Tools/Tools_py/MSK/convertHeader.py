def convert_header(df, headers):
    # Tìm dòng header bằng cách tìm tất cả các header trong sheet
    header_positions = [pos[0] for pos in headers.values()]
    header_row = min(header_positions) - 1  # dòng nhỏ nhất là header thật

    df.columns = df.iloc[header_row]
    df = df.iloc[header_row+1:]
    df = df.reset_index(drop=True)

    return df
