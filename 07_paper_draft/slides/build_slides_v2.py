"""Build the group's slide deck following the chapter structure of the mentor's sample (present.html):
00 Mở đầu → 01 Khám phá dữ liệu → 02 Tiền xử lý & đặc trưng → 03 Distribution shift → 04 Mô hình & đánh giá →
05 Insight & kết luận, with a "NGUỒN" line on every slide and speaker notes (press N).

Every number is taken from the result files named on the slide (code/outputs, 06_experiment_results) or from the
paper (08_final_submission/ICIIT2027_Paper_rev7). Figures are embedded, so the output is one self-contained file.

Usage:
    python 07_paper_draft/slides/build_slides_v2.py
Writes 07_paper_draft/slides/Tu_du_bao_den_quyet_dinh_v2.html
"""
import base64
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Tu_du_bao_den_quyet_dinh_v2.html")
TOPIC = "Từ dự báo<br>đến quyết định"
TEAM = "Bùi Anh Duy · Khổng Trần Gia Huy"
MENTOR = "Nguyễn Thị Cẩm Hương · Trương Long"
TAG = "M5 · VN1 · Dự báo → Tồn kho"


def img(rel, width=None, style=""):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        b = base64.b64encode(fh.read()).decode()
    w = f"width:{width}px;" if width else ""
    return (f'<figure class="fig" style="{w}{style}"><img src="data:image/png;base64,{b}" '
            f'alt="{os.path.basename(rel)}"></figure>')


def table(head, rows, cls="spec small", num=(), hl=()):
    h = "".join(f'<th class="n">{c}</th>' if i in num else f"<th>{c}</th>" for i, c in enumerate(head))
    body = ""
    for k, r in enumerate(rows):
        tds = "".join(f'<td class="n">{c}</td>' if i in num else f"<td>{c}</td>" for i, c in enumerate(r))
        body += f'<tr class="hl">{tds}</tr>' if k in hl else f"<tr>{tds}</tr>"
    return f'<table class="{cls}"><tr>{h}</tr>{body}</table>'



def table7_rows():
    import pandas as pd
    r = pd.read_csv(os.path.join(ROOT, "code", "outputs", "robustness", "rolling_calibration.csv"))
    r = r[(r.eta == 0.5) & (r.target == 0.92)]
    cols = [("M5", "third → second"), ("M5", "second → main"), ("VN1", "third → second"), ("VN1", "second → main"),
            ("VNF", "main (τ0 = target)")]
    sg = lambda v: f"{100 * v:+.1f}".replace(".", ",").replace("-", "−")
    out = []
    for m in ["LGB-Q", "HGB-Q", "TSB-NB", "C2", "E7-med"]:
        row = [m]
        for ds, tr in cols:
            x = r[(r.dataset == ds) & (r.transition == tr) & (r.method == m)].iloc[0]
            cell = f"{x.fill:.3f}".replace(".", ",") + " · "
            cell += (f"{x.inv:.2f} tuần".replace(".", ",") if m == "LGB-Q"
                     else f"{sg(x.d_inv)}% [{sg(x.lo)}; {sg(x.hi)}]")
            row.append(cell)
        out.append(row)
    return out

SLIDES = []


def slide(sec, title, body, src, notes, cover=False):
    SLIDES.append(dict(sec=sec, title=title, body=body, src=src, notes=notes, cover=cover))


CH = {"00": "Mở đầu", "01": "Khám phá dữ liệu", "02": "Tiền xử lý & đặc trưng", "03": "Distribution shift",
      "04": "Mô hình & đánh giá", "05": "Insight & kết luận"}

# ============================================================================================ 00 Mở đầu
slide("00", None, f"""
<div class="cover">
  <h1>Dự báo chính xác nhất có phải là <em>giữ ít hàng nhất</em>?</h1>
  <p class="q">So sánh các phương pháp dự báo nhu cầu xác suất bằng lượng tồn kho chúng cần để phục vụ cùng một mức
  fill rate, trên hai bối cảnh bán lẻ (M5, VN1) và ba giai đoạn kiểm thử.</p>
  <div class="who">
    <div><div class="k">Nhóm thực hiện · RetailQ</div>Bùi Anh Duy<br>Khổng Trần Gia Huy</div>
    <div><div class="k">Giảng viên hướng dẫn</div>Nguyễn Thị Cẩm Hương<br>Trương Long</div>
    <div><div class="k">Đề tài</div>NCKH FA26 · ICIIT 2027<br>FPT University HCMC</div>
  </div>
</div>""", "NGUỒN · 08_final_submission/ICIIT2027_Paper_rev7 · github.com/anhduyBA/forecast-to-decision-benchmark",
      ["Chào thầy cô và các bạn. Nhóm RetailQ trình bày đề tài so sánh các phương pháp dự báo nhu cầu theo lượng tồn kho chúng cần, chứ không chỉ theo sai số.",
       "Hai bộ dữ liệu công khai: M5 của Walmart (cửa hàng truyền thống) và VN1 (thương mại điện tử nhiều nhà bán), mỗi bộ ba cửa sổ kiểm thử 26 tuần."],
      cover=True)

slide("00", "Bối cảnh: mỗi tuần, mỗi sản phẩm, chọn một trong ba việc", """
<div class="grid2" style="grid-template-columns:1fr 1fr 1fr;gap:40px">
  <div class="box"><span class="tag">01 · ĐẶT HÀNG</span><h3>Tồn &lt; S</h3>
    <p>S = phân vị τ của tổng nhu cầu 3 tuần tới (lead time 2 tuần + chu kỳ 1 tuần). Đặt bù lên S.</p></div>
  <div class="box"><span class="tag">02 · GIỮ</span><h3>Không hành động</h3>
    <p>Tồn nằm giữa S và ngưỡng thanh lý. Khách không mua được hàng thì mất luôn (lost sales).</p></div>
  <div class="box b"><span class="tag">03 · THANH LÝ</span><h3>Tồn dư quá nhiều</h3>
    <p>Tồn vượt phân vị 0,95 của nhu cầu 13 tuần tới → bán ra kênh thứ cấp với tỷ lệ thu hồi r.</p></div>
</div>
<div class="box why" style="margin-top:46px"><p><b>Vấn đề.</b> Các cuộc thi dự báo (M5, VN1) xếp hạng phương pháp theo <b>sai số</b>.
Nhưng cửa hàng dùng dự báo để <b>quyết định lượng hàng</b>: đặt ít thì mất khách, đặt nhiều thì tốn vốn và chỗ chứa.
Dự báo có sai số nhỏ hơn chưa chắc cần ít hàng hơn để phục vụ cùng một tỷ lệ nhu cầu.</p></div>
""", "NGUỒN · bài báo mục 1 và 3.3 · code/f2d/policy.py",
      ["Một tuần của người lập kế hoạch: với từng sản phẩm ở từng điểm bán, chọn đặt, giữ hay thanh lý.",
       "Mức đặt S là phân vị của tổng nhu cầu 3 tuần, vì hàng mất 2 tuần mới về và mỗi tuần xem lại một lần.",
       "Câu hỏi của đề tài: phương pháp có sai số thấp nhất có cũng là phương pháp cần ít hàng nhất không."])

slide("00", "Bốn câu hỏi nghiên cứu", """
<ol class="steps" style="max-width:1500px">
  <li><b>RQ1 · Độ chính xác và tồn kho</b>Trên M5 và VN1, bảy phương pháp xếp hạng thế nào về sai số và về tồn kho cần
  thiết ở cùng fill rate thực tế? Hai bảng xếp hạng có trùng nhau không?</li>
  <li><b>RQ2 · Chọn phương pháp theo nhóm nhu cầu</b>Có thể chọn trước phương pháp theo loại nhu cầu (ADI–CV², phân
  cụm) hay theo cửa sổ trước không?</li>
  <li><b>RQ3 · Thanh lý</b>Quy tắc thanh lý giảm được bao nhiêu tồn dư, và tỷ lệ thu hồi phải tối thiểu bao nhiêu (s*)
  thì thanh lý mới có lợi?</li>
  <li><b>RQ4 · Độ vững</b>Kết luận có giữ khi đổi lead time, siêu tham số, giai đoạn, và khi doanh số bị kiểm duyệt
  do hết hàng không?</li>
</ol>""", "NGUỒN · bài báo mục 1",
      ["RQ1 là câu chính. RQ2 hỏi có chọn trước được không. RQ3 về thanh lý. RQ4 về độ vững, trong đó có câu hỏi của reviewer về hết hàng."])

