"""Script tạo dataset tiếng Việt cho spam detection."""
import csv
import random

random.seed(42)

SPAM = [
    # Vay tiền / Tín dụng
    "Vay tiền nhanh không cần thế chấp lãi suất 0% nhận tiền ngay trong 30 phút liên hệ hotline 0987654321",
    "Cho vay online tối đa 50 triệu đồng lãi suất thấp chỉ từ 0.5 phần trăm mỗi tháng duyệt hồ sơ trong ngày",
    "Cần tiền gấp vay ngay 10 triệu không cần gặp mặt không cần chứng minh thu nhập duyệt trong 15 phút",
    "Dịch vụ cho vay nhanh uy tín hỗ trợ 24 giờ 7 ngày trong tuần không giới hạn số tiền vay lãi suất cực thấp",
    "THÔNG BÁO QUAN TRỌNG bạn đã được duyệt khoản vay 20 triệu đồng nhấp vào link nhận tiền ngay hôm nay",
    "Vay tiêu dùng không thế chấp lãi suất ưu đãi chỉ cần CMND giải ngân trong vòng 1 giờ toàn quốc",
    "Bạn đang cần tiền gấp chúng tôi hỗ trợ vay online từ 5 triệu đến 100 triệu không cần gặp mặt nhận tiền ngay",
    "Cho vay tiêu dùng nhanh chóng lãi suất siêu thấp chỉ cần số điện thoại và CMND giải ngân trong vài giờ",
    "App vay tiền online duyệt 100% hồ sơ không từ chối ai nhận tiền trong 10 phút đăng ký ngay hôm nay",
    "Cần tiền trả nợ vay ngay không hỏi lý do lãi suất 0% tháng đầu sau đó chỉ 1% mỗi tháng đăng ký ngay",

    # Xổ số / Trúng thưởng
    "CHÚC MỪNG bạn đã trúng thưởng 1 tỷ đồng từ chương trình khách hàng thân thiết vui lòng gọi ngay để nhận thưởng",
    "Bạn là người may mắn trúng thưởng iPhone 15 Pro Max bấm vào đây để xác nhận và nhận quà ngay hôm nay",
    "Thông báo trúng thưởng chương trình bốc thăm may mắn số tài khoản của bạn trúng giải 500 triệu đồng",
    "XIN CHÚC MỪNG bạn đã được chọn là 1 trong 10 khách hàng may mắn nhận giải thưởng 200 triệu đồng",
    "Bạn vừa trúng xổ số đặc biệt trị giá 2 tỷ đồng vui lòng cung cấp thông tin tài khoản để chuyển tiền thưởng",
    "Kết quả quay thưởng tháng này bạn là người may mắn nhất nhận ngay 100 triệu đồng chỉ cần xác minh tài khoản",
    "PHẦN THƯỞNG ĐẶC BIỆT dành cho bạn trúng thưởng chuyến du lịch Châu Âu trị giá 150 triệu gọi ngay để nhận",
    "Chương trình tri ân khách hàng số điện thoại của bạn may mắn trúng thưởng xe máy Honda trị giá 50 triệu",
    "Thư chúc mừng số điện thoại 0987654321 đã được hệ thống chọn ngẫu nhiên trúng thưởng 1 chiếc ô tô",
    "Bạn vừa được chọn ngẫu nhiên từ hàng triệu khách hàng để nhận giải thưởng đặc biệt trị giá 500 triệu đồng",

    # Đầu tư / Tiền điện tử / Forex
    "Đầu tư Bitcoin ngay hôm nay lợi nhuận 300 phần trăm mỗi tháng cam kết không rủi ro hoàn vốn 100 phần trăm",
    "Cơ hội đầu tư sinh lời cực cao chỉ bỏ vốn 5 triệu nhận về 15 triệu sau 30 ngày đã có 10000 người tham gia",
    "Sàn giao dịch Forex uy tín nhất Việt Nam đăng ký ngay nhận bonus 100 USD bắt đầu kiếm tiền từ hôm nay",
    "Đầu tư vàng online lợi nhuận 50 phần trăm mỗi tháng không cần kinh nghiệm hệ thống tự động giao dịch",
    "Mô hình đầu tư MLM lợi nhuận thụ động 1 triệu mỗi ngày chỉ cần giới thiệu 3 người bạn bè tham gia",
    "Nhóm đầu tư tài chính kín lợi nhuận 200 phần trăm trong 2 tuần chỉ nhận 100 thành viên đăng ký gấp",
    "Cơ hội làm giàu nhanh chóng đầu tư tiền điện tử cùng chuyên gia tài chính cam kết lãi 30 phần trăm mỗi tuần",
    "Hệ thống auto trading chứng khoán Mỹ lợi nhuận 500 phần trăm mỗi năm đăng ký ngay giới hạn 50 suất",
    "Đầu tư bất động sản online chỉ từ 1 triệu đồng lợi nhuận 20 phần trăm mỗi tháng an toàn và minh bạch",
    "Cơ hội đầu tư hiếm có sinh lời 1000 phần trăm trong 6 tháng đã có 50000 nhà đầu tư thành công tham gia",

    # Casino / Cờ bạc
    "Tải app casino online nhận ngay 500K tiền thưởng không cần nạp tiền chơi ngay thắng lớn mỗi ngày",
    "Chơi game bài đổi thưởng kiếm tiền thật nạp 100K nhận 300K thắng lớn rút ngay về tài khoản ngân hàng",
    "Sòng bạc online uy tín nhất châu Á đăng ký ngay nhận 1 triệu đồng tiền thưởng chào mừng thành viên mới",
    "App game bài xóc đĩa online nhận thưởng tiền thật ngay nạp tối thiểu 50K nhận thưởng 200K chơi ngay",
    "Xổ số online trúng tiền thật mỗi ngày tham gia ngay nhận vé số miễn phí cơ hội trúng 1 tỷ đồng mỗi ngày",
    "Game cá cược bóng đá online thắng tiền thật đặt cược 100K có thể nhận về 10 triệu đồng đăng ký ngay",
    "Casino trực tuyến uy tín nạp 200K tặng thêm 500K khuyến mãi đặc biệt thành viên mới chơi poker blackjack",
    "Tải ngay app slot game đổi thưởng tiền thật mỗi vòng quay cơ hội trúng jackpot 5 tỷ đồng đăng ký miễn phí",

    # Việc làm / Thu nhập cao
    "Tuyển dụng làm việc tại nhà thu nhập 50 triệu mỗi tháng không cần kinh nghiệm chỉ cần có điện thoại internet",
    "Cơ hội việc làm online từ xa lương khủng 30 đến 100 triệu mỗi tháng làm việc thoải mái tự do thời gian",
    "Tuyển cộng tác viên online không cần bằng cấp thu nhập 20 triệu mỗi tháng chỉ cần 2 đến 3 giờ mỗi ngày",
    "Kiếm tiền online với Facebook chỉ cần bấm like share bình luận thu nhập thêm 10 triệu mỗi tháng không vốn",
    "Việc làm thêm tại nhà cho sinh viên nội trợ thu nhập 5 đến 15 triệu mỗi tháng làm theo giờ rảnh linh hoạt",
    "Tuyển nhân viên content nhập liệu online từ xa lương 500K đến 1 triệu mỗi ngày làm việc chỉ 2 giờ ngày",
    "Cơ hội kiếm tiền thụ động thật sự không cần bán hàng không cần giới thiệu thu nhập tự động 24 giờ mỗi ngày",
    "Tuyển gấp 100 cộng tác viên toàn quốc thu nhập 200K mỗi ngày chỉ cần có điện thoại không cần kinh nghiệm",

    # Giảm giá / Flash sale giả
    "FLASH SALE 24 GIỜ giảm giá sốc đến 90 phần trăm tất cả sản phẩm mua ngay trước khi hết hàng hôm nay",
    "Siêu sale cuối năm giảm đến 80 phần trăm hàng ngàn sản phẩm chính hãng mua ngay giá rẻ nhất năm",
    "Khuyến mãi đặc biệt mua 1 tặng 2 áp dụng hôm nay chỉ hôm nay đừng bỏ lỡ cơ hội mua hàng giá rẻ",
    "Clearance sale hàng tồn kho giảm đến 95 phần trăm hàng hiệu xách tay chính hãng số lượng có hạn mua ngay",
    "Mua hàng hiệu Mỹ chính hãng giá chỉ bằng 10 phần trăm giá thị trường ship toàn quốc miễn phí bảo đảm chất lượng",
    "Deal sốc ngày hôm nay điện thoại Samsung iPhone giảm giá 70 phần trăm hàng chính hãng full box mua ngay",
    "Túi xách Gucci Louis Vuitton hàng hiệu authentic giá chỉ 500K đến 2 triệu ship toàn quốc cam kết chính hãng",

    # Thuốc / Sức khỏe giả
    "Thuốc giảm cân thần kỳ giảm 10 kg trong 1 tháng không cần ăn kiêng không cần tập thể dục kết quả đảm bảo",
    "Viên uống tăng chiều cao hiệu quả 5 đến 10 cm sau 3 tháng sử dụng kết quả thật sự cam kết hoàn tiền",
    "Kem trắng da nhanh chóng trắng da toàn thân chỉ sau 7 ngày không hóa chất an toàn cho da nhạy cảm",
    "Thuốc tăng cường sinh lý nam cải thiện rõ rệt chỉ sau 1 tuần sử dụng chiết xuất thiên nhiên 100 phần trăm",
    "Thực phẩm chức năng chữa tiểu đường cao huyết áp mỡ máu hiệu quả sau 1 liệu trình cam kết khỏi bệnh hoàn toàn",
    "Thần dược từ thảo dược thiên nhiên giúp ngủ ngon sâu giấc thức dậy tỉnh táo không gây nghiện không tác dụng phụ",
    "Gel tăng kích thước vòng 1 vòng 3 hiệu quả sau 30 ngày kết quả vĩnh viễn không cần phẫu thuật đặt hàng ngay",

    # Phishing / Lừa đảo
    "Tài khoản ngân hàng của bạn bị khóa vui lòng truy cập link để xác minh thông tin và mở khóa ngay lập tức",
    "Cập nhật thông tin tài khoản Zalo của bạn để tránh bị khóa vĩnh viễn bấm vào đây để xác nhận ngay",
    "Hệ thống phát hiện đăng nhập bất thường vào tài khoản của bạn vui lòng xác minh ngay tại link bên dưới",
    "Thông báo khẩn từ ngân hàng VCB tài khoản của bạn bị giới hạn giao dịch vui lòng xác minh danh tính ngay",
    "Bạn có gói thưởng chưa được kích hoạt từ Momo vui lòng nhập OTP để nhận 200K tiền thưởng vào ví ngay",
    "Tài khoản Facebook của bạn vi phạm chính sách cộng đồng vui lòng xác minh thông tin để tránh bị xóa tài khoản",
    "Cảnh báo bảo mật tài khoản Shopee của bạn đang bị truy cập từ thiết bị lạ bấm vào đây xác nhận ngay",
    "Ngân hàng ACB thông báo thẻ tín dụng của bạn hết hạn vui lòng cập nhật thông tin thẻ tại đây ngay",

    # Bất động sản lừa đảo
    "Đất nền trung tâm thành phố giá chỉ 500 triệu mảnh mua ngay kẻo hết số lượng cực kỳ hạn chế",
    "Cho thuê nhà nguyên căn giá rẻ chỉ 2 triệu mỗi tháng full nội thất mới 100 phần trăm trung tâm quận 1",
    "Căn hộ cao cấp chỉ từ 300 triệu gần trường học bệnh viện thương mại trung tâm đang mở bán ưu đãi đặt biệt",
    "Dự án đất nền sinh lời 300 phần trăm sau 2 năm pháp lý rõ ràng sổ đỏ ngay đặt cọc chỉ 50 triệu giữ chỗ ngay",

    # Email marketing rác
    "Bạn đã được chọn để nhận ưu đãi đặc biệt từ đối tác của chúng tôi bấm xem ngay trước khi hết hạn",
    "Thông báo đặc biệt chỉ dành cho bạn nhận ngay voucher 1 triệu đồng mua sắm tại hệ thống cửa hàng chúng tôi",
    "Cơ hội cuối cùng nhận ưu đãi cực khủng chỉ còn 2 giờ đăng ký ngay trước khi chương trình kết thúc",
    "Nhận quà miễn phí từ nhà tài trợ đặc biệt điền form ngay để nhận gói quà trị giá 5 triệu đồng",
    "Chương trình khuyến mãi bí mật chỉ dành cho số ít người dùng may mắn được chọn đừng bỏ lỡ nhận ngay",
    "Mở tài khoản ngân hàng số nhận ngay 500K không điều kiện chuyển khoản miễn phí mãi mãi lãi suất cao nhất",
    "Nhận 300K tiền mặt ngay bây giờ chỉ cần tải ứng dụng và đăng ký tài khoản không cần điều kiện gì thêm",
    "Đăng ký thẻ tín dụng ngay nhận ưu đãi hoàn tiền 5 phần trăm mọi giao dịch phí thường niên 0 đồng năm đầu",

    # Sản phẩm đa cấp
    "Tham gia hệ thống MLM của chúng tôi kiếm thu nhập thụ động hàng trăm triệu mỗi tháng không cần bán hàng",
    "Cơ hội kinh doanh độc quyền sản phẩm Nhật Bản phân phối độc quyền toàn quốc hoa hồng cực cao",
    "Gia nhập mạng lưới kinh doanh thông minh thu nhập không giới hạn chỉ cần giới thiệu thêm bạn bè tham gia",
    "Bán hàng online không vốn ăn hoa hồng 40 phần trăm mỗi đơn hàng sản phẩm hot nhất thị trường hiện nay",

    # Spam tình cảm / Hẹn hò
    "Tìm bạn bè kết đôi nghiêm túc phụ nữ xinh đẹp giàu có đang tìm bạn trai tốt bụng đăng ký miễn phí ngay",
    "Cô gái Nhật Bản đang tìm người bạn đời Việt Nam đăng ký app hẹn hò ngay để được ghép đôi ngay hôm nay",
    "Hàng ngàn phụ nữ độc thân xinh đẹp đang chờ bạn tham gia cộng đồng hẹn hò lớn nhất Việt Nam miễn phí",

    # Thêm spam
    "Nhận tiền thưởng 100K mỗi ngày chỉ cần xem video quảng cáo 30 giây trên điện thoại dễ dàng kiếm tiền online",
    "Bán tài khoản Netflix cả năm giá chỉ 99K share với 10 người cùng dùng 4K hàng chính hãng đảm bảo 100 phần trăm",
    "Mua sim số đẹp phong thủy hợp mệnh giá siêu rẻ giao hàng toàn quốc nhiều đầu số đẹp nhất thị trường",
    "Dịch vụ hack tài khoản game lấy lại tài khoản bị hack giá rẻ uy tín đảm bảo thành công 100 phần trăm",
    "Khóa học làm giàu bí mật từ người thành công học cách kiếm 100 triệu mỗi tháng chỉ làm online 2 giờ ngày",
    "Chứng chỉ ngoại ngữ IELTS TOEIC đảm bảo đầu ra cam kết đỗ ngay trong kỳ thi đầu tiên không đỗ hoàn tiền",
    "Dịch vụ viết luận văn thuê cam kết chất lượng cao 100 phần trăm đạt điểm A bảo mật tuyệt đối nhanh chóng",
    "Tuyển cộng tác viên đặt cược thể thao lương ngàn đô mỗi tháng làm việc từ xa không cần kinh nghiệm",
    "Mua account Facebook verified nhiều bạn bè tương tác cao giá rẻ nhất thị trường nhiều loại tài khoản",
    "SEO website lên top Google trong 24 giờ giá chỉ 500K bảo hành kết quả 6 tháng uy tín hàng đầu Việt Nam",
    "Phần mềm spam email tự động gửi hàng triệu email mỗi ngày tỷ lệ vào hộp thư chính cao giá rẻ nhất",
    "Bán data khách hàng tiềm năng toàn quốc theo ngành nghề địa phương cập nhật mới nhất giá rẻ",
    "Dịch vụ tăng follow Instagram TikTok YouTube nhanh 10000 người theo dõi chỉ trong 24 giờ bảo hành",
    "Mua vote đánh giá 5 sao trên Google Maps Shopee Lazada giá chỉ từ 5K mỗi đánh giá giao trong ngày",
    "Cho thuê tài khoản ngân hàng lương cao mỗi tháng không rủi ro an toàn tuyệt đối không cần làm gì",
    "Dịch vụ mua bán thẻ cào điện thoại chiết khấu cao nhất thị trường mua nhiều giảm giá thêm giao dịch ngay",
    "Nhận coin miễn phí từ ứng dụng ví điện tử mới ra mắt đăng ký ngay kiếm token chờ niêm yết giá tăng gấp 100",
    "Cảnh báo tài khoản zalo của bạn sẽ bị xóa sau 24 giờ nếu không xác minh bấm vào đây để giữ tài khoản",
    "Mua thẻ điện thoại Viettel Vinaphone Mobifone chiết khấu 30 đến 50 phần trăm thanh toán chuyển khoản ngay",
    "Đáo hạn thẻ tín dụng lãi suất thấp nhất dịch vụ tài chính uy tín không phí ẩn giải quyết nhanh trong ngày",
]

