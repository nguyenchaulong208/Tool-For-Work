def get_po_for_shipment(df_raw, shipment_value, shipment_col_raw, po_col_raw):
    shipment_value = str(shipment_value).strip().lower()

    for _, raw_row in df_raw.iterrows():
        raw_shipment = str(raw_row[shipment_col_raw]).strip().lower()
        if raw_shipment == shipment_value:
            return str(raw_row[po_col_raw]).strip()

    return None