# ============================================================================================ 01 Khám phá dữ liệu
slide("01", "1.1 Tải dữ liệu và kiểm tra cấu trúc", table(
    ["Tiêu chí", "M5 (Walmart)", "VN1", "Xử lý"],
    [["Chuỗi × tuần", "30.490 × 277", "15.053 × 196", "Mọi KPI là tỷ lệ, kiểm định riêng từng bộ"],
     ["Giai đoạn", "29/01/2011 → 14/05/2016", "06/07/2020 → 01/04/2024", "Mỗi bộ có ba cửa sổ kiểm thử riêng"],
     ["Đơn vị nhu cầu", "sản phẩm × cửa hàng", "khách hàng × kho × sản phẩm", "Khác do bản chất, nêu trong bài"],
     ["Giá trị thiếu sau ngày bắt đầu", "0", "0", "—"],
     ["Doanh số âm", "0", "0", "—"],
     ["Ô giá quan sát được", "100%", "44,6%", "VN1 chỉ có giá ở tuần có bán → mang giá trước sang"],
     ["Số đặc trưng mô hình", "27", "21", "21 đặc trưng chung; M5 thêm sự kiện, SNAP, cấp bậc"],
     ["Chuỗi được đánh giá (chính / 2 / 3)", "30.381 / 29.917 / 28.824", "13.844 / 11.442 / 9.383", "≥ 13 tuần lịch sử, ≥ 1 lần bán"]],
    num=()), "NGUỒN · code/sync_check.py → code/outputs/sync_check.md · bài báo Bảng 1",
      ["Kiểm tra đồng bộ hai bộ: cùng tuần 7 ngày, không thiếu, không âm.",
       "Khác biệt lớn nhất là giá: VN1 chỉ có giá ở tuần có bán, nên nhóm mang giá gần nhất sang và đã thử bỏ biến giá.",
       "Nhóm giữ mọi chuỗi có đủ 13 tuần lịch sử, không bỏ chuỗi ngắn hay chuỗi thưa."])

slide("01", "1.2 Nhu cầu thưa và lệch → chọn thước đo phù hợp", """
<div class="row" style="gap:60px">
 <div style="flex:1">
  <div class="row" style="gap:70px;margin-bottom:36px">
   <div><div class="k">Tuần không bán · M5</div><div class="mid">24,4%</div></div>
   <div><div class="k">Tuần không bán · VN1</div><div class="mid b">49,1%</div></div>
  </div>
  <ol class="obs">
   <li><b>Sai số có chuẩn hoá (scaled QL) không ổn định trên VN1:</b> trung bình 0,336 / 0,539 / <b>2,008</b> qua ba cửa sổ,
   do vài chuỗi có mẫu số (sai số naïve) gần 0.</li>
   <li><b>Thay bằng wQL</b> = tổng pinball loss / tổng nhu cầu (0,103 / 0,078 / 0,102), kèm trung vị và hạng trung bình theo chuỗi.</li>
   <li><b>Thước đo quyết định:</b> tồn kho (tuần nhu cầu) cần để đạt cùng <b>fill rate thực tế</b> 0,90–0,98.</li>
  </ol>
 </div>
 <div style="width:560px">
  <div class="box"><span class="tag">VÌ SAO KHÔNG SO Ở CÙNG τ</span>
   <p>Cùng τ = 0,9 nhưng mỗi phương pháp đạt fill rate thực tế khác nhau: phương pháp nào phình phân vị trông như phục vụ
   tốt hơn. Nhóm đổi τ trên lưới {0,5; 0,8; 0,9; 0,95; 0,99} rồi nội suy theo đường đánh đổi.</p></div>
 </div>
</div>""", "NGUỒN · bài báo mục 3.4 và 5.1 · code/outputs/sync_check.md",
      ["Giống bài mẫu: đặc điểm của biến mục tiêu quyết định thước đo.",
       "Gần một nửa số tuần ở VN1 không bán được. Sai số chuẩn hoá trung bình bị vài chuỗi kéo lên 2,0, nên nhóm dùng wQL.",
       "Quan trọng hơn, thước đo chính là tồn kho ở cùng fill rate thực tế, không phải ở cùng τ."])

slide("01", "1.3 Tổng doanh số theo tuần và ba cửa sổ kiểm thử",
      img("code/outputs/eda/eda_1_sales_over_time.png", 1040, "margin:0 auto"),
      "NGUỒN · code/eda_figures.py → code/outputs/eda/eda_1_sales_over_time.png (thành viên A)",
      ["M5 tăng đều, có mùa vụ; VN1 tăng mạnh và có nhiều đỉnh đột biến.",
       "Vùng tô là ba cửa sổ 26 tuần. Mọi thí nghiệm lặp lại trên cả ba, vì kết luận chỉ đúng ở một giai đoạn thì không đáng tin."])

slide("01", "1.3 So sánh phân phối đặc trưng chuỗi: VN1 thưa hơn, ngắn hơn", f"""
<div class="row" style="gap:44px">
 {img("code/outputs/eda/eda_3_feature_distributions.png", 1080)}
 <div style="flex:1">{table(["Trung vị", "M5", "VN1", "KS"],
    [["Mức bán / tuần", "4,18", "1,44", "0,34"], ["Tỷ lệ tuần = 0", "0,198", "0,542", "0,40"],
     ["ADI", "1,25", "2,18", "0,40"], ["CV²", "0,315", "0,342", "0,23"], ["Độ dài lịch sử", "230", "103", "0,68"],
     ["Xu hướng 26 tuần", "0,113", "0", "0,15"]], num=(1, 2, 3))}
 <p class="cap" style="margin-top:22px;font-size:20px">Nhóm đều (smooth): <b>53,0%</b> ở M5, <b>18,8%</b> ở VN1.</p></div>
</div>""", "NGUỒN · code/outputs/eda/eda_3_feature_distributions.png · eda_summary.md · sync_check.md",
      ["Sáu đặc trưng chuỗi, tính trên lịch sử trước cửa sổ chính.",
       "VN1 có trung vị 54% tuần không bán so với 20% ở M5, lịch sử ngắn bằng nửa. KS cao nhất là độ dài lịch sử (0,68)."])

slide("01", "1.4 Ma trận tương quan các đặc trưng chuỗi", f"""
<div class="row" style="gap:44px">
 {img("code/outputs/eda/eda_6_correlation.png", 1120)}
 <ol class="obs" style="padding-top:10px">
  <li>Mức bán và tỷ lệ tuần = 0 tương quan âm mạnh: <b>−0,72</b> (M5), <b>−0,91</b> (VN1).</li>
  <li>CV² đổi dấu: <b>−0,24</b> với mức bán ở M5 nhưng <b>+0,55</b> ở VN1 — chuỗi bán nhiều ở VN1 lại dao động mạnh.</li>
  <li>Xu hướng gần như không tương quan với các đặc trưng còn lại (|ρ| ≤ 0,31): khó đoán trước chuỗi nào sẽ tăng.</li>
 </ol>
</div>""", "NGUỒN · code/eda_figures.py → code/outputs/eda/eda_6_correlation.png (tương quan Spearman, trước cửa sổ chính)",
      ["Tương quan Spearman giữa sáu đặc trưng chuỗi.",
       "Điểm đáng chú ý thứ ba: xu hướng gần như độc lập với các đặc trưng khác. Điều này báo trước kết quả ở phần 4: không chọn trước được phương pháp theo nhóm."])

# ============================================================================================ 02 Tiền xử lý & đặc trưng
slide("02", "2.1 Biến mục tiêu và đặc trưng cho mô hình toàn cục", """
<div class="row" style="gap:50px">
 <div style="width:720px">
  <div class="box b"><span class="tag">MỤC TIÊU</span>
   <p class="formula">D<sub>h</sub>(o) = Σ<sub>k=0..h−1</sub> Y[o+k]</p>
   <p>Tổng nhu cầu h tuần, h = 3 (đặt hàng) và h = 13 (thanh lý). Dự báo trực tiếp phân vị của tổng, vì phân vị của tổng
   khác tổng các phân vị.</p></div>
  <div class="box" style="margin-top:34px"><span class="tag">CHUẨN HOÁ QUY MÔ</span>
   <p class="formula">s = TB tuần có bán (52 tuần) ≥ 0,1</p>
   <p>Đặc trưng mức và mục tiêu chia cho s, nên một mô hình chung học được cả chuỗi lớn và nhỏ; dự báo nhân lại s
   (pinball loss bất biến theo tỷ lệ).</p></div>
 </div>
 <div style="flex:1">""" + table(["Nhóm", "Đặc trưng", "M5", "VN1"],
    [["Trễ", "lag 1, 2, 3, 4, 8, 13, 26, 52", "8", "8"],
     ["Cửa sổ trượt", "mean và std 4, 13, 26 tuần", "6", "6"],
     ["Gián đoạn", "tỷ lệ tuần = 0 (13 tuần), số tuần từ lần bán cuối", "2", "2"],
     ["Lịch", "tuần trong năm, tháng", "2", "2"],
     ["Giá", "giá, thay đổi giá 4 tuần", "2", "2"],
     ["Sự kiện", "số sự kiện, ngày SNAP trong h tuần", "2", "—"],
     ["Cấp bậc", "dept, cat, store, state", "4", "—"],
     ["Quy mô", "s", "1", "1"],
     ["Tổng", "", "27", "21"]], num=(2, 3), hl=(8,)) + """
 </div>
</div>""", "NGUỒN · code/f2d/features.py · code/outputs/sync_check.md · bài báo mục 3.2",
      ["Mục tiêu là tổng nhu cầu h tuần tính từ tuần ra quyết định o.",
       "Các đặc trưng mức được chia cho quy mô s để một mô hình LightGBM dùng chung cho hơn 30 nghìn chuỗi.",
       "M5 có 27 đặc trưng, VN1 có 21; 21 đặc trưng là chung. Nhóm đã thử chỉ dùng đặc trưng chung trên M5."])

