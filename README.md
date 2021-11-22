# Socket

- Thì có 2 phần cần làm là, gửi list ListData.json qua từ sv qua cl để cl hiện thị danh sách, và từ list đó truy vấn về 1 địa điểm trong đó
  - Bên client thì phần gửi ListData.json được comment lại, phần không comment là truy vấn các hình cần thiết, vì có list.json rồi thì mấy thứ kia cũng đã có nên chỉ cần hình thôi
  - Server thì đã có thể gửi lại được

- Cl sẽ gửi command, sv gửi lại tên file rồi gửi tiếp data, khi cl đợi hết timeout (0.1s) thì sẽ ngưng tiếp tục như vậy.

- Folder ClientTmp/ để chứa data cho phần cl khi nhận được từ sv, để làm cache luôn còn ServerFile/ chưa data bên sv

# To-do

- [X] Cliet truy vấn server danh sách các địa điểm đang được server quản lý: mã số, tên địa điểm, vị trí địa lý (vĩ độ, kinh độ), mô tả
- [ ] Client truy vấn server 1 địa điểm thông tin: mã số, tên địa điểm, vị trí địa lý (vĩ độ, kinh độ), mô tả 
- [ ] Cần fix lại chỗ gửi hình từ sv -> cl còn bị mất dữ liệu nhiều.
- [ ] Thêm check nếu dữ liệu bên cl có trong ClientTmp/ thì không cần phải request lại