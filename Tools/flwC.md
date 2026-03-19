```mermaid
flowchart TD
    %% TERMINAL
    A([BẮT ĐẦU])

    %% DOCUMENT: Phiếu đề nghị
    D1[/Phiếu đề nghị tạm ứng / thanh toán/]

    %% PROCESS: Nhân viên lập đề nghị
    B[Nhân viên lập đề nghị<br/>tạm ứng / thanh toán]

    %% DECISION: Thông tin & nợ
    C{Thông tin đủ<br/>& không nợ quá hạn?}

    %% PROCESS: Từ chối / trả lại
    C1[ TỪ CHỐI / TRẢ LẠI ]

    %% PROCESS: Trưởng phòng vận hành kiểm tra
    D[Trưởng phòng vận hành<br/>kiểm tra hợp lý theo Tariff]

    %% DECISION: Hợp lý theo hạn mức
    E{Hợp lý theo<br/>hạn mức chi?}

    %% PROCESS: Từ chối
    E1[ TỪ CHỐI ]

    %% PROCESS: Kế toán kiểm tra chứng từ & nợ
    F[Kế toán kiểm tra<br/>chứng từ & số dư nợ cũ]

    %% DECISION: Đạt chuẩn & không nợ
    G{Đạt chuẩn<br/>& không nợ?}

    %% PROCESS: Trả lại
    G1[ TRẢ LẠI ]

    %% PROCESS: Giám đốc điều hành phê duyệt
    H[Giám đốc điều hành<br/>phê duyệt chủ trương]

    %% DECISION: Phê duyệt chủ trương
    I{Phê duyệt<br/>chủ trương chi?}

    %% PROCESS: Dừng quy trình
    I1[ DỪNG QUY TRÌNH ]

    %% DOCUMENT: Phiếu chi / UNC
    D2[/Phiếu chi / Ủy nhiệm chi (UNC)/]

    %% PROCESS: Kế toán thực chi
    J[Kế toán thực chi<br/>lập Phiếu chi / UNC]

    %% DECISION: Thông tin chứng từ chi
    K{Thông tin chứng từ chi<br/>chính xác?}

    %% PROCESS: Sửa lại thông tin
    K1[ Sửa lại thông tin ]

    %% PROCESS: Duyệt lệnh ngân hàng
    L[Duyệt lệnh ngân hàng]

    %% DECISION: Duyệt lệnh chuyển khoản
    M{Duyệt lệnh<br/>chuyển khoản?}

    %% PROCESS: Dừng quy trình
    M1[ DỪNG QUY TRÌNH ]

    %% DOCUMENT: Chứng từ gốc
    D3[/Chứng từ gốc 3–5 ngày/]

    %% PROCESS: Nhân viên nộp chứng từ
    N[Nhân viên nộp chứng từ gốc<br/>trong 3–5 ngày]

    %% PROCESS: Kế toán quyết toán
    O[Kế toán quyết toán chênh lệch]

    %% DATABASE: Lưu hồ sơ kế toán
    P[(Lưu hồ sơ kế toán<br/>hệ thống / hồ sơ giấy)]

    %% TERMINAL
    Q([KẾT THÚC])

    %% FLOW
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