TIMELINE = """
<svg class="chart" viewBox="0 0 1780 330" width="1780" height="330" xmlns="http://www.w3.org/2000/svg">
 <rect x="20" y="60" width="980" height="70" fill="none" stroke="#1A1A1A" stroke-width="2"/>
 <text x="510" y="104" class="t-mono t-val" text-anchor="middle" fill="#1A1A1A">LỊCH SỬ · chỉ dữ liệu này được dùng để huấn luyện</text>
 <rect x="1000" y="60" width="380" height="70" fill="#E8590C" fill-opacity="0.12" stroke="#E8590C" stroke-width="2"/>
 <text x="1190" y="104" class="t-mono t-val" text-anchor="middle" fill="#E8590C">KHỐI 1 · 13 tuần</text>
 <rect x="1380" y="60" width="380" height="70" fill="#E8590C" fill-opacity="0.22" stroke="#E8590C" stroke-width="2"/>
 <text x="1570" y="104" class="t-mono t-val" text-anchor="middle" fill="#E8590C">KHỐI 2 · 13 tuần</text>
 <line x1="1000" y1="30" x2="1000" y2="170" stroke="#1A1A1A" stroke-width="2.5"/>
 <line x1="1380" y1="30" x2="1380" y2="170" stroke="#1A1A1A" stroke-width="2.5"/>
 <text x="1000" y="22" class="t-mono t-dim" text-anchor="middle">refit 1</text>
 <text x="1380" y="22" class="t-mono t-dim" text-anchor="middle">refit 2 (thêm 13 tuần mới)</text>
 <rect x="790" y="60" width="210" height="70" fill="#1A1A1A" fill-opacity="0.08" stroke="none"/>
 <text x="895" y="160" class="t-mono t-dim" text-anchor="middle">13 tuần validation</text>
 <line x1="1150" y1="190" x2="1150" y2="130" stroke="#1A1A1A" stroke-width="1.5" stroke-dasharray="6 4"/>
 <text x="1150" y="215" class="t-mono t-dim" text-anchor="middle">tuần o: dự báo D_h(o) chỉ dùng tuần &lt; o</text>
 <line x1="20" y1="270" x2="1760" y2="270" stroke="#5B5B57" stroke-width="1.2"/>
 <text x="20" y="305" class="t-mono t-dim">ngày bắt đầu chuỗi ≤ đầu kiểm thử − 13 tuần</text>
 <text x="1760" y="305" class="t-mono t-dim" text-anchor="end">26 tuần kiểm thử (4 tuần khởi động + 22 tuần đánh giá)</text>
</svg>"""

slide("02", "2.2 Chống rò rỉ dữ liệu: mọi thứ chỉ học trên quá khứ", TIMELINE + """
<div class="grid2" style="grid-template-columns:1fr 1fr 1fr;gap:36px;margin-top:30px">
 <div class="box"><span class="tag">ĐẶC TRƯNG</span><p>Tại tuần o chỉ dùng tuần &lt; o. Phân loại ADI–CV² và quy mô s tính trên lịch sử.</p></div>
 <div class="box"><span class="tag">MÔ HÌNH</span><p>Huấn luyện lại ở đầu mỗi khối 13 tuần; dự báo và quyết định chạy hằng tuần.</p></div>
 <div class="box"><span class="tag">CHỌN NHÓM</span><p>Quy tắc chọn phương pháp và phân cụm học trên cửa sổ sớm hơn, thử trên cửa sổ sau.</p></div>
</div>""", "NGUỒN · code/f2d/models.py · code/f2d/config.py · bài báo mục 4",
      ["Tương đương bước fit trên train, transform trên test của bài mẫu, nhưng theo thời gian.",
       "Tại mỗi tuần o, dự báo chỉ dùng dữ liệu trước o. Mô hình được huấn luyện lại hai lần trong mỗi cửa sổ.",
       "Các quy tắc chọn phương pháp theo nhóm được học trên cửa sổ trước và kiểm tra trên cửa sổ sau."])

# ============================================================================================ 03 Distribution shift
slide("03", "3.1 Định lượng khác biệt M5 ↔ VN1 bằng KS và PSI", """
<div class="row" style="gap:50px">""" + table(
    ["Đặc trưng", "Trung vị M5", "Trung vị VN1", "KS", "PSI", "Mức"],
    [["độ dài lịch sử", "230", "103", "0,679", "5,48", '<span class="b">Mạnh</span>'],
     ["tỷ trọng tuần lớn nhất", "0,022", "0,100", "0,615", "2,84", '<span class="b">Mạnh</span>'],
     ["hệ số biến thiên giá", "0,023", "0,082", "0,446", "1,39", '<span class="b">Mạnh</span>'],
     ["tỷ lệ tuần = 0", "0,198", "0,542", "0,401", "1,44", '<span class="b">Mạnh</span>'],
     ["ADI", "1,25", "2,18", "0,401", "1,44", '<span class="b">Mạnh</span>'],
     ["log mức bán", "1,65", "0,89", "0,343", "1,31", '<span class="b">Mạnh</span>'],
     ["CV²", "0,315", "0,342", "0,229", "1,09", '<span class="b">Mạnh</span>'],
     ["xu hướng 26 tuần", "0,066", "−0,038", "0,216", "0,33", '<span class="b">Mạnh</span>'],
     ["tự tương quan 52 tuần", "0,035", "0,057", "0,107", "0,16", "Nhẹ / vừa"]], num=(1, 2, 3, 4)) + """
 <div style="width:420px">
  <div class="box"><span class="tag">NGƯỠNG PSI</span>
   <p><b style="color:var(--ink)">&lt; 0,10</b> · ổn định</p><p><b style="color:var(--ink)">0,10 – 0,25</b> · nhẹ / vừa</p>
   <p><b class="b">&gt; 0,25</b> · khác biệt mạnh</p></div>
  <p class="cap" style="margin-top:24px;font-size:21px">KS ổn định qua ba cửa sổ (độ dài lịch sử 0,68–0,72; tỷ lệ tuần = 0 0,35–0,40).</p>
 </div>
</div>""", "NGUỒN · code/dataset_shift.py → code/outputs/dataset_shift.md (mục 1–2)",
      ["Ở bài mẫu, shift là giữa dây chuyền A và B. Ở đề tài, có hai loại shift: giữa hai bối cảnh bán lẻ và giữa các giai đoạn.",
       "Bảng này là shift giữa M5 và VN1, cửa sổ chính. Hầu hết đặc trưng có PSI trên 0,25."])

slide("03", "3.2 Drift classifier phân biệt M5 và VN1: AUC đến 0,994", """
<div class="row" style="gap:60px">
 <div style="flex:1">""" + table(["Bộ đặc trưng", "Chính", "Thứ hai", "Thứ ba"],
    [["Tất cả đặc trưng", "0,994", "0,993", "0,992"],
     ["9 đặc trưng chung (không độ dài lịch sử, không giá)", "0,913", "0,908", "0,893"],
     ["Chỉ ADI và CV²", "0,865", "0,866", "0,855"]], num=(1, 2, 3)) + """
 </div>
 <div style="width:620px">
  <div class="box"><span class="tag">CÁCH LÀM</span>
   <p>Gán nhãn 0 cho chuỗi M5, 1 cho chuỗi VN1, mẫu cân bằng, phân loại 5-fold CV. Nếu hai bộ giống nhau → AUC ≈ 0,5.</p></div>
  <div class="box why"><p><b>Đọc kết quả.</b> Chỉ riêng ADI và CV² đã tách được phần lớn khác biệt; các đặc trưng còn lại
  thêm khoảng 0,04–0,05 AUC. Hai bộ là hai bối cảnh khác nhau thật, nên cần kiểm tra cả hai.</p></div>
 </div>
</div>""", "NGUỒN · code/dataset_shift.py → code/outputs/dataset_shift.md (mục 3) · 06_experiment_results/phase2_b1_b2.md",
      ["Huấn luyện bộ phân loại đoán chuỗi thuộc M5 hay VN1.",
       "Với mọi đặc trưng, AUC 0,994. Chỉ ADI và CV² đã 0,865. Hai bộ khác nhau rõ, nên kết luận trên M5 chưa chắc đúng trên VN1."])

