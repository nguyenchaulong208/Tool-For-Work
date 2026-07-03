Tôi có 1 file excel gồm có 3 sheet (các dữ liệu bên trong là dữ liệu mẫu dùng để xử lý project này):
- DATA_RAW: Chứa dữ liệu thô, bao gồm và có các cột với các header cố định cần quan tâm là PO#; Shipment; TTHQ Dán nhãn/ Chỉnh Bill/ Bổ sung Manifest/ Hủy TK/ Lệch kg; Trucking; Dịch vụ.
- DATA_PROC: chứa dữ liệu đã được xử lý với template cố định.
- DATA_DONE: là 1 template cố định được dùng để add vào 1 phần mềm quản lý

#I. Mô tả chi tiết về các file
##1. DATA_RAW: 
Mỗi một``PO#`` sẽ gắn với 1``Shipment`` tương ứng, và các dữ liệu tương ứng sẽ đi kèm với dữ liệu tương ứng của dòng đó. file này dùng làm file nguồn để xử lý dữ liệu
##2. DATA_PROC
Ghép chuỗi với quy tắc sau:
- Ở Header số thứ tự sẽ đánh số với quy tắc là 1 dòng diễn giải và các dòng tiếp theo phía dưới diễn giải sẽ đi cùng với diễn giải đó. Các dữ liệu này sẽ được xử lý thủ công, bạn không cần thao tác ở phần này
##3. DATA_DONE
- Công việc ở file này bao gồm:
 - Ghép chuỗi ở header ``Tên  hàng hóa, dịch vụ:`` hoặc tương đương như vậy với các ``Shipment`` được điền trong sheet ``DATA_PROC`` vào cột ``Diễn giải``
Sử dụng dữ liệu từ ``DATA_RAW``  để lấy ``PO#`` từ ``Shipment`` được điền ở sheet ``DATA_PROC``
 - Sắp xếp và xử lý dữ liệu theo quy tắc sau:
   + Mỗi một ``Shipment`` (bao gồm cả ``PO#`` của ``Shipment`` đó) được ghi nhận là cùng 1 số chứng từ, các ``Shipment`` tiếp theo sẽ được đánh số tăng dần.
   +Tại ``Mã dịch vụ`` sẽ xử lý theo keyword, nếu trong ``Diễn giải`` có chứa cụm từ *"Phí dịch vụ thủ tục Hải quan"* thì sẽ gán ``Mã dịch vụ`` là *"DVHQ"*, nếu trong ``Diễn giải`` có chứa cụm từ *" vận chuyển xe tải "* thì sẽ gán ``Mã dịch vụ`` là *"DVVC2"*,  nếu trong ``Diễn giải`` có chứa cụm từ *" vận chuyển xe cont"* thì sẽ gán ``Mã dịch vụ`` là *"DVVC1"*
   + Các cột còn lại thì điền theo header tương ứng trong sheet ``DATA_PROC``
   