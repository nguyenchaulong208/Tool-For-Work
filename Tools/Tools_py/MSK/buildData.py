import re
from collections import OrderedDict
from Tools_py.MSK.getShipment import get_po_for_shipment

SHIPMENT_PATTERN = re.compile(r"[A-Z]{3,6}[A-Z0-9]{2,6}")

def extract_shipments(value: str):
    parts = [v.strip() for v in value.split(",")]
    return [p for p in parts if SHIPMENT_PATTERN.fullmatch(p)]


def build_data_done(df_raw, df_proc, headers_raw, headers_proc):
    po_col_raw = df_raw.columns[headers_raw["PO#"][1]]
    shipment_col_raw = df_raw.columns[headers_raw["Shipment"][1]]

    ten_hh_col = df_proc.columns[headers_proc["Tên hàng hóa"][1]]

    # shipment -> list[description]
    shipment_map: dict[str, list[str]] = OrderedDict()

    current_description = None

    # Bước 1: gom description theo shipment
    for _, proc_row in df_proc.iterrows():
        value = str(proc_row[ten_hh_col]).strip()

        # Dòng tiêu đề dịch vụ
        if value.endswith(":") and not SHIPMENT_PATTERN.fullmatch(value):
            current_description = value.rstrip(":")
            continue

        # Dòng chứa shipment
        shipments = extract_shipments(value)
        if shipments and current_description:
            for shipment_value in shipments:
                if shipment_value not in shipment_map:
                    shipment_map[shipment_value] = []
                # tránh trùng description
                if current_description not in shipment_map[shipment_value]:
                    shipment_map[shipment_value].append(current_description)

    # Bước 2: xuất ra rows_done theo từng shipment
    rows_done = []
    so_ct = 1

    for shipment_value, descriptions in shipment_map.items():
        # Lấy PO từ DATA_RAW
        po_value = get_po_for_shipment(
            df_raw,
            shipment_value,
            shipment_col_raw,
            po_col_raw
        )

        ct = f"CT{so_ct:06d}"

        # Các dòng dịch vụ
        for desc in descriptions:
            rows_done.append({
                "Số chứng từ": ct,
                "Nội dung": f"{desc}: {shipment_value}",
            })

        # Dòng PO
        rows_done.append({
            "Số chứng từ": ct,
            "Nội dung": f"PO {po_value}",
        })

        so_ct += 1

    return rows_done