slide("03", "3.3 Xử lý shift: cân lại VN1 cho giống M5", """
<div class="row" style="gap:56px">
 <div style="width:640px">
  <div class="box"><span class="tag">01 · IMPORTANCE REWEIGHTING</span>
   <p class="formula">w(x) ∝ p(x) / (1 − p(x))</p>
   <p>p(x) từ bộ phân loại trên 9 đặc trưng chung. Trung bình |SMD|: <b style="color:var(--ink)">0,32–0,39 → 0,02–0,03</b>
   (|SMD| &lt; 0,1 là cân bằng). Cỡ mẫu hiệu dụng 1.671–2.039 chuỗi.</p></div>
  <div class="box why"><p><b>Kết luận.</b> Sau khi cân lại, phương pháp dẫn đầu trên VN1 vẫn như bản gốc ở cả ba cửa sổ.
  Khác biệt giữa hai bộ không chỉ do thành phần chuỗi (thưa, ngắn), mà còn do động thái nhu cầu.</p></div>
 </div>
 <div style="flex:1">""" + table(["Cửa sổ", "VN1 gốc", "VN1 cân lại như M5", "M5 gốc"],
    [["Chính", "LGB-Q (1,40)", "LGB-Q (2,20)", "LGB-Q (1,00)"],
     ["Thứ hai", "TSB-NB (1,80)", "TSB-NB (2,50)", "LGB-Q (1,20)"],
     ["Thứ ba", "LGB-Q (1,25)", "LGB-Q (1,40)", "LGB-Q (1,00)"]]) + """
  <p class="cap" style="margin-top:22px;font-size:20px">Phương pháp dẫn đầu (frontier rank, 1 = ít tồn kho nhất trên fill 0,90–0,98).</p>
 </div>
</div>""", "NGUỒN · code/matched_comparison.py → code/outputs/matched_comparison.md (mục 1–3)",
      ["Tương tự bước cân lại mẫu train của bài mẫu, nhưng mục đích ở đây là kiểm tra: nếu VN1 có cùng thành phần chuỗi như M5 thì kết quả có giống M5 không.",
       "Cân bằng tốt: SMD trung bình giảm từ khoảng 0,35 xuống 0,02. Nhưng người dẫn đầu trên VN1 không đổi, đặc biệt cửa sổ thứ hai vẫn là TSB-NB."])

slide("03", "3.4 Shift theo thời gian: nhu cầu đổi khi vào kiểm thử", """
""" + img("code/outputs/eda/eda_5_growth_by_window.png", 1580, "margin:0 auto") + """
<p class="cap" style="margin-top:20px">Chuỗi tăng &gt; 1,5×: M5 <b>19,5–23,8%</b>, VN1 <b>22,3–29,4%</b>. Chuỗi giảm &lt; 0,67×:
M5 14,3–19,5%, VN1 <b>28,9–34,4%</b>.</p>""",
      "NGUỒN · code/outputs/eda/eda_5_growth_by_window.png · eda_summary.md",
      ["Loại shift thứ hai: theo thời gian. So nhu cầu trong cửa sổ kiểm thử với 26 tuần trước đó.",
       "VN1 có nhiều chuỗi đổi mạnh hơn M5, cả tăng lẫn giảm. Đây là nguyên nhân người thắng trên VN1 đổi theo giai đoạn."])

# ============================================================================================ 04 Mô hình & đánh giá
slide("04", "4.1 Bảy phương pháp, cùng một chính sách kho", """
<div class="grid2" style="gap:36px 60px">
 <div class="box"><span class="tag">THỐNG KÊ · TỪNG CHUỖI</span>
  <p><b style="color:var(--ink)">EMP</b> · phân vị thực nghiệm của tổng h tuần trong quá khứ</p>
  <p><b style="color:var(--ink)">ETS</b> · làm trơn hàm mũ, phân phối chuẩn</p>
  <p><b style="color:var(--ink)">TSB-NB</b> · xác suất có bán × lượng bán, nhị thức âm (nhu cầu gián đoạn)</p></div>
 <div class="box b"><span class="tag">GRADIENT BOOSTING · MỘT MÔ HÌNH CHO MỌI CHUỖI</span>
  <p><b style="color:var(--ink)">LGB-Q</b> · LightGBM học trực tiếp 5 phân vị {0,5; 0,8; 0,9; 0,95; 0,99}</p>
  <p><b style="color:var(--ink)">HGB-Q</b> · như LGB-Q, thư viện scikit-learn</p>
  <p><b style="color:var(--ink)">LGB-T / LGB-C</b> · dự báo điểm Tweedie + tồn kho an toàn chuẩn / conformal</p></div>
</div>
<div class="box why"><p><b>Đối chứng thêm.</b> N-HiTS (deep learning, đơn biến) và Chronos-2 (foundation model, zero-shot).
<b>Kết hợp</b> C2 = trung bình phân vị LGB-Q và TSB-NB (post hoc); E7 / E7-med = trung bình / trung vị cả 7 phương pháp (chốt trước khi chạy).</p></div>""",
      "NGUỒN · code/f2d/models.py · bài báo mục 3.2",
      ["Hai nhóm phương pháp. Mô hình chính LGB-Q học trực tiếp các phân vị. LGB-T là cách dự báo điểm rồi cộng tồn kho an toàn.",
       "Mọi phương pháp dùng đúng cùng một chính sách đặt hàng, nên khác biệt chỉ đến từ dự báo."])

slide("04", "4.2 Huấn luyện và độ nhạy siêu tham số (h = 3, cửa sổ chính)", table(
    ["Dữ liệu", "Cấu hình LightGBM", "wQL LGB-Q", "Tồn kho LGB-Q", "Δ LGB-T", "Δ TSB-NB"],
    [["M5", "mặc định · 63 lá, ≥ 200 mẫu/lá, λ2 = 1", "0,0761", "1,124", "+5,5%", "+10,4%"],
     ["M5", "cây nhỏ · 15 lá", "0,0771", "1,154", "+4,7%", "+7,5%"],
     ["M5", "cây lớn · 255 lá", "0,0759", "1,119", "+6,8%", "+11,0%"],
     ["M5", "điều chuẩn · 31 lá, ≥ 500 mẫu/lá, λ2 = 10", "0,0761", "1,131", "+5,3%", "+9,8%"],
     ["VN1", "mặc định", "0,1026", "2,544", "−2,5%", "+5,0%"],
     ["VN1", "cây nhỏ · 15 lá", "0,1071", "2,751", '<span class="b">−8,9%</span>', "−2,9%"],
     ["VN1", "cây lớn · 255 lá", "0,1015", "2,520", "−4,5%", "+6,0%"],
     ["VN1", "điều chuẩn", "0,1036", "2,575", "−3,6%", "+3,7%"]], num=(2, 3, 4, 5)) + """
<p class="cap" style="margin-top:20px">Fill rate 0,92. Δ dương = LGB-Q cần ít hàng hơn. Không tinh chỉnh siêu tham số; learning rate 0,05,
feature fraction 0,8. Trên M5 kết luận giữ ở cả bốn cấu hình; trên VN1, cây nhỏ làm LGB-T vượt LGB-Q.</p>""",
      "NGUỒN · code/hparam_sensitivity.py → code/outputs/hparam_sensitivity.md",
      ["Nhóm không tinh chỉnh siêu tham số mà kiểm tra độ nhạy với bốn cấu hình.",
       "M5: LGB-Q luôn cần ít hàng hơn LGB-T 4,7–6,8% và TSB-NB 7,5–11%. VN1 nhạy hơn: với cây nhỏ, LGB-T cần ít hơn LGB-Q 8,9%."])

