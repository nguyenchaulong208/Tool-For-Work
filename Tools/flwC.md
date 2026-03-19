```mermaid
flowchart TD

    %% TERMINAL
    A([BẮT ĐẦU])

    %% DOCUMENT: Phiếu đề nghị
    D1[/Phiếu đề nghị tạm ứng / thanh toán/]

    %% PROCESS
    B[Nhân viên lập đề nghị tạm ứng / thanh toán]

    %% DECISION
    C{Thông tin đầy đủ và không nợ quá hạn?}

    C1[ TỪ CHỐI / TRẢ LẠI ]

    D[Trưởng phòng vận hành kiểm tra hợp lý theo Tariff]

    E{Hợp lý theo hạn mức chi?}

    E1[ TỪ CHỐI ]

    F[Kế toán kiểm tra chứng từ & số dư nợ cũ]

    G{Đạt chuẩn và không nợ?}

    G1[ TRẢ LẠI ]

    H[Giám đốc điều hành phê duyệt chủ trương]

    I{Phê duyệt chủ trương chi?}

    I1[ DỪNG QUY TRÌNH ]

    %% DOCUMENT
    D2[/Phiếu chi / Ủy nhiệm chi (UNC)/]

    J[Kế toán thực chi]

    K{Thông tin chứng từ chi chính xác?}

    K1[ Sửa lại thông tin ]

    L[Duyệt lệnh ngân hàng]

    M{Duyệt lệnh chuyển khoản?}

    M1[ DỪNG QUY TRÌNH ]

    %% DOCUMENT
    D3[/Chứng từ gốc 3–5 ngày/]

    N[Nhân viên nộp chứng từ gốc]

    O[Kế toán quyết toán chênh lệch]

    %% DATABASE
    P[(Lưu hồ sơ kế toán)]

    Q([KẾT THÚC])


    %% FLOW CONNECTIONS
    A --> B --> D1 --> C
    C -- Không --> C1
    C -- Có --> D

    D --> E
    E -- Không --> E1
    E -- Có --> F

    F --> G
    G -- Không --> G1
    G -- Có --> H

    H --> I
    I -- Không --> I1
    I -- Có --> J

    J --> D2 --> K
    K -- Không --> K1 --> J
    K -- Có --> L

    L --> M
    M -- Không --> M1
    M -- Có --> N

    N --> D3 --> O --> P --> Q
```
