flowchart TD
    A([BẮT ĐẦU]) --> B[Nhân viên lập đề nghị<br/>tạm ứng / thanh toán]

    B --> C{Thông tin đủ<br/>& không nợ quá hạn?}
    C -- Không --> C1[ TỪ CHỐI / TRẢ LẠI ]
    C -- Có --> D[Trưởng phòng vận hành<br/>kiểm tra hợp lý theo Tariff]

    D --> E{Hợp lý theo<br/>hạn mức chi?}
    E -- Không --> E1[ TỪ CHỐI ]
    E -- Có --> F[Kế toán kiểm tra<br/>chứng từ & số dư nợ cũ]

    F --> G{Đạt chuẩn<br/>& không nợ?}
    G -- Không --> G1[ TRẢ LẠI ]
    G -- Có --> H[Giám đốc điều hành<br/>phê duyệt chủ trương]

    H --> I{Phê duyệt<br/>chủ trương chi?}
    I -- Không --> I1[ DỪNG QUY TRÌNH ]
    I -- Có --> J[Kế toán thực chi<br/>Phiếu chi / Ủy nhiệm chi]

    J --> K{Thông tin UNC / phiếu chi<br/>chính xác?}
    K -- Không --> K1[ Sửa lại thông tin ]
    K -- Có --> L[Duyệt lệnh ngân hàng]

    L --> M{Duyệt lệnh<br/>chuyển khoản?}
    M -- Không --> M1[ DỪNG QUY TRÌNH ]
    M -- Có --> N[Nhân viên nộp chứng từ gốc<br/>3–5 ngày]

    N --> O[Kế toán quyết toán chênh lệch]
    O --> P[Lưu hồ sơ kế toán]
    P --> Q([KẾT THÚC])