slide("04", "4.3 Độ chính xác: LGB-Q có wQL thấp nhất ở mọi cửa sổ", table(
    ["Phương pháp", "M5 wQL", "M5 hạng TB", "VN1 wQL", "VN1 hạng TB"],
    [["EMP", "0,115", "4,85", "0,172", "4,72"], ["TSB-NB", "0,088", "4,22", "0,129", "3,25"],
     ["ETS", "0,084", "4,12", "0,129", "4,50"], ["LGB-T", "0,083", "3,87", "0,121", "4,68"],
     ["LGB-C", "0,086", "4,50", "0,120", "4,43"], ["HGB-Q", "0,077", "3,35", "0,104", "3,23"],
     ["LGB-Q", "0,076", "3,10", "0,103", "3,18"]], num=(1, 2, 3, 4), hl=(6,)) + """
<p class="cap" style="margin-top:20px">Cửa sổ chính, h = 3. Trên VN1, LGB-Q, HGB-Q và TSB-NB cách nhau ≤ 0,17 hạng; ở h = 13, TSB-NB có
hạng tốt nhất trên VN1 ở cả ba cửa sổ (2,92 / 2,99 / 3,37).</p>""",
      "NGUỒN · bài báo Bảng 2 và mục 5.1",
      ["Về sai số, LGB-Q tốt nhất ở cả hai bộ và cả ba cửa sổ; HGB-Q sát sau.",
       "Nhưng ở cấp từng chuỗi VN1, ba phương pháp gần như ngang nhau, và ở h = 13 TSB-NB đứng đầu. Sai số thấp nhất tổng thể không có nghĩa là tốt nhất ở mọi chuỗi."])

slide("04", "4.4 Đường đánh đổi tồn kho – fill rate (cửa sổ chính)",
      img("08_final_submission/fig1_tradeoff.png", 1360, "margin:0 auto"),
      "NGUỒN · bài báo Hình 1 · 08_final_submission/fig1_tradeoff.png",
      ["Tương đương đường PR/ROC của bài mẫu. Trục ngang là tồn kho theo tuần nhu cầu, trục dọc là fill rate thực tế.",
       "Mỗi điểm là một mức τ; nội suy dọc đường để đọc tồn kho cần cho fill 0,90–0,98, khoảng tin cậy từ 200 lần bootstrap theo chuỗi.", "Trên M5, đường LGB-Q (hồng) nằm trên cùng. Trên VN1 các đường gần nhau hơn nhiều."])

slide("04", "4.5 Tồn kho cần ở fill rate 0,94, so với LGB-Q", table(
    ["Dữ liệu", "Cửa sổ", "LGB-Q (tuần)", "HGB-Q", "LGB-T", "LGB-C", "TSB-NB", "ETS"],
    [["M5", "chính", "1,38", "+1,2", "+5,1", "+4,5", "+10,0", "+10,6"],
     ["M5", "thứ hai", "1,49", "+1,4", "+6,8", "+8,2", "+7,5", "+8,0"],
     ["M5", "thứ ba", "1,74", "+0,2", "+3,3", "+7,5", "+4,9", "+5,9"],
     ["VN1", "chính", "3,17", "+4,5", "+0,9", "+1,7", "+10,5", "+12,0"],
     ["VN1", "thứ hai", "1,79", "−1,2", '<span class="b">−7,7</span>', '<span class="b">−4,1</span>', '<span class="b">−8,8</span>', "−0,4"],
     ["VN1", "thứ ba", "3,31", "+1,3", "—", "+11,5", "—", "—"]], num=(2, 3, 4, 5, 6, 7)) + """
<p class="cap" style="margin-top:20px">Δ = tồn kho phương pháp / LGB-Q − 1 (%); dương = LGB-Q cần ít hơn; “—” = không đạt 0,94.
<b>M5:</b> LGB-Q dẫn đầu ở 100% lần bootstrap. <b>VN1:</b> người dẫn đầu đổi theo cửa sổ.</p>""",
      "NGUỒN · bài báo Bảng 3 · code/outputs/equal_fill_ci.md, equal_fill_ci_w26.md, equal_fill_ci_w52.md",
      ["M5 rõ ràng: LGB-Q cần ít hơn 3,3–10,6% so với LGB-T, LGB-C, TSB-NB, ETS, khoảng tin cậy không chứa 0.",
       "VN1 cửa sổ thứ hai: TSB-NB cần ít hơn LGB-Q 8,8%, dù sai số cao hơn. Đây là câu trả lời cho RQ1: hai bảng xếp hạng không trùng nhau trên VN1."])

slide("04", "4.6 VN1: ổn định hợp TSB-NB, tăng mạnh hợp LGB-Q", table(
    ["Dữ liệu", "Cửa sổ", "Tỷ trọng nhu cầu chuỗi tăng", "Δ TSB-NB · ổn định", "Δ TSB-NB · tăng", "Δ TSB-NB · tất cả"],
    [["M5", "chính", "20,7%", "+8,5", "+12,5", "+10,4"], ["M5", "thứ hai", "28,0%", "+7,7", "+7,7", "+5,5"],
     ["M5", "thứ ba", "19,4%", "+3,9", "+5,7", "+6,1"],
     ["VN1", "chính", "31,5%", '<span class="b">−14,4</span>', "không đạt", "+5,0"],
     ["VN1", "thứ hai", "22,8%", '<span class="b">−13,3</span>', "−10,5", "−11,3"],
     ["VN1", "thứ ba", "40,4%", '<span class="b">−15,6</span>', "không đạt", "+25,1"]], num=(2, 3, 4, 5)) + """
<div class="box why"><p><b>Chọn trước có giúp không?</b> Chọn theo ADI–CV², theo phân cụm (GMM 3 cụm, silhouette 0,21) hay theo cửa sổ trước
đều <b>không ổn định</b>: trên VN1, từ cửa sổ thứ hai sang chính, phần lớn quy tắc cần thêm +4,8 đến +10,5% hàng so với luôn dùng LGB-Q.
Nhóm chuỗi được định nghĩa hồi cứu, nên phép tách này không dùng được để triển khai.</p></div>""",
      "NGUỒN · bài báo Bảng 4–5, mục 5.3–5.4",
      ["Tách chuỗi theo nhu cầu trong cửa sổ kiểm thử so với 26 tuần trước. Trên chuỗi ổn định, TSB-NB tiết kiệm 13–16% ở fill 0,92.",
       "Nhưng nhóm này chỉ biết sau. Các quy tắc chọn trước theo ADI–CV², phân cụm hay cửa sổ trước đều không ổn định."])

slide("04", "4.7 C2 = trung bình phân vị LGB-Q và TSB-NB <span class=\"flag\">POST HOC</span>", """
<div class="row" style="gap:80px;margin-bottom:34px">
 <div><div class="k">Regret lớn nhất · C2</div><div class="mid b">0,9%</div></div>
 <div><div class="k">LGB-Q</div><div class="mid">9,4%</div></div>
 <div><div class="k">LGB-T</div><div class="mid">9,5%</div></div>
 <div><div class="k">HGB-Q</div><div class="mid">11,4%</div></div>
 <div><div class="k">TSB-NB</div><div class="mid">20,7%</div></div>
</div>
<ol class="obs">
 <li><b>VN1:</b> C2 cần ít hơn LGB-Q 5,9% / 10,5% / 7,1% tồn kho ở fill 0,92 (ba cửa sổ, khoảng tin cậy không chứa 0). <b>M5:</b> lệch LGB-Q ≤ 1,5%.</li>
 <li><b>Regret</b> = tồn kho dư so với phương pháp đơn tốt nhất nếu biết trước, trung bình trên các mức fill đạt được, lấy giá trị lớn nhất qua 6 lần chạy.</li>
 <li><b>Chưa được kiểm chứng độc lập:</b> C2 được chọn sau khi xem kết quả. Bước tiếp theo là cố định cấu hình rồi thử trên giai
 đoạn sau và bộ dữ liệu khác (prospective), trong doanh nghiệp thì chạy song song (shadow mode) trước khi chuyển.</li>
</ol>""", "NGUỒN · code/outputs/combination.md · bài báo mục 5.5 và 6",
      ["Không biết trước phương pháp nào thắng, nhóm thử phòng hộ bằng trung bình hai phương pháp.",
       "C2 có regret lớn nhất chỉ 0,9%. Nhưng phải nói rõ, như reviewer yêu cầu: C2 được chọn sau khi xem kết quả, nên đây là giả thuyết cần kiểm chứng, chưa phải khuyến nghị triển khai."])

