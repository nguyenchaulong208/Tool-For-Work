HEADER_MAP = {
    "DATA_RAW": {
        "PO#": ["PO#", "PO #"],
        "Shipment": ["Shipment"],
        "Trucking": ["Trucking"],
        "Dịch vụ": ["Dịch vụ"]
    },

    "DATA_PROC": {
        "Số thứ tự": ["STT"],
        "Tên hàng hóa": ["Tên  hàng hóa, dịch vụ:"],
        "Biển kiểm soát": ["Biển kiểm soát"],
        "ĐVT": ["ĐVT"],
        "Đơn giá": ["Đơn giá dịch vụ"]
    },

    "DATA_DONE": {
        "Số chứng từ": ["Số chứng từ"],
        "Mã dịch vụ": ["Mã dịch vụ"],
        "Diễn giải": ["Diễn giải"],
        "Biển kiểm soát": ["Biển kiểm soát"],
        "Đơn vị tính": ["Đơn vị tính"],
        "Số lượng": ["Số lượng"],
        "Đơn giá": ["Đơn giá"]
    }
}


def search_header(df, sheet_name):
    results = {}

    if sheet_name not in HEADER_MAP:
        return results

    header_keywords = HEADER_MAP[sheet_name]

    for row_idx, row in df.iterrows():
        for col_idx, cell in enumerate(row.values):
            cell_text = str(cell).strip()

            for header_name, keywords in header_keywords.items():
                if any(key.lower() in cell_text.lower() for key in keywords):
                    results[header_name] = (row_idx + 1, col_idx)

    return results
