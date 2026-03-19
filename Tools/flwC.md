flowchart TD
  A[Nhân viên: Lập phiếu đề nghị] -->|Gửi đề nghị| B[Hệ thống AIS: Module Đề nghị (Document)]
  B --> C{Trưởng phòng Vận hành kiểm tra}
  C -- Hợp lý --> D[Hệ thống AIS: Ghi nhận duyệt hạn mức]
  C -- Không hợp lý --> E[Trả về Nhân viên để chỉnh sửa]
  D --> F[Kế toán (Tổng hợp): Kiểm tra chứng từ & số dư tạm ứng]
  F --> G{Số dư OK và chứng từ hợp lệ?}
  G -- Có --> H[CEO: Phê duyệt nếu vượt hạn mức hoặc chi quản trị]
  G -- Không --> E
  H --> I[Kế toán (Thực chi): Lập phiếu chi / ủy nhiệm chi]
  I --> J[Ngân hàng: Duyệt lệnh chuyển khoản]
  J --> K[Ngân hàng: Thực hiện chuyển khoản]
  K --> L[Nhân viên nhận tiền]
  L --> M[Nhân viên: Nộp chứng từ gốc (Hoàn ứng)]
  M --> N[Kế toán: Quyết toán chênh lệch; Cập nhật sổ AIS]
  N --> O[Kho lưu trữ AIS: Lưu chứng từ & báo cáo]