slide("04", "4.8 Kết hợp cả 7 phương pháp và ablation <span class=\"flag\">CHỐT THIẾT KẾ TRƯỚC KHI CHẠY</span>", table(
    ["Kết hợp", "VN1 · tồn kho vs LGB-Q (fill 0,92)", "M5 · tồn kho vs LGB-Q (fill 0,92)", "Regret lớn nhất", "Đạt tiêu chí?"],
    [["E7 · trung bình 7 phương pháp", "−4,6 đến −6,1% (3/3 có ý nghĩa)", '<span class="b">+0,8 đến +3,1%</span>', "3,4%", "Không (M5 kém &gt; 1%)"],
     ["E7-med · trung vị 7 phương pháp", "−7,1 đến −8,2% (3/3 có ý nghĩa)", "−0,9 đến +1,6%", '<span class="b">0,3%</span>', "Gần đạt (M5 +1,6%)"],
     ["C2 · LGB-Q + TSB-NB (post hoc)", "−5,9 đến −10,5%", "−1,5 đến +0,4%", "0,9%", "—"],
     ["Chọn tổ hợp ở cửa sổ trước → áp dụng cửa sổ sau", "−7,8 đến −8,2% (2/2 có ý nghĩa)", "−0,6 / +0,9%", "—", "Không (M5 kém 0,9% một lần)"]],
    hl=(1,)) + """
<div class="grid2" style="grid-template-columns:1fr 1fr;gap:36px;margin-top:30px">
 <div class="box"><span class="tag">ABLATION · BỎ TỪNG PHƯƠNG PHÁP KHỎI E7</span>
  <p>Bỏ <b style="color:var(--ink)">LGB-Q hoặc HGB-Q</b> → cần thêm 1,0–4,5% hàng (đóng góp nhiều nhất).
  Bỏ <b style="color:var(--ink)">ETS</b> → cần ít hàng hơn ở cả 6 lần chạy (kéo tổ hợp xuống).
  Tổ hợp tốt nhất của cả 6 lần chạy (trong 127 tập con) đều chứa <b style="color:var(--ink)">LGB-Q + TSB-NB</b>.</p></div>
 <div class="box why" style="margin-top:0"><p><b>Đọc kết quả.</b> Kết hợp giảm tồn kho rõ rệt trên VN1 nhưng không hơn LGB-Q trên M5.
  Mọi tổ hợp đều có <b>wQL cao hơn</b> LGB-Q (E7-med VN1: 0,110 so với 0,103) mà vẫn cần <b>ít hàng hơn</b>. Nhưng đây là lợi thế <b>ex-post</b> — xem kiểm tra prospective ở tờ 4.9.</p></div>
</div>""", "NGUỒN · code/ensemble_ablation.py → code/outputs/ensemble/ensemble_ablation.md · thiết kế: 07_paper_draft/phase5_workflow.md mục 7",
      ["Theo góp ý của thầy, nhóm kết hợp cả 7 phương pháp. Thiết kế và tiêu chí được ghi lại trước khi chạy, để không lặp lại vấn đề post hoc của C2.",
       "E7 trung bình không đạt tiêu chí vì kém LGB-Q khoảng 3% trên M5. Trung vị E7-med ổn định nhất: regret lớn nhất chỉ 0,3%, trên VN1 giảm 7–8% tồn kho.",
       "Ablation cho thấy nên kết hợp các phương pháp phân vị trực tiếp với TSB-NB; thêm các phương pháp yếu như ETS làm tổ hợp kém đi.",
       "Cặp LGB-Q + TSB-NB xuất hiện trong tổ hợp tốt nhất ở cả 6 lần chạy, nên cấu trúc của C2 không phải ngẫu nhiên."])

slide("04", "4.9 Kết hợp có giữ khi triển khai thật? <span class=\"flag\">CHỐT TIÊU CHÍ TRƯỚC</span>", table(
    ["Phép kiểm tra", "M5", "VN1", "Kết luận"],
    [["τ chọn ở cửa sổ trước, áp cho cửa sổ sau", "fill lệch ≤ 0,8 điểm; LGB-T, LGB-C, TSB-NB, ETS cần thêm 3,8–14,2% hàng", "fill lệch tới 4,6 điểm; kết hợp lúc dư, lúc thiếu hàng", "M5 giữ · VN1 không"],
     ["Hiệu chỉnh τ hằng tuần bằng fill đã quan sát", "không cần (đã lệch ≤ 0,5 điểm)", "lệch giảm còn 2,4 điểm (tiêu chí ≤ 1); E7-med không lần nào ít hàng hơn LGB-Q có ý nghĩa; TSB-NB cần thêm 28–42%", '<span class="b">Không đạt</span>'],
     ["Bootstrap theo sản phẩm, cửa hàng, kho, nhà bán, khối tuần (1.000 lần)", "12/12 khẳng định giữ", "chỉ còn khoản tiết kiệm ở cửa sổ thứ hai có ý nghĩa", "M5 giữ · VN1 yếu"],
     ["Bộ dữ liệu độc lập VNF (909 chuỗi giày dép, chưa dùng để thiết kế)", "—", "LGB-Q cần ít hàng nhất; E7-med +2,4%, C2 +0,3%", '<span class="b">Không xác nhận</span>'],
     ["Hết hàng: 4 ngưỡng × 3 cách bù nhu cầu", "TSB-NB luôn kém LGB-Q 11,8–34,2%", "E7-med regret lớn nhất ≤ 1,6% ở mọi kịch bản", "Giữ"]]) + """
<div class="box why"><p><b>Đọc kết quả.</b> Lợi thế 7–8% của E7-med trên VN1 là <b>ex-post</b>: không giữ khi chọn mức phục vụ chỉ bằng quá khứ,
khi bootstrap theo kho, và trên dữ liệu độc lập. Kết luận trên M5 thì vững trước mọi phép kiểm tra. <b>LGB-Q là lựa chọn mặc định đáng tin cậy.</b>
Đây cũng chính là thông điệp của bài: phải đánh giá bằng quyết định khi triển khai thật.</p></div>""",
      "NGUỒN · code/prospective_tau.py, rolling_calibration.py, bootstrap_robust.py, censoring_sensitivity.py → code/outputs/robustness/ · thiết kế: phase5_workflow.md mục 8–9",
      ["Sau góp ý, nhóm kiểm tra xem lợi thế của kết hợp có giữ khi đánh giá theo cách triển khai thật không. Tiêu chí được ghi trước khi chạy.",
       "Trên M5 mọi kết luận đều giữ: chọn τ trước, bootstrap theo cụm và theo thời gian, các kịch bản hết hàng.",
       "Trên VN1, lợi thế của E7-med không giữ khi hiệu chỉnh τ chỉ bằng quá khứ, khi bootstrap theo kho, và không được xác nhận trên bộ giày dép độc lập VNF.",
       "Nhóm báo cáo trung thực: kết hợp là kết quả thăm dò, LGB-Q là lựa chọn mặc định."])

slide("04", "4.10 Kết quả prospective: fill đạt được và tồn kho cùng lúc <span class=\"flag\">BẢNG 7</span>", table(
    ["Phương pháp", "M5 3→2", "M5 2→chính", "VN1 3→2", "VN1 2→chính", "Giày dép (VNF)"], table7_rows(), hl=(0,)) + """
<div class="grid2" style="grid-template-columns:1.15fr 1fr;gap:36px;margin-top:26px">
 <div class="box"><span class="tag">CÁCH ĐỌC</span>
  <p>Mỗi ô: <b style="color:var(--ink)">fill đạt được · tồn kho so với LGB-Q</b> [khoảng tin cậy 95% theo cụm: M5 sản phẩm, VN1 kho, VNF mẫu giày].
  Mục tiêu fill 0,92; τ cập nhật hằng tuần chỉ bằng fill đã quan sát. <b style="color:var(--ink)">Chỉ coi là tiết kiệm khi fill lệch nhau dưới 0,5 điểm.</b></p></div>
 <div class="box"><span class="tag">BỘ ĐỘC LẬP · GIÀY DÉP VIỆT NAM</span>
  <p>Kaggle (tienanh2003/sales-and-inventory-snapshot-data), kênh bán lẻ; 909 chuỗi mẫu × màu, 82 tuần (01/2022–07/2023), một cửa sổ 26 tuần từ 30/01/2023;
  cùng pipeline, 21 đặc trưng; không dùng để thiết kế tổ hợp.</p></div>
</div>""", "NGUỒN · code/rolling_calibration.py → code/outputs/robustness/rolling_calibration.csv · bài báo Bảng 7, mục 3.1 và 5.8",
      ["Đây là Bảng 7 của bài: đánh giá theo cách triển khai thật, nên báo cáo fill đạt được cạnh tồn kho, không chỉ tồn kho.",
       "Trên VN1 và bộ giày dép, E7-med không lần nào cần ít hàng hơn LGB-Q một cách có ý nghĩa ở fill tương đương; C2 làm được một lần ở VN1.",
       "TSB-NB, phương pháp thắng ex-post ở cửa sổ thứ hai VN1, khi triển khai lại cần thêm 28–33% hàng.",
       "Bộ giày dép là dữ liệu độc lập: LGB-Q cần ít hàng nhất ở cùng fill."])