HAM = [
    # Tin nhắn gia đình
    "Bố ơi con về muộn một chút tối nay vì có cuộc họp quan trọng bố mẹ ăn cơm trước không cần đợi con",
    "Mẹ ơi mai con cần tiền đóng học phí xin mẹ chuyển cho con 2 triệu đồng nha mẹ con cảm ơn nhiều lắm",
    "Anh ơi em đang ở siêu thị mua gì về không nhắn tin cho em anh ơi còn thứ gì cần mua không",
    "Con gái ơi nhớ mặc áo ấm đi học hôm nay trời lạnh lắm nhớ ăn sáng đầy đủ trước khi đi học nghe con",
    "Bà nội ơi hôm nay cháu đến thăm bà được không cháu mang theo ít cam và bánh bà thích bà nhà có không",
    "Anh ơi bố bệnh phải vào viện hôm nay anh có thể về sớm không em lo lắm bố đang trong phòng cấp cứu",
    "Chị ơi hôm nay chị có về ăn cơm nhà không em nấu nhiều em đợi chị ăn cùng cho vui chị về mấy giờ",
    "Con ơi nhớ uống thuốc sau bữa ăn nghen con bác sĩ dặn phải uống đủ liều mới mau hết bệnh được con",
    "Bố về muộn tối nay con tự nấu cơm ăn nhé đồ ăn trong tủ lạnh con tự lấy ra nấu bố về sau sẽ tính nhé",
    "Anh trai ơi em nhớ anh lắm bao giờ anh về thăm nhà em học tập bình thường anh đừng lo cho em nhé",
    "Mẹ ơi con đã đến nơi rồi an toàn mẹ yên tâm nhé con sẽ gọi điện cho mẹ sau khi ổn định chỗ ở mẹ nhé",
    "Cả nhà ơi cuối tuần này mình đi picnic không trời đẹp lắm con bé rất thích đi chơi mình đi cùng nhau nhé",
    "Chú ơi cháu hỏi thăm sức khỏe chú thím dạo này chú thím có khỏe không gia đình cháu đều khỏe cả chú ơi",

    # Tin nhắn công việc
    "Xin chào chị ơi ngày mai cuộc họp với khách hàng dời sang 10 giờ sáng chị nhớ chuẩn bị báo cáo nhé",
    "Anh ơi file báo cáo quý 3 anh đã hoàn thành chưa sếp cần trước 5 giờ chiều hôm nay anh gửi email cho sếp nhé",
    "Chị ơi hôm nay em nghỉ phép vì con ốm phải đưa đi bệnh viện em đã báo với sếp rồi chị thông cảm nhé",
    "Xin chào anh chị đồng nghiệp nhắc nhở mọi người họp team thứ 2 lúc 9 giờ sáng phòng họp tầng 3 nhé",
    "Em ơi em có thể gửi lại file excel cho anh không anh lỡ xóa mất file quan trọng cần gấp để báo cáo",
    "Chào anh anh có thể xem lại hợp đồng và ký tên giúp em không em cần gấp để gửi cho đối tác chiều nay",
    "Xin chào sếp em xin phép nghỉ buổi chiều hôm nay vì có việc gia đình quan trọng em đã hoàn thành công việc rồi",
    "Anh ơi deadline dự án là thứ 6 tuần này đội mình cần họp thêm một lần nữa để review trước khi nộp",
    "Chị ơi khách hàng hỏi về tiến độ dự án chị có thể cập nhật tình hình cho em để em trả lời khách không",
    "Xin chào anh chị công ty thông báo thứ 6 tuần này được nghỉ bù làm việc trực tiếp với văn phòng sẽ thông báo sau",
    "Em ơi anh cần thêm thông tin về ngân sách dự án Q4 anh cần biết con số chính xác để trình lên ban giám đốc",
    "Chào cả team ngày mai mình có buổi training kỹ năng mềm từ 8 giờ đến 12 giờ trưa tại hội trường lớn",

    # Tin nhắn học tập
    "Bạn ơi mai thi môn Toán bạn ôn bài chưa mình ôn cùng nhau được không hay bạn muốn tự ôn thì thôi",
    "Thầy ơi em nộp bài tập trễ được không em bị ốm mấy ngày không làm được bài em xin lỗi thầy",
    "Bạn bè ơi ai có tài liệu ôn thi cuối kỳ môn Vật lý không cho mình mượn với mình tìm mãi không có",
    "Mình vừa đọc xong chương 5 sách giáo khoa khó quá không hiểu phần nào bạn có thể giải thích cho mình không",
    "Cô ơi tiết học ngày mai học tại phòng nào ạ em bị nhầm phòng tuần trước xin cô thông báo trước ạ",
    "Nhóm học tập ơi hôm nay mình họp nhóm thuyết trình lúc mấy giờ mình quên mất rồi ai nhớ nhắc mình với",
    "Bạn ơi cho mình hỏi bài tập về nhà môn Hóa hôm nay làm trang mấy trong sách vở mình không chép kịp",
    "Thư viện trường thông báo sẽ đóng cửa sớm lúc 6 giờ chiều hôm nay do bảo trì hệ thống điện xin thông báo",
    "Mình đã đăng ký học thêm tiếng Anh thứ 3 thứ 5 mỗi tuần bạn có muốn học cùng mình không thầy dạy rất tốt",
    "Bạn ơi tuần này có kiểm tra giữa kỳ môn Văn không bạn nhớ ôn bài từ chương 1 đến chương 6 nghe",

    # Thông báo dịch vụ chính thống
    "Thông báo từ Viettel gói cước Data 4G của bạn sắp hết vui lòng đăng ký gia hạn để tiếp tục sử dụng",
    "Thông báo hóa đơn điện tháng 6 của hộ gia đình bạn là 450000 đồng vui lòng thanh toán trước ngày 15",
    "Nhắc nhở từ Bảo hiểm xã hội phí bảo hiểm quý 3 cần đóng trước ngày 30 tháng 9 vui lòng không trễ hạn",
    "Ngân hàng Vietcombank thông báo giao dịch thành công số tiền 500000 đồng lúc 10 giờ 30 phút ngày hôm nay",
    "Thông báo từ bệnh viện Đại học Y Dược lịch khám định kỳ của bạn vào lúc 9 giờ sáng ngày 20 tháng 7",
    "Grab thông báo tài xế của bạn đang trên đường đến nơi đón ước tính 5 phút nữa tài xế sẽ đến nơi bạn đang đứng",
    "Shopee thông báo đơn hàng của bạn đã được giao thành công vui lòng xác nhận nhận hàng trên ứng dụng",
    "EVN thông báo khu vực của bạn sẽ cúp điện từ 8 giờ đến 17 giờ ngày mai để bảo trì đường dây điện",
    "Momo thông báo bạn vừa nhận được 200000 đồng từ bạn bè số dư ví điện tử của bạn hiện tại là 500000 đồng",
    "Vietcredit thông báo kỳ hạn thanh toán thẻ tín dụng của bạn vào ngày 25 tháng này số tiền tối thiểu 500000 đồng",

    # Trò chuyện thông thường
    "Ơi bạn ơi lâu quá không gặp bạn khỏe không dạo này bạn làm gì ở đâu cuối tuần này mình cà phê không",
    "Hôm nay trời đẹp quá bạn ơi mình đi dạo công viên không mình gọi thêm mấy đứa bạn cũng đi cùng cho vui",
    "Bạn đã xem phim đó chưa tuyệt vời lắm mình xem xong mà còn muốn xem lại bạn nên đi xem với mình tuần sau",
    "Mình vừa nấu xong món canh chua bạn thích không mình nấu nhiều sang ăn cùng cho vui hai người một mình buồn",
    "Ơi bạn ơi nhớ bạn quá lâu rồi không gặp bạn có khỏe không gia đình bạn mọi người vẫn bình thường chứ",
    "Hôm nay công ty cho nghỉ sớm mình thích quá bạn có rảnh không cùng ra ngoài ăn uống một chút cho vui",
    "Bạn thấy kết quả bóng đá tối qua không Việt Nam thắng to quá mình xem mà phấn khích lắm vui quá bạn ơi",
    "Mình vừa mua được áo mới đẹp lắm bạn ơi bạn có muốn đi mua sắm cùng mình cuối tuần này không mình chỉ cho",
    "Bạn ơi bạn có công thức nấu bánh kem không mình muốn tự làm bánh sinh nhật cho mẹ nhưng chưa biết cách",
    "Chiều nay nhóm mình đá bóng bạn đi không thiếu người lắm mình chờ bạn đến sân Thống Nhất lúc 5 giờ nhé",
    "Mình đang đọc cuốn sách này hay lắm bạn ơi bạn đọc sách nhiều không mình cho bạn mượn đọc sau khi mình xong",
    "Bạn có rảnh tối nay không cùng xem phim trên Netflix mình mới đăng ký gói mới nhiều phim hay lắm bạn ơi",

    # Hỏi thăm sức khỏe
    "Anh ơi nghe nói anh bệnh dạo này anh đã đỡ chưa có cần gì không em đưa đi bệnh viện khám hay mang thuốc tới",
    "Bạn ơi sao hôm nay trông bạn mệt vậy bạn có ổn không bạn cần nghỉ ngơi không hay bạn muốn mình đưa đi khám",
    "Cô ơi nghe tin cô không khỏe chúng con lo lắng lắm cô có cần chúng con mang gì tới không cô nhớ giữ sức khỏe",
    "Em ơi em cảm thấy thế nào rồi có đỡ không uống thuốc chưa nếu không khỏi thì sáng mai mình đi khám nhé",
    "Ông bà ơi dạo này sức khỏe ông bà thế nào tháng này cháu về thăm ông bà ông bà nhớ giữ sức khỏe nghe ông bà",

    # Lịch hẹn
    "Bác sĩ ơi em xin đặt lịch khám vào sáng thứ 4 tuần sau được không em muốn khám sức khỏe tổng quát",
    "Anh ơi lịch hẹn ngày mai lúc 2 giờ chiều tại văn phòng anh nhớ đừng quên nhé mình cần bàn hợp đồng quan trọng",
    "Bạn ơi mình đặt bàn nhà hàng rồi 7 giờ tối thứ 6 tại nhà hàng Quê Hương bạn đến đúng giờ nghe bạn ơi",
    "Thẩm mỹ viện thông báo lịch hẹn chăm sóc da của bạn vào lúc 10 giờ sáng ngày 15 tháng này vui lòng đến đúng giờ",
    "Nhóm ơi cuối tuần này mình tổ chức họp lớp tại quán cà phê góc phố lúc 3 giờ chiều mọi người cùng đến nhé",

    # Tin tức
    "Thời tiết hôm nay ở Hà Nội dự báo có mưa lớn vào buổi chiều người dân nên chuẩn bị áo mưa khi ra ngoài",
    "Đội tuyển bóng đá Việt Nam vừa giành chiến thắng 2 đến 0 trước Thái Lan trong trận đấu bán kết hôm qua",
    "Giá xăng dầu hôm nay được điều chỉnh giảm 500 đồng mỗi lít áp dụng từ 15 giờ chiều ngày hôm nay",
    "Trường đại học Bách Khoa thông báo tuyển sinh năm học mới điểm chuẩn dự kiến sẽ được công bố vào tháng 8",
    "Lễ hội âm nhạc mùa hè sẽ được tổ chức tại Công viên Thống Nhất từ ngày 15 đến 20 tháng 7 miễn phí vào cửa",
    "Bộ Giáo dục thông báo học sinh sẽ được nghỉ hè từ ngày 25 tháng 5 và khai giảng năm học mới vào 5 tháng 9",
    "UBND thành phố thông báo từ ngày 1 tháng 8 sẽ triển khai làn đường riêng cho xe đạp tại một số tuyến phố chính",
    "Bệnh viện Chợ Rẫy thông báo từ tháng 8 sẽ mở thêm khoa Nội tiết với nhiều thiết bị y tế hiện đại mới nhất",

    # Thông báo từ dịch vụ thật
    "Kính gửi khách hàng hóa đơn điện nước tháng 7 của quý khách là 320000 đồng hạn nộp ngày 20 tháng 7",
    "Cảm ơn bạn đã mua hàng tại Vinmart đơn hàng của bạn đã được xác nhận và sẽ giao trong 2 đến 3 ngày làm việc",
    "BIDV thông báo số dư tài khoản của bạn sau giao dịch là 15000000 đồng giao dịch thực hiện lúc 9 giờ 15 phút",
    "Thông báo từ Vietnam Airlines vé máy bay của bạn chuyến HAN-SGN ngày 20 tháng 7 đã được xác nhận thành công",
    "Bưu điện thông báo bưu phẩm của bạn đã đến bưu cục địa phương vui lòng đến nhận trong vòng 7 ngày",

    # Nhắn tin sinh hoạt bình thường
    "Hàng xóm ơi nhờ anh chị tắt nhạc giúp tôi với muộn rồi con tôi đang ngủ cảm ơn anh chị nhiều lắm",
    "Bạn ơi chìa khóa của mình để quên ở chỗ bạn hôm qua không mình tìm mãi không thấy bạn xem giúp mình với",
    "Thợ ơi anh đến sửa điều hòa giúp tôi được không nóng quá không chịu được nữa anh đến được không chiều này",
    "Bạn ơi cuốn sách mình mượn bạn từ tuần trước bạn cần lấy lại không mình đọc gần xong rồi sẽ trả bạn sớm",
    "Anh tài xế ơi anh đang ở đâu rồi em đặt xe 15 phút rồi mà chưa thấy anh đến anh có đến không",
    "Em ơi em có thể qua giúp chị một việc không chị đang cần người phụ giúp dọn nhà cuối tuần này được không",
    "Bạn ơi mình để quên ví ở chỗ bạn hôm qua không trong ví có tiền và các giấy tờ quan trọng rất cần lấy lại",
    "Cô ơi em xin phép cô cho em về sớm hôm nay 30 phút được không em có việc gia đình quan trọng cần giải quyết",
    "Mọi người ơi ai biết tiệm sửa xe đạp gần khu vực quận 3 không mình bị hỏng xích giữa đường không biết đi đâu sửa",
    "Bạn ơi tối nay bạn có đi ăn tối với bọn mình không mình đặt chỗ rồi còn thiếu một người nữa là đủ nhóm",
    "Anh ơi anh có thể cho em mượn máy tính không máy em đang hỏng phải nộp bài chiều nay mà chưa xong",
    "Chị ơi chị có thể chỉ mình đường đến bệnh viện Nhi Đồng không mình chưa biết đường qua đó bao giờ",
    "Bạn ơi hôm nay cửa hàng mình đóng cửa sớm lúc 5 giờ chiều nếu bạn cần mua gì thì qua trước 5 giờ nhé",
    "Thầy ơi em gửi bài tập cuối kỳ qua email rồi thầy xem giúp em với em nộp trước deadline 2 ngày đó thầy",
    "Bạn ơi nhớ mang theo ô hôm nay trời sắp mưa rồi bạn đi bộ từ nhà ra xe buýt dễ bị ướt lắm đó bạn",
    "Nhóm ơi thứ 7 này ai rảnh không mình tổ chức nướng BBQ tại nhà mình mọi người cùng góp đồ ăn cho vui",
    "Bạn ơi mình vừa đọc được bài báo hay về sức khỏe mình gửi link cho bạn đọc thử nhé bổ ích lắm",
    "Anh ơi em gặp khó khăn trong bài toán này anh có thể giải thích cách làm cho em hiểu không em cảm ơn anh",
    "Chị ơi đơn hàng chị đặt tuần trước đã về rồi chị sang lấy được rồi nhớ mang theo phiếu đặt hàng nghe chị",
    "Cậu ơi tớ đang nấu cháo gà cậu muốn ăn không tớ nấu nhiều ăn cho khỏe người vừa ốm dậy cần bồi dưỡng",
]

# Xáo trộn và tạo dataset
all_data = [('spam', msg) for msg in SPAM] + [('ham', msg) for msg in HAM]
random.shuffle(all_data)

output_path = r'D:\UTH\HK2N3\TTNT\project_spam_email\demo1\spam_email\spam_detector_ai\data\spam_vi.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['label', 'text'])
    for label, text in all_data:
        writer.writerow([label, text])

print(f"Đã tạo dataset: {output_path}")
print(f"Tổng số mẫu: {len(all_data)}")
print(f"Spam: {sum(1 for l, _ in all_data if l == 'spam')}")
print(f"Ham: {sum(1 for l, _ in all_data if l == 'ham')}")