slide("04", "4.11 Độ vững: lead time, chi phí mất khách, deep learning", """
<div class="grid2" style="gap:40px 60px">
 <div class="box"><span class="tag">LEAD TIME 1, 2, 4 TUẦN · 18 LẦN CHẠY</span><h3>C2 2,0% · LGB-Q 12,6%</h3>
  <p>Regret lớn nhất so với phương pháp đơn tốt nhất trong sáu phương pháp (không có HGB-Q).</p></div>
 <div class="box"><span class="tag">QUY RA CHI PHÍ</span><h3>Ngưỡng ≈ 200 tuần giữ hàng</h3>
  <p>Khi phạt mất khách dưới khoảng 200 tuần chi phí giữ hàng, C2 trong phạm vi 3,1% của phương pháp đơn rẻ nhất; phạt cao hơn thì LGB-Q tốt nhất.</p></div>
 <div class="box"><span class="tag">N-HiTS · DEEP LEARNING</span><h3>M5: +2,6 đến +8,9%</h3>
  <p>Hàng cần thêm so với LGB-Q. wQL nằm giữa LGB-Q và TSB-NB ở cả 6 lần chạy; độ phủ phân vị 0,99 là 0,986–0,992.</p></div>
 <div class="box"><span class="tag">CẤU HÌNH LightGBM</span><h3>M5 giữ ở 4/4 cấu hình</h3>
  <p>VN1 nhạy với kích thước cây (mục 4.2).</p></div>
</div>""", "NGUỒN · code/outputs/leadtime_equal_fill.md · code/outputs/neural_eval.md · bài báo mục 5.8 và 6",
      ["Đổi lead time: C2 vẫn có regret thấp nhất.",
       "Quy ra chi phí: nếu mất khách cực kỳ đắt, phương pháp chính xác nhất LGB-Q mới là lựa chọn tốt nhất.",
       "N-HiTS chạy dạng tiêu chuẩn, không tinh chỉnh, cần nhiều hàng hơn LGB-Q trên M5."])

slide("04", "4.12 Chi phí tính toán so với hiệu quả tồn kho <span class=\"flag\">REVIEWER · MỤC 3</span>", table(
    ["Phương pháp", "Loại", "Thời gian · M5", "Thời gian · VN1", "Tồn kho vs LGB-Q (fill 0,92)"],
    [["TSB-NB", "thống kê", "1,1–2,3 phút", "≈ 0,5 phút", "M5 +5,5 đến +10,4% · VN1 −11,3 đến +25,1%"],
     ["LGB-Q", "ML toàn cục, 5 mô hình", "10–21 phút", "2,4–4,4 phút", "mốc so sánh"],
     ["C2", "LGB-Q + TSB-NB", "≈ LGB-Q + 1–2 phút", "≈ LGB-Q + 0,5 phút", "M5 −1,5 đến +0,4% · VN1 −5,9 đến −10,5%"],
     ["N-HiTS", "deep learning", "≈ 7 phút", "5,1–5,7 phút", "M5 +2,6 đến +8,9% · VN1 −2,1 đến +8,3%"],
     ["Chronos-2", "foundation, zero-shot", '<span class="b">5,4 giờ</span>', "32–45 phút", '<span class="b">M5 +14,7% · VN1 +1,2 đến +48,1%</span>']],
    num=()) + """
<div class="box why"><p><b>Đọc kết quả.</b> Chu kỳ đặt hàng là mỗi tuần, nên vài phút đến khoảng 20 phút trên CPU laptop không phải ràng buộc.
Mô hình tốn kém nhất không mua được hiệu quả tồn kho ở đây. <b>Giới hạn:</b> Chronos-2 chạy zero-shot, không fine-tune, không biến ngoại sinh;
thời gian đo trên hai máy (N-HiTS M5 trên máy thành viên B), chỉ đúng ở mức độ lớn.</p></div>""",
      "NGUỒN · 06_experiment_results/phase4_compute_cost.md (thành viên A) · logs run_*_c2.log · bài báo mục 5.8",
      ["Reviewer hỏi về đánh đổi giữa chi phí tính toán và hiệu quả của mô hình zero-shot so với N-HiTS.",
       "Chronos-2 không cần huấn luyện nhưng suy luận trên CPU mất 5,4 giờ mỗi cửa sổ M5 và cần nhiều hàng nhất. Đây là kết quả cho bản tiêu chuẩn, không phải giới hạn trên của foundation model."])

slide("04", "4.13 Hết hàng có làm đổi thứ hạng? <span class=\"flag\">REVIEWER · MỤC 2</span>", """
<div class="row" style="gap:50px">
 <div style="width:600px">
  <div class="box"><span class="tag">PHÁT HIỆN TỪ DOANH SỐ</span>
   <p class="formula">(1 − p)<sup>k</sup> &lt; α = 0,01</p>
   <p>Chuỗi k tuần = 0 nằm giữa hai lần bán, với p là tần suất có bán trước kiểm thử, bị gắn cờ nghi hết hàng.
   Tỷ lệ tuần kiểm thử bị gắn cờ: <b style="color:var(--ink)">M5 7,4–9,0%</b>, <b style="color:var(--ink)">VN1 6,1–6,9%</b>,
   gấp khoảng đôi ở chuỗi gián đoạn. Đây là <b style="color:var(--ink)">cận trên</b> (cả khoảng nghỉ thật cũng bị gắn cờ).</p></div>
 </div>
 <div style="flex:1">""" + table(["Kịch bản", "Người dẫn đầu", "Kết quả chính"],
    [["(a) Chỉ chuỗi sạch (72–82% chuỗi)", "không đổi ở 6/6 cửa sổ", "C2 vẫn có regret lớn nhất thấp nhất"],
     ["(b) Bù nhu cầu ở tuần bị gắn cờ (mức bán TB)", "đổi ở 3/6, sang phương pháp sát hạng", "TSB-NB cần +17 đến +27% so với LGB-Q trên M5 (fill 0,92)"],
     ["(b) — C2", "", "regret lớn nhất lên 9,8%; VN1 vẫn ít hơn LGB-Q 6,9–10,7%"],
     ["(a) / (b) — E7-med", "", '<span class="b">regret lớn nhất 0,1% (a) và −2,2% (b)</span>; (b): ít hơn LGB-Q 2,9–5,6% (M5), 9,5–14,7% (VN1)']], hl=(3,)) + """
  <div class="box why" style="margin-top:28px"><p><b>Kết luận.</b> Hết hàng ảnh hưởng nhiều nhất tới TSB-NB và C2. E7-med (chốt trước) thì vững:
  lợi thế còn rõ hơn khi bù nhu cầu. Cần dữ liệu tồn kho thật để kết luận chắc chắn.</p></div>
 </div>
</div>""", "NGUỒN · code/censoring_check.py (thành viên A) · code/censoring_rank_check.py, censoring_rank_check_e7.py → code/outputs/censoring/",
      ["Reviewer hỏi: dữ liệu chỉ có doanh số, tuần hết hàng ghi nhận bằng 0, vậy thứ hạng có đổi không.",
       "Thành viên A phát hiện tuần nghi hết hàng từ doanh số. Nhóm kiểm tra hai kịch bản.",
       "Trên chuỗi sạch, không đổi gì. Khi bù nhu cầu, TSB-NB bị ảnh hưởng nặng nhất vì xác suất có bán giảm trong các khoảng 0, và regret của C2 tăng lên 9,8%.",
       "Ngược lại, trung vị 7 phương pháp E7-med vẫn vững: regret lớn nhất 0,1% trên chuỗi sạch và −2,2% khi bù nhu cầu, tức tốt hơn phương pháp đơn tốt nhất ở mọi lần chạy."])

slide("04", "4.14 Thanh lý và quy tắc dùng giá thu hồi hòa vốn s*", """
<div class="row" style="gap:60px">
 <div style="flex:1">
  <div class="row" style="gap:70px;margin-bottom:30px">
   <div><div class="k">Fill rate mất · quy tắc phân vị</div><div class="mid">≤ 0,02 điểm</div></div>
   <div><div class="k">Tồn kho giảm · VN1</div><div class="mid">1,7–7,4%</div></div>
  </div>
  <div class="box"><span class="tag">GIÁ THU HỒI HÒA VỐN</span>
   <p class="formula">s* = [ΔO − ΔE + h·ΔI − (1+m)·ΔS] / Q</p>
   <p>ΔO hàng đặt, ΔE vị thế cuối kỳ (tính theo giá vốn), ΔI tồn kho, ΔS doanh số, Q lượng thanh lý; h chi phí giữ tuần, m biên lợi nhuận.
   s* là cận trên.</p></div>
 </div>
 <div style="width:640px">
  <div class="box b"><span class="tag">QUY TẮC THỰC HÀNH</span><h3>Thanh lý chỉ khi r ≥ s*</h3>
   <p>r = giá bán thanh lý / giá vốn. Trên VN1, quy tắc phân vị có <b style="color:var(--ink)">s* = 0,91–1,21</b>:
   kênh thu hồi 60% giá vốn <b style="color:var(--ink)">không đáng</b> thanh lý trong 26 tuần; kênh thu hồi xấp xỉ giá vốn thì có thể.
   Hàng lỗi mốt, kho chật hay kỳ dài hơn sẽ hạ s* (chưa mô hình hoá).</p></div>
  <p class="cap" style="margin-top:20px;font-size:20px">M5: quy tắc phân vị gần như không kích hoạt (thanh lý 0,01–0,02% nhu cầu).</p>
 </div>
</div>""", "NGUỒN · code/liquidation_breakeven.py → code/outputs/*/breakeven.csv · bài báo Bảng 6, mục 5.6",
      ["Quy tắc thanh lý theo phân vị gần như không làm mất khách.",
       "Reviewer yêu cầu hướng dẫn rõ hơn khi biết tỷ lệ thu hồi: so r với s*. Ví dụ VN1: s* từ 0,91 đến 1,21, nên kênh thu hồi 60% thì chưa đáng thanh lý."])

# ============================================================================================ 05 Insight & kết luận
slide("05", "5. Insight vận hành và khuyến nghị theo tình huống", """
<div class="grid2" style="gap:36px 60px">
 <div class="box"><span class="tag">CỬA HÀNG TRUYỀN THỐNG · KIỂU M5</span><h3>Dùng LGB-Q</h3>
  <p>Vừa chính xác nhất vừa cần ít hàng nhất ở cả ba cửa sổ: ít hơn 3,3–10,6% so với dự báo điểm + tồn kho an toàn, TSB-NB, ETS (fill 0,94).</p></div>
 <div class="box"><span class="tag">NHIỀU NHÀ BÁN · KIỂU VN1</span><h3>Không có người thắng cố định</h3>
  <p>Người dẫn đầu đổi theo giai đoạn; không chọn trước được. Kết hợp chỉ giảm 6–8% tồn kho ex-post, không giữ khi triển khai thật: dùng LGB-Q làm mặc định.</p></div>
 <div class="box"><span class="tag">KHI MẤT KHÁCH RẤT ĐẮT</span><h3>Ưu tiên LGB-Q</h3>
  <p>Khi phạt mất khách trên khoảng 200 tuần chi phí giữ hàng; theo dõi độ phủ phân vị trên, nơi TSB-NB phủ thiếu.</p></div>
 <div class="box b"><span class="tag">THANH LÝ</span><h3>Chỉ khi r ≥ s*</h3>
  <p>Ước lượng tỷ lệ thu hồi thật của kênh thứ cấp trước; với chi phí giả định, chưa quy tắc nào sinh lời trong 26 tuần.</p></div>
</div>
<p class="cap" style="margin-top:28px;font-size:20px"><b>[Nhận định nhóm]</b> Đánh giá dự báo nên đo bằng quyết định nó tạo ra (tồn kho ở cùng fill rate), không chỉ bằng sai số.</p>""",
      "NGUỒN · bài báo mục 6–7",
      ["Bốn khuyến nghị theo tình huống, đều rút từ kết quả.",
       "Riêng C2, nhóm chỉ đề xuất như một ứng viên cần kiểm chứng, không khuyến nghị triển khai ngay."])

slide("05", "Những điều bài chưa trả lời được", table(
    ["Hạn chế", "Mức độ và hướng xử lý"],
    [["Doanh số ≠ nhu cầu", "Hết hàng chỉ được suy ra; thứ hạng giữ trên chuỗi sạch nhưng nhạy khi bù nhu cầu. Cần dữ liệu tồn kho thật."],
     ["Kết hợp chưa qua kiểm chứng", "C2 chọn sau kết quả; E7-med chốt trước nhưng không giữ khi hiệu chỉnh τ bằng quá khứ, bootstrap theo kho và trên VNF."],
     ["Chi phí giả định", "Không có chi phí thật; kết luận thanh lý phụ thuộc h, m và tỷ lệ thu hồi."],
     ["Không tinh chỉnh siêu tham số", "M5 giữ ở 4 cấu hình; VN1 nhạy với kích thước cây."],
     ["Nhóm chuỗi định nghĩa hồi cứu", "Bộ phân loại chuỗi tăng trưởng chỉ thu được một phần lợi ích và không ổn định."],
     ["Deep learning bản tiêu chuẩn", "N-HiTS đơn biến, Chronos-2 zero-shot; không phải giới hạn trên của các họ mô hình này."],
     ["Hướng mở rộng", "Phiên bản phân vị của mô hình hai giai đoạn (phân loại có bán × hồi quy lượng bán, Nabil và cộng sự 2026)."]]),
      "NGUỒN · bài báo mục 6 (Limitations, Censored demand)",
      ["Nhóm nói rõ các hạn chế. Quan trọng nhất là doanh số không phải nhu cầu, và C2 được chọn sau kết quả.",
       "Hướng mở rộng cho bản journal: mô hình hai giai đoạn dạng phân vị."])

slide("05", "Tổng kết", """
<ol class="steps" style="max-width:1560px">
 <li><b>Thứ hạng bất ổn giữa bối cảnh và giai đoạn</b>Trên M5, chính xác nhất cũng là ít hàng nhất (LGB-Q); trên VN1 thì không: cửa sổ thứ hai TSB-NB cần ít hơn LGB-Q 8,8% dù sai số cao hơn.</li>
 <li><b>Không chọn trước được theo nhóm</b>ADI–CV², phân cụm hay cửa sổ trước đều không ổn định; khác biệt M5–VN1 vẫn còn sau khi cân lại thành phần chuỗi.</li>
 <li><b>Lợi thế ex-post chưa chắc giữ khi triển khai</b>Trung vị 7 phương pháp giảm 7–8% tồn kho trên VN1 ex-post, nhưng không giữ khi chọn τ bằng quá khứ, bootstrap theo kho và trên dữ liệu độc lập; LGB-Q là mặc định đáng tin.</li>
 <li><b>Thanh lý theo quy tắc r ≥ s*</b>Trên VN1 cần thu hồi khoảng 0,91–1,21 giá vốn mới có lợi trong 26 tuần.</li>
</ol>
<p class="lead" style="margin-top:10px">Cảm ơn thầy cô và các bạn đã lắng nghe.</p>""",
      "NGUỒN · bài báo mục 7 · code và kết quả: github.com/anhduyBA/forecast-to-decision-benchmark",
      ["Bốn ý chính. Thông điệp chung: đánh giá dự báo bằng quyết định nó tạo ra.",
       "Code và mọi file kết quả công khai trên GitHub. Em xin cảm ơn."])


# ============================================================================================ render
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_style.css"), encoding="utf-8").read()


def render():
    n = len(SLIDES)
    parts = []
    for k, s in enumerate(SLIDES, 1):
        hdr = f'<div class="hdr"><div class="sec"><b>{s["sec"]}</b>{CH[s["sec"]]}</div><div>{TAG}</div></div>'
        title = "" if s["cover"] else f'<h1 class="title">{s["title"]}</h1>'
        body = s["body"] if s["cover"] else f'<div class="body">{s["body"]}</div>'
        tb = (f'<div class="tb"><div><span>Đề tài</span>{TOPIC}</div><div><span>Nhóm thực hiện</span>{TEAM}</div>'
              f'<div><span>Hướng dẫn</span>{MENTOR}</div><div><span>Tờ</span><b class="sheet">TỜ {k} / {n}</b></div></div>')
        notes = "".join(f"<li>{x}</li>" for x in s["notes"])
        parts.append(f'<section class="slide{" cover" if s["cover"] else ""}" data-n="{k}"><div class="frame">{hdr}{title}'
                     f'{body}<div class="src">{s["src"]}</div>{tb}</div><aside class="notes"><ul>{notes}</ul></aside></section>')
    js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "deck_nav.js"), encoding="utf-8").read()
    html = (f'<!DOCTYPE html>\n<html lang="vi">\n<head>\n<meta charset="UTF-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Từ dự báo đến quyết định</title>\n'
            f'<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">\n'
            f'<style>\n{CSS}\n</style>\n</head>\n<body>\n<div id="deck">\n' + "\n".join(parts) +
            f'\n</div>\n<div id="notes"></div>\n<script>\n{js}\n</script>\n</body>\n</html>\n')
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("written", OUT, "| slides:", n, "| size:", len(html) // 1024, "KB")


if __name__ == "__main__":
    render()
