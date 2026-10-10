# Results

Mọi số liệu lấy từ `code/outputs/` (bản sao: `tables/`).

- Bảng đầy đủ: `tables/comparison_full.md`.
- Kiểm định theo chuỗi: `tables/stat_tests.md`.
- Hình: `figures/fig_tradeoff_M5.png`, `figures/fig_tradeoff_VN1.png`.

Quy ước:

- Phiên bản v2.4: Tweedie học mục tiêu chuẩn hóa (mục 1.1); lưới τ = {0,5; 0,8; 0,9; 0,95; 0,99}; có thêm quy tắc dead-stock.
- Kịch bản mặc định: τ = 0,9; L = 2; R = 1; H = 13; q_L = 0,95; k = 26.
- Tồn kho tính bằng **tuần nhu cầu**.
- Với hàng chục nghìn chuỗi, gần như mọi chênh lệch đều có p < 0,001. Vì vậy kết luận dựa thêm vào **độ lớn hiệu ứng**: chênh lệch hạng so với Nemenyi CD, tỷ lệ chuỗi thắng/thua.
- [Nhận định nhóm] đánh dấu phần diễn giải, không phải số đo.

## 0. Tóm tắt

1. **Độ chính xác:**
   - LightGBM quantile có SQL **trung bình** thấp nhất trên cả hai dataset, ở cả hai horizon và cả 4 nhóm; HistGradientBoosting sát ngay sau.
   - Kiểm định theo chuỗi xác nhận điều này trên M5 (h = 3).
   - Trên VN1 thì không: xét từng chuỗi, TSB negative binomial ngang (h = 3) hoặc tốt hơn (h = 13). Lợi thế của LightGBM quantile là **ít khi sai rất nặng**.
2. **Hiệu quả tồn kho ở cùng fill rate:**
   - M5, **vững qua hai cửa sổ:** LightGBM quantile cần ít tồn kho nhất (hạng theo đường đánh đổi 1,0 và 1,2). Ở fill rate 0,94–0,96, nó cần ít hơn các baseline mạnh (Tweedie, conformal, TSB-NB, ETS) 4–13% ở cả hai cửa sổ; HistGradientBoosting bám sát (chênh dưới 3%).
   - VN1, **không vững** (mục 10):
     - Cửa sổ chính: LightGBM quantile hạng 1,4; Tweedie nhỉnh hơn ở fill rate 0,90–0,92.
     - Cửa sổ thứ hai: TSB-NB hạng 1,8, conformal 2,0, LightGBM quantile chỉ 3,8.
     - Trên VN1 chưa có phương pháp nào hiệu quả nhất một cách ổn định.
3. **Theo nhóm:**
   - M5: mô hình phân vị trực tiếp tốt nhất ở mọi nhóm.
   - VN1, vững qua hai cửa sổ: TSB-NB hiệu quả nhất ở nhóm smooth; LightGBM quantile hiệu quả nhất ở intermittent và lumpy (theo đường đánh đổi).
   - VN1, nhóm erratic: phương pháp đứng đầu đổi giữa hai cửa sổ.
4. **Độ nhất quán giữa dataset:**
   - Cửa sổ chính: xếp theo đường đánh đổi nhất quán hơn (ρ = 0,88 so với 0,69).
   - Cửa sổ thứ hai: điều này **không lặp lại** (0,50 so với 0,93).
   - Chỉ nhóm intermittent nhất quán ở cả hai cửa sổ (ρ = 0,83–0,95).
5. **Thanh lý:**
   - Quy tắc theo phân vị giảm tồn kho mà gần như không mất fill rate.
   - Quy tắc cố định và quy tắc dead-stock mất nhiều fill rate hơn hoặc làm tăng số tuần hết hàng.
   - Trong cửa sổ 26 tuần, không quy tắc nào chứng minh được lợi ích kinh tế: ngưỡng giá thu hồi hòa vốn s\* ≈ 0,91–1,04 lần giá vốn với quy tắc phân vị, và > 1 với các quy tắc khác.

## 1. RQ1 — Độ chính xác dự báo

**Bảng 1.** SQL, RMSSE và độ phủ của phân vị 0,9 (toàn bộ chuỗi). Thấp hơn là tốt hơn, trừ độ phủ (lý tưởng = 0,9).

| Mô hình | M5 SQL h=3 | M5 SQL h=13 | M5 RMSSE h=3 | M5 cov₀.₉ h=3 | VN1 SQL h=3 | VN1 SQL h=13 | VN1 RMSSE h=3 | VN1 cov₀.₉ h=3 |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,340 | 0,347 | 0,765 | 0,855 | 0,522 | 0,557 | 0,799 | 0,909 |
| tsb | 0,283 | 0,361 | 0,596 | 0,793 | 0,454 | 0,506 | 0,645 | 0,849 |
| tsb_nb | 0,251 | 0,317 | 0,610 | 0,881 | 0,411 | 0,458 | 0,650 | 0,903 |
| ets | 0,246 | 0,254 | 0,601 | 0,890 | 0,431 | 0,445 | 0,654 | 0,912 |
| lgb_tweedie | 0,229 | 0,223 | **0,565** | 0,858 | 0,439 | 0,575 | 0,651 | 0,913 |
| lgb_conformal | 0,232 | 0,241 | 0,572 | 0,901 | 0,405 | 0,507 | 0,633 | 0,906 |
| hgb_quantile | 0,211 | 0,201 | 0,572 | 0,872 | 0,338 | 0,423 | **0,593** | 0,917 |
| **lgb_quantile** | **0,208** | **0,198** | 0,570 | 0,883 | **0,336** | **0,410** | 0,594 | 0,921 |

- LightGBM quantile có SQL trung bình thấp nhất trong cả 4 cột SQL. HistGradientBoosting cách 0,002–0,013, dù chỉ huấn luyện trên tối đa 300.000 dòng. Như vậy kết quả không phụ thuộc riêng vào thư viện LightGBM.
- Về RMSSE (dự báo điểm), LightGBM-Tweedie tốt nhất trên M5, nhưng chênh lệch giữa 4 mô hình ML nhỏ (0,565–0,572).
- **Hiệu chỉnh:**
  - M5: phân vị 0,9 của các mô hình phủ 0,79–0,90, tức hơi lệch thấp; chỉ conformal đạt 0,901.
  - VN1: phần lớn phủ 0,90–0,92; riêng TSB Poisson chỉ phủ 0,849, do khoảng Poisson quá hẹp.

### 1.1 Sửa lỗi LightGBM-Tweedie (v2.4)

Bản v2.3 có RMSSE của Tweedie trên VN1 ở h = 13 bằng 1,13, kém cả Empirical.

- **Nguyên nhân:** mô hình Tweedie học tổng D_h **chưa chuẩn hóa**, trong khi mọi đặc trưng mức đã được chia cho quy mô s. Với các chuỗi gần như không bán (khoảng 0,04 đơn vị/tuần), mô hình dự báo trung vị 44–620 đơn vị cho 13 tuần. Lỗi lan rộng, không chỉ ở vài chuỗi: bỏ 1% chuỗi tệ nhất, RMSSE vẫn là 0,87.
- **Sửa:** Tweedie học cùng mục tiêu D_h / s (cắt ở phân vị 99,9) như mô hình quantile, rồi nhân lại với s (`models._fit_tweedie`). Như vậy phép so sánh (ablation) giữa "dự báo điểm + safety stock" và "phân vị trực tiếp" chỉ còn khác nhau ở cách tạo phân vị. LightGBM-conformal dùng cùng mô hình điểm nên cũng thay đổi theo.

| | VN1 SQL h=3 | VN1 SQL h=13 | VN1 RMSSE h=13 | M5 SQL h=3 | M5 SQL h=13 |
|---|---|---|---|---|---|
| Tweedie, trước → sau | 0,496 → 0,439 | 0,664 → 0,575 | 1,131 → 0,896 | 0,226 → 0,229 | 0,215 → 0,223 |
| Conformal, trước → sau | 0,436 → 0,405 | 0,590 → 0,507 | 1,074 → 0,825 | 0,229 → 0,232 | 0,231 → 0,241 |

Nguồn: `tables/tweedie_fix_before_after.csv`. Cache cũ: `data/cache/forecasts/<D>_raw_tweedie/`.

- Trên M5, bản sửa gần như không làm thay đổi kết quả.
- Trên VN1, RMSSE ở h = 13 vẫn kém Empirical (0,90 so với 0,64). Phần còn lại đến từ hai nguồn:
  - các lần bán sỉ đột biến mà mọi mô hình đều sai, ví dụ một chuỗi bình quân 0,5 đơn vị/tuần bán 3.700 đơn vị trong 13 tuần;
  - cách lấy trung vị = trung bình μ khi giả định phân phối chuẩn.
  - [Nhận định nhóm] Đây là đặc tính của baseline, không phải lỗi cài đặt.

## 2. RQ1–RQ2 — Kiểm định thống kê theo chuỗi

Cách làm (`code/stat_tests.py`):

- Tính SQL của từng chuỗi, cho từng mô hình.
- Kiểm định Friedman trên 8 mô hình, so hạng trung bình với Nemenyi CD (α = 0,05).
- Wilcoxon theo cặp so với LightGBM quantile, hiệu chỉnh Holm.

Friedman có p < 0,001 ở mọi dataset × nhóm × metric.

**Bảng 2.** Hạng trung bình theo SQL (1 = tốt nhất; ba mô hình đứng đầu mỗi cột).

| | M5 h = 3 (CD 0,06) | M5 h = 13 (CD 0,06) | VN1 h = 3 (CD 0,09) | VN1 h = 13 (CD 0,09) |
|---|---|---|---|---|
| 1 | lgb_quantile 3,40 | hgb_quantile 3,72 | tsb_nb 3,62 | tsb_nb 3,36 |
| 2 | hgb_quantile 3,66 | lgb_quantile 3,81 | lgb_quantile 3,68 | tsb 3,74 |
| 3 | lgb_tweedie 4,23 | lgb_tweedie 3,99 | hgb_quantile 3,73 | hgb_quantile 4,50 |

Ghi chú cho Bảng 2:

- **M5 h = 3:** LightGBM quantile tốt hơn HistGradientBoosting ở 57,3% chuỗi.
- **M5 h = 13:** HistGradientBoosting có hạng tốt hơn LightGBM quantile 0,09 (> CD), nhưng Wilcoxon p = 0,055 và nó chỉ tốt hơn ở 53% chuỗi. Hai mô hình gần như ngang nhau.
- **VN1 h = 3:** chênh lệch giữa TSB-NB và LightGBM quantile (0,06), và giữa LightGBM quantile và HistGradientBoosting (0,05), đều dưới CD.
- **VN1 h = 13:** LightGBM quantile chỉ xếp hạng 4,67, kém TSB-NB ở 69% chuỗi.

**VN1 theo nhóm** (h = 3, hạng trung bình):

| Mô hình | smooth | erratic | intermittent | lumpy |
|---|---|---|---|---|
| lgb_quantile | 3,73 | **3,03** | 4,02 | **3,30** |
| hgb_quantile | **3,68** | 3,04 | 4,12 | 3,37 |
| tsb_nb | 4,08 | 4,76 | **3,11** | 3,60 |
| tsb | 5,42 | 5,48 | 3,43 | 4,29 |

**SQL trung vị theo chuỗi** (VN1, h = 3 / h = 13):

| Mô hình | Toàn bộ | Intermittent |
|---|---|---|
| lgb_quantile | 0,152 / 0,175 | 0,133 / 0,181 |
| tsb_nb | 0,152 / 0,107 | 0,112 / 0,080 |
| tsb | 0,151 / 0,110 | 0,111 / 0,079 |

Đối chiếu với SQL trung bình ở Bảng 1 (lgb_quantile 0,336 / 0,410; tsb_nb 0,411 / 0,458):

- Trên M5, LightGBM quantile và HistGradientBoosting cũng tốt nhất theo trung vị, ở mọi nhóm và cả hai horizon.
- [Nhận định nhóm] Trên VN1, mô hình ML global **không** chính xác hơn TSB ở chuỗi rời rạc điển hình. Lợi thế của nó là **độ vững**: ít khi sai rất nặng. Điều này phù hợp với nhận xét của bài 12 rằng chưa có kiến trúc global model được thiết lập cho chuỗi rời rạc (tr. 2). Khi viết bài, cần báo cáo cả trung bình và trung vị/hạng.

### 2.1 Loss theo từng phân vị (h = 3)

Cách làm (`code/per_quantile_loss.py`, kết quả `tables/per_quantile_loss.csv`):

- Với mỗi chuỗi, tính pinball loss ở từng phân vị q, trung bình trên các origin, chia cho h · mean|Δy| như SQL.
- So sánh LightGBM quantile với TSB-NB theo nhóm, ở cả hai cửa sổ.

**VN1, nhóm intermittent:**

| q | Cửa sổ | Trung bình lgb_q / tsb_nb | Trung vị lgb_q / tsb_nb | % chuỗi lgb_q tốt hơn |
|---|---|---|---|---|
| 0,9 | chính | 0,441 / 0,492 | 0,142 / 0,122 | 29,7 |
| 0,99 | chính | 0,206 / 0,321 | 0,064 / 0,025 | 24,1 |
| 0,9 | thứ hai | 0,978 / 1,434 | 0,147 / 0,134 | 33,1 |
| 0,99 | thứ hai | 0,678 / 1,241 | 0,052 / 0,027 | 29,4 |

Ở mọi phân vị của nhóm intermittent VN1:

- LightGBM quantile chỉ tốt hơn TSB-NB ở 24–33% chuỗi (cửa sổ chính) và 29–34% chuỗi (cửa sổ thứ hai).
- Theo trung vị, lợi thế của TSB-NB **lớn nhất ở phân vị cao** (q = 0,99).
- Theo trung bình, LightGBM quantile tốt hơn ở mọi phân vị, chênh lệch cũng lớn nhất ở q = 0,99.

Các nhóm khác:

- VN1 lumpy: lgb_q tốt hơn ở 41–46% (chính) và 46–53% (thứ hai) số chuỗi.
- VN1 erratic: 60–76%.
- M5 toàn bộ: 53–64% (chính) và 51–61% (thứ hai); ở q = 0,99 chỉ khoảng 51–53%.

[Nhận định nhóm] Với chuỗi intermittent điển hình, phân vị cao của TSB-NB **không** kém, mà còn tốt hơn LightGBM quantile. Lợi thế của LightGBM quantile ở phân vị cao chỉ là lợi thế **trung bình**, đến từ việc TSB-NB thỉnh thoảng sai rất nặng. Vì vậy, hạng tốt của LightGBM quantile theo đường đánh đổi ở nhóm intermittent (mục 4–5) không thể giải thích bằng "đuôi tốt hơn ở chuỗi điển hình". Một giả thuyết **chưa kiểm chứng**: KPI cộng gộp theo đơn vị nên bị chi phối bởi các chuỗi mà TSB-NB sai nặng.

Kiểm định KPI theo chuỗi ở τ = 0,9 (`tables/stat_tests.md`) cũng cho khác biệt có ý nghĩa thống kê. Tuy vậy, các khác biệt này chủ yếu phản ánh mức phục vụ khác nhau giữa các phương pháp; ví dụ TSB Poisson có tồn kho thấp hơn LightGBM quantile ở 97% chuỗi nhưng có fill rate kém nhất. Vì vậy so sánh hiệu quả tồn kho dùng đường đánh đổi (mục 4).

## 3. RQ1 — KPI tồn kho ở kịch bản mặc định (không thanh lý)

**Bảng 3.** Fill rate, CSL, tỷ lệ hết hàng (trên tuần có nhu cầu) và tồn kho; khoảng tin cậy bootstrap 95% trong ngoặc.

| Mô hình | M5 fill | M5 CSL | M5 hết hàng | M5 tồn kho | VN1 fill | VN1 CSL | VN1 hết hàng | VN1 tồn kho |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,935 | 0,906 | 0,117 | 1,78 | 0,888 | 0,943 | 0,137 | 2,80 |
| tsb | 0,891 | 0,873 | 0,158 | **1,00** | 0,823 | 0,910 | 0,216 | **1,31** |
| tsb_nb | 0,950 | 0,929 | 0,088 | 1,65 | 0,911 | 0,948 | 0,125 | 2,40 |
| ets | 0,960 | 0,946 | 0,067 | 1,87 | 0,917 | 0,958 | 0,100 | 2,74 |
| lgb_tweedie | 0,950 | 0,931 | 0,086 | 1,58 | 0,924 | 0,961 | 0,094 | 2,57 |
| lgb_conformal | **0,967** (0,966–0,969) | **0,954** | **0,057** | 2,08 | 0,935 | 0,964 | 0,086 | 2,88 |
| hgb_quantile | 0,951 | 0,937 | 0,079 | 1,53 | 0,945 | 0,972 | 0,068 | 3,47 |
| lgb_quantile | 0,956 (0,954–0,957) | 0,942 | 0,072 | 1,58 (1,55–1,61) | **0,948** (0,943–0,953) | **0,973** | **0,066** | 3,41 (3,13–3,70) |

- Ở cùng τ = 0,9, các phương pháp **không** đạt cùng mức phục vụ, nên so sánh fill rate hoặc tồn kho riêng lẻ dễ gây hiểu lầm. Mục 4 so sánh ở **cùng fill rate**.
- CSL của VN1 cao hơn fill rate vì nhiều tuần không có nhu cầu (không thể hết hàng).

## 4. RQ1 — Đánh đổi tồn kho – fill rate

![M5 trade-off](figures/fig_tradeoff_M5.png)

![VN1 trade-off](figures/fig_tradeoff_VN1.png)

**Bảng 4.** Tồn kho (tuần nhu cầu) cần để đạt fill rate mục tiêu, toàn bộ chuỗi.

- Giá trị được nội suy tuyến tính trên τ ∈ {0,5; 0,8; 0,9; 0,95; 0,99}.
- "—" = mục tiêu nằm ngoài khoảng fill rate mà phương pháp đạt được trong lưới τ.

| Mô hình | M5 0,90 | M5 0,94 | M5 0,96 | M5 0,98 | VN1 0,90 | VN1 0,92 | VN1 0,94 | VN1 0,96 | VN1 0,98 |
|---|---|---|---|---|---|---|---|---|---|
| empirical | 1,41 | 1,88 | 2,31 | 3,14 | 3,16 | 3,73 | 4,67 | — | — |
| tsb | 1,08 | — | — | — | — | — | — | — | — |
| tsb_nb | 1,09 | 1,51 | 1,92 | 2,91 | 2,21 | 2,67 | 3,50 | 4,79 | — |
| ets | 1,20 | 1,52 | 1,87 | 2,67 | 2,38 | 2,83 | 3,54 | — | — |
| lgb_tweedie | 1,07 | 1,45 | 1,83 | — | **2,05** | **2,48** | 3,19 | — | — |
| lgb_conformal | 1,14 | 1,44 | 1,91 | 2,82 | 2,10 | 2,55 | 3,22 | 4,72 | 8,94 |
| hgb_quantile | 1,03 | 1,39 | 1,74 | 2,60 | 2,17 | 2,68 | 3,31 | 4,36 | 7,61 |
| **lgb_quantile** | **1,02** | **1,38** | **1,69** | **2,49** | 2,07 | 2,54 | **3,17** | **4,13** | **7,24** |

**Bảng 5.** Hạng theo đường đánh đổi: hạng trung bình về lượng tồn kho cần, trên các mức fill rate 0,90–0,98 (1 = ít tồn kho nhất; phương pháp không đạt một mức thì nhận hạng cuối ở mức đó).

| Mô hình | M5 all | M5 smooth | M5 erratic | M5 interm. | M5 lumpy | VN1 all | VN1 smooth | VN1 erratic | VN1 interm. | VN1 lumpy |
|---|---|---|---|---|---|---|---|---|---|---|
| empirical | 7,2 | 7,4 | 6,8 | 6,8 | 6,75 | 6,7 | 6,8 | 6,1 | 6,7 | 5,9 |
| tsb | 6,7 | 6,4 | 7,9 | 7,4 | 7,88 | 7,3 | 7,6 | 6,9 | 7,1 | 6,3 |
| tsb_nb | 5,0 | 4,8 | 5,6 | 4,8 | 5,5 | 4,8 | **2,4** | 5,3 | 3,2 | 5,2 |
| ets | 5,4 | 5,8 | 4,6 | 4,8 | 3,25 | 6,1 | 4,0 | 5,9 | 5,2 | 6,3 |
| lgb_tweedie | 4,1 | 3,4 | 4,5 | 3,8 | 4,38 | 3,3 | 3,4 | 4,3 | 4,4 | 6,3 |
| lgb_conformal | 4,6 | 5,2 | **1,6** | 5,4 | 5,0 | 3,0 | 3,0 | 3,7 | 4,8 | 2,8 |
| hgb_quantile | 2,0 | 2,0 | 3,2 | 2,0 | 2,0 | 3,4 | 5,4 | 2,6 | 3,2 | 2,2 |
| **lgb_quantile** | **1,0** | **1,0** | 1,8 | **1,0** | **1,25** | **1,4** | 3,4 | **1,2** | **1,4** | **1,0** |

**M5:**

- LightGBM quantile cần ít tồn kho nhất ở mọi mức fill rate.
- Ở fill rate 0,94, nó cần ít hơn:
  - Tweedie 4,8%;
  - conformal 4,2%;
  - TSB-NB 8,6%;
  - ETS 9,2%.
- Ở 0,96: ít hơn Tweedie 7,7%, ETS 9,6%, conformal 11,5%, TSB-NB 12,0%, HistGradientBoosting 2,9%.
- Riêng nhóm erratic, conformal xếp tốt nhất (hạng 1,6).

**VN1:**

- Ở fill rate 0,90–0,92, LightGBM-Tweedie + safety stock chuẩn cần ít tồn kho nhất, nhưng chênh với LightGBM quantile nhỏ: 2,05 so với 2,07 ở 0,90; 2,48 so với 2,54 ở 0,92.
- Từ 0,94 trở lên LightGBM quantile tốt nhất.
- Tweedie không vượt được fill rate 0,952 ngay cả với τ = 0,99. [Nhận định nhóm] Đuôi của phân phối chuẩn quá mỏng cho dữ liệu rời rạc.
- Ở fill rate 0,96–0,98, chỉ các mô hình có đuôi phân phối được học từ dữ liệu (quantile, conformal) hoặc TSB-NB (đến 0,96) đạt được.
- **Lưu ý:** kết quả VN1 trong mục này **không lặp lại** ở cửa sổ kiểm thử thứ hai, nơi TSB-NB cần ít tồn kho nhất ở fill rate 0,90–0,94 (mục 10).

## 5. RQ2 — Theo nhóm nhu cầu

**Bảng 6.** SQL trung bình (h = 3) theo nhóm.

| Mô hình | M5 smooth | M5 erratic | M5 interm. | M5 lumpy | VN1 smooth | VN1 erratic | VN1 interm. | VN1 lumpy |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,208 | 0,230 | 0,556 | 0,384 | 0,437 | 0,448 | 0,514 | 0,669 |
| tsb | 0,196 | 0,215 | 0,425 | 0,309 | 0,376 | 0,428 | 0,459 | 0,533 |
| tsb_nb | 0,172 | 0,189 | 0,381 | 0,270 | 0,314 | 0,353 | 0,443 | 0,465 |
| ets | 0,168 | 0,178 | 0,376 | 0,261 | 0,319 | 0,350 | 0,474 | 0,490 |
| lgb_tweedie | 0,165 | 0,176 | 0,332 | 0,253 | 0,296 | 0,326 | 0,510 | 0,479 |
| lgb_conformal | 0,166 | 0,172 | 0,338 | 0,265 | 0,285 | 0,301 | 0,473 | 0,428 |
| hgb_quantile | 0,157 | 0,162 | 0,300 | 0,236 | 0,262 | 0,260 | 0,387 | 0,349 |
| **lgb_quantile** | **0,155** | **0,160** | **0,295** | **0,232** | **0,260** | **0,258** | **0,384** | **0,345** |

**Tồn kho cần, VN1, các nhóm có kết luận khác M5** (`tables/comparison_full.md`):

| Nhóm | fill 0,90 | fill 0,92 | fill 0,94 | fill 0,96 |
|---|---|---|---|---|
| smooth | **tsb_nb 1,19**; ets, lgb_quantile, tweedie 1,28 | **tsb_nb 1,36**; ets, conformal 1,42 | **tsb_nb 1,67**; tweedie 1,73; ets 1,74 | conformal 2,22; tweedie 2,29; tsb_nb 2,32 |
| intermittent | **tsb_nb 2,12**; lgb_quantile 2,47 | **tsb_nb 2,64**; lgb_quantile 2,90 | **lgb_quantile 3,64**; tsb_nb 3,68 | **lgb_quantile 4,88**; hgb 5,10 (TSB-NB không đạt) |

Nhận xét:

- **M5:** mô hình phân vị trực tiếp có SQL thấp nhất và cần ít tồn kho nhất ở cả 4 nhóm, trừ nhóm erratic, nơi conformal ngang bằng.
- **VN1:**
  - TSB-NB hiệu quả nhất ở nhóm smooth và ở mức phục vụ trung bình của nhóm intermittent.
  - LightGBM quantile hiệu quả nhất ở erratic, lumpy, và ở mức phục vụ cao của mọi nhóm.
  - Ở nhóm lumpy, chỉ 5 phương pháp đạt fill rate 0,90. LightGBM quantile cần 6,06 tuần tồn kho, TSB-NB 8,99 tuần, Empirical 12,8 tuần.
- [Nhận định nhóm] Kết quả ủng hộ việc **chọn phương pháp theo nhóm nhu cầu và theo mức phục vụ mục tiêu** trên dữ liệu thương mại điện tử rời rạc.

## 6. Độ nhất quán giữa M5 và VN1

**Bảng 7.** Spearman ρ giữa thứ hạng của 8 phương pháp trên M5 và VN1 (p theo scipy, xấp xỉ t).

| Xếp hạng theo | toàn bộ | smooth | erratic | intermittent | lumpy |
|---|---|---|---|---|---|
| Fill rate ở τ = 0,9 (không thanh lý) | 0,69 (p 0,058) | 0,60 (0,12) | 0,19 (0,65) | 0,83 (0,010) | 0,69 (0,058) |
| **Đường đánh đổi** (Bảng 5) | **0,88 (0,004)** | 0,48 (0,23) | **0,90 (0,002)** | **0,90 (0,002)** | 0,54 (0,17) |

- Xếp hạng theo đường đánh đổi nhất quán hơn rõ ràng ở toàn bộ chuỗi và ở nhóm erratic.
- [Nhận định nhóm] Phần lớn khác biệt giữa hai dataset khi so ở một τ đến từ việc mỗi phương pháp hiệu chỉnh phân vị khác nhau, không phải từ hiệu quả tồn kho thực sự.
- Nhóm smooth và lumpy kém nhất quán, vì ở VN1 TSB-NB (smooth) và conformal (lumpy) xếp cao hơn hẳn so với ở M5.
- Thứ hạng **SQL** cũng nhất quán: ở h = 3, LightGBM quantile đứng đầu và Empirical đứng cuối ở cả hai dataset.
- **Lưu ý:** ở cửa sổ thứ hai, Spearman theo đường đánh đổi chỉ còn 0,50 (p = 0,21), còn theo fill rate là 0,93. Vì vậy nhận định "xếp theo đường đánh đổi nhất quán hơn" **không vững**; chỉ nhóm intermittent nhất quán ở cả hai cửa sổ (mục 10).

## 7. RQ3 — Thanh lý

**Bảng 8.** Kịch bản mặc định, toàn bộ chuỗi.

- Δfill = thay đổi fill rate so với không thanh lý, tính bằng điểm %.
- % TL = đơn vị thanh lý / nhu cầu.
- dead13 = thanh lý toàn bộ và ngừng đặt hàng khi chuỗi không bán trong 13 tuần (mục 7.1).

| Mô hình | Dataset | Tồn kho (không TL) | Quantile: tồn kho / % TL / Δfill | Fixed: tồn kho / % TL / Δfill | dead13: tồn kho / % TL / Δfill |
|---|---|---|---|---|---|
| lgb_quantile | M5 | 1,581 | 1,579 / 0,02 / 0,00 | 1,545 / 0,79 / −0,29 | 1,542 / 0,67 / −0,66 |
| tsb_nb | M5 | 1,650 | 1,591 / 1,07 / −0,48 | 1,644 / 0,17 / −0,09 | 1,625 / 0,60 / −0,37 |
| lgb_quantile | VN1 | 3,405 | 3,261 / 1,18 / −0,02 | 3,198 / 2,76 / −0,67 | 3,269 / 1,21 / −0,09 |
| hgb_quantile | VN1 | 3,475 | 3,066 / 3,66 / −0,10 | 3,245 / 2,95 / −0,64 | 3,337 / 1,25 / −0,09 |
| lgb_tweedie | VN1 | 2,567 | 2,543 / 0,23 / −0,02 | 2,480 / 1,84 / −0,22 | 2,436 / 1,00 / −0,10 |
| lgb_conformal | VN1 | 2,875 | 2,857 / 0,18 / −0,01 | 2,770 / 2,02 / −0,27 | 2,732 / 0,90 / −0,11 |
| tsb_nb | VN1 | 2,401 | 2,246 / 2,28 / −0,45 | 2,370 / 0,54 / −0,05 | 2,339 / 0,78 / −0,06 |

**Quy tắc phân vị:**

- M5: gần như không kích hoạt với các mô hình ML, ETS và Empirical (≤ 0,02% nhu cầu). Nó chỉ kích hoạt với TSB và TSB-NB (khoảng 1,1%), làm mất khoảng 0,5 điểm % fill rate.
- VN1: với các mô hình ML, giảm tồn kho 0,6–12%, mất ≤ 0,1 điểm % fill rate, chạm 2–12% số chuỗi.

**Quy tắc cố định:** trên VN1, với 4 mô hình ML, mất 0,2–0,7 điểm % fill rate và chạm 42–51% số chuỗi (với các mô hình thống kê: mất 0,02–0,19 điểm %, chạm 16–42% số chuỗi).

**Nhóm lumpy, VN1, LightGBM quantile:**

| Chính sách | % thanh lý | Fill rate | Tồn kho |
|---|---|---|---|
| Không thanh lý | 0 | 0,928 | 7,52 |
| Quantile | 6,4 | 0,926 | 6,73 (−10,5%) |
| Fixed | 14,6 | 0,877 | 6,40 (−14,9%) |
| dead13 | 4,5 | 0,923 | 7,02 (−6,6%) |

### 7.1 Quy tắc dead-stock (việc 5)

- **Quy tắc:** chuỗi không có lần bán nào trong N tuần trước tuần quyết định (N = 13 hoặc 26) → thanh lý toàn bộ tồn hiện có và ngừng đặt hàng cho đến khi bán lại (`policy.deadstock`).
- **Vì sao thêm:** 28,2% chuỗi VN1 không có nhu cầu trong 22 tuần KPI, nhưng quy tắc phân vị chỉ chạm 5,4% số chuỗi (LightGBM quantile).

Kết quả với LightGBM quantile (toàn bộ / intermittent):

| | VN1 dead13 | VN1 dead26 | M5 dead13 |
|---|---|---|---|
| % chuỗi bị thanh lý | 19,3 | 11,2 | 6,2 |
| Tồn kho so với không thanh lý | −4,0% / −19,4% | −1,3% / −9,9% | −2,5% / −7,1% |
| Fill rate | 0,948 → 0,947 / 0,950 → 0,942 | 0,948 → 0,948 / 0,950 → 0,947 | 0,956 → 0,949 / 0,944 → 0,927 |
| Tỷ lệ tuần hết hàng (trên tuần có nhu cầu) | 0,066 → 0,081 / 0,081 → 0,135 | 0,066 → 0,071 / 0,081 → 0,101 | 0,072 → 0,081 / 0,072 → 0,089 |

- Trên VN1, dead13 giảm tồn kho nhóm intermittent mạnh hơn quy tắc phân vị (−19,4% so với −5,9%). Đổi lại, tỷ lệ tuần hết hàng của nhóm này tăng 68% (0,081 → 0,135).
- Trên M5, sản phẩm "ngủ" 13 tuần thường bán lại, nên dead13 làm mất 0,66 điểm % fill rate.

### 7.2 Ngưỡng giá thu hồi hòa vốn

**Bảng 9.** s\* (chi phí lưu kho 25%/năm, biên lợi nhuận 50%); cận trên (a) / cận dưới (b); `tables/breakeven_*.csv`.

| Mô hình | M5 quantile | M5 fixed | M5 dead13 | VN1 quantile | VN1 fixed | VN1 dead13 |
|---|---|---|---|---|---|---|
| lgb_quantile | 1,00 / 1,00 (*) | 1,14 / 1,16 | 1,57 / 1,62 | 0,95 / 0,78 | 1,09 / 1,15 | 1,09 / 12,4 (**) |
| hgb_quantile | 0,93 / — (*) | 1,14 / 1,16 | 1,55 / 1,60 | 0,96 / 0,83 | 1,07 / 1,12 | 1,08 / 4,3 (**) |
| lgb_tweedie | 0,94 / 0,86 (*) | 1,14 / 1,15 | 1,55 / 1,60 | 0,98 / 0,97 | 1,04 / 1,06 | 1,15 / 3,2 (**) |
| lgb_conformal | 1,28 / 1,31 (*) | 1,13 / 1,14 | 1,61 / 1,66 | 0,98 / 0,84 | 1,04 / 1,05 | 1,26 / — (**) |

Ghi chú cho Bảng 9:

- (\*) Dưới 1.200 đơn vị bị thanh lý trên toàn M5, nên s\* không ổn định.
- (\*\*) Cận (b) không ổn định hoặc không xác định. Lý do: gần như toàn bộ hàng bị thanh lý lẽ ra vẫn còn trong kho ở cuối kỳ, nên mẫu số X + ΔVịTríCuối ≈ 0.
  - Khi đó thanh lý chỉ là "bán thanh lý sớm hơn". Lợi hay hại phụ thuộc vào chênh lệch giữa chi phí lưu kho tiết kiệm được và lợi nhuận mất do hết hàng.
  - Ở cả 4 mô hình, phần lợi nhuận mất lớn hơn: tử số dương, nên s\* rất lớn hoặc không xác định.

**Khoảng s\* trên toàn lưới** (chi phí lưu kho 10–40%/năm × biên lợi nhuận 30–100%), cận trên, 4 mô hình ML:

| Quy tắc | VN1 | M5 |
|---|---|---|
| quantile | 0,91–1,04 | — (*) |
| fixed | 1,00–1,22 | 1,06–1,32 |
| dead13 | 1,03–1,37 | 1,35–2,08 |
| dead26 | 1,16–1,47 | 1,76–3,12 |

**Bảng 10.** Phân rã mỗi đơn vị thanh lý: so với không thanh lý, trên toàn bộ 26 tuần, 4 mô hình ML.

| Quy tắc | Phải đặt lại | Mất doanh số | Lẽ ra còn tồn ở cuối kỳ |
|---|---|---|---|
| VN1, quantile | 0,04–0,50 | 0,02–0,06 | 0,44–0,90 |
| VN1, fixed | 0,35–0,63 | 0,12–0,23 | 0,24–0,42 |
| VN1, dead13 | 0,01–0,12 | 0,08–0,13 | 0,93–1,05 |
| M5, fixed | 0,57–0,63 | 0,30–0,32 | 0,07–0,11 |
| M5, dead13 | 0,07–0,22 | 0,86–0,97 | 0,07–0,08 |

[Nhận định nhóm] Cách đọc Bảng 10:

- **Quy tắc cố định** thanh lý nhiều hàng mà sau đó phải đặt lại hoặc làm mất doanh số, nên s\* > 1.
- **Quy tắc dead-stock trên VN1** nhắm đúng hàng thực sự không bán được (93–105% số hàng thanh lý lẽ ra vẫn còn ở cuối kỳ). Tuy vậy, cứ 100 đơn vị thanh lý thì mất khoảng 8–13 đơn vị doanh số. Trong 26 tuần, chi phí lưu kho tiết kiệm được không bù được phần này.
- **Quy tắc dead-stock trên M5** sai: hầu hết sản phẩm "ngủ" 13 tuần bán lại sau đó.
- **Quy tắc phân vị** có s\* thấp nhất, nhưng vẫn cần giá thu hồi gần bằng giá vốn.
- Lợi ích của thanh lý (tránh hàng lỗi thời, giải phóng chỗ chứa) cần tầm nhìn dài hơn 26 tuần, hoặc dữ liệu về sản phẩm ngừng kinh doanh, mới đánh giá được.

**Ở cấp chuỗi** (VN1, LightGBM quantile, không thanh lý; `tables/series_inventory_VN1.csv`):

- trung vị số tuần tồn kho là 6,9; phân vị 90 là 42 tuần;
- trên M5, các con số tương ứng là 2,0 và 6,6 tuần.

## 8. RQ4 — Độ nhạy theo kịch bản

**τ** (LightGBM quantile; fill / tồn kho):

| | τ = 0,5 | τ = 0,8 | τ = 0,9 | τ = 0,95 | τ = 0,99 |
|---|---|---|---|---|---|
| M5 | 0,816 / 0,59 | 0,921 / 1,13 | 0,956 / 1,58 | 0,974 / 2,05 | 0,992 / 3,32 |
| VN1 | 0,797 / 0,97 | 0,907 / 2,16 | 0,948 / 3,41 | 0,971 / 4,77 | 0,992 / 10,37 |

- Trên VN1, đẩy fill rate từ 0,971 lên 0,992 làm tồn kho tăng hơn gấp đôi (4,77 → 10,37 tuần).
- TSB Poisson gần như không phản ứng với τ trên VN1 (fill 0,793 → 0,843 khi τ đi từ 0,5 đến 0,99).

**Lead time L** (chỉ VN1):

| Mô hình | fill L=1 | fill L=2 | fill L=4 | tồn kho L=1 | tồn kho L=2 | tồn kho L=4 |
|---|---|---|---|---|---|---|
| lgb_quantile | 0,944 | 0,948 | 0,943 | 2,07 | 3,41 | 6,01 |
| lgb_tweedie | 0,929 | 0,924 | 0,915 | 1,72 | 2,57 | 4,40 |
| lgb_conformal | 0,937 | 0,935 | 0,930 | 1,89 | 2,88 | 4,98 |
| tsb_nb | 0,919 | 0,911 | 0,889 | 1,76 | 2,40 | 3,61 |
| ets | 0,918 | 0,917 | 0,908 | 1,83 | 2,74 | 4,70 |

- Thứ hạng fill rate gần như không đổi theo L: Spearman ρ giữa L = 2 và L = 1 là 0,96; giữa L = 2 và L = 4 là 1,00 (7 phương pháp).
- Tồn kho tăng gần tỷ lệ với L + R.
- TSB-NB mất fill rate nhanh nhất khi L tăng: −2,2 điểm % từ L = 2 lên L = 4.

**Tham số thanh lý** (VN1, LightGBM quantile):

- H = 8 / 13 / 26 → % thanh lý 3,1 / 1,2 / 0,2; fill rate 0,946 / 0,948 / 0,948.
- q_L = 0,9 / 0,95 / 0,99 → % thanh lý 2,8 / 1,2 / 0,2.
- Quy tắc cố định với k = 13 / 26 / 52 → % thanh lý 7,1 / 2,8 / 1,2; fill rate 0,929 / 0,941 / 0,946.
- Ở L = 4: quy tắc phân vị thanh lý 5,0% và mất 0,1 điểm % fill rate; quy tắc cố định thanh lý 8,6% và mất 1,9 điểm %.
- [Nhận định nhóm] Quy tắc phân vị an toàn hơn trong toàn bộ lưới.

## 9. Kiểm tra giả thuyết (`05_methodology/evaluation_metrics.md` mục 7)

| Giả thuyết | Kết quả | Mức độ |
|---|---|---|
| H1: LightGBM quantile có SQL thấp nhất | SQL trung bình: đúng ở mọi dataset, horizon và nhóm. Theo chuỗi: đúng ở M5 h = 3; ngang HistGradientBoosting ở M5 h = 13; trên VN1 ngang TSB-NB (h = 3) hoặc kém TSB/TSB-NB (h = 13) | Ủng hộ ở M5; một phần ở VN1 |
| H2: Phân vị trực tiếp cần ít tồn kho hơn dự báo điểm + safety stock | M5: đúng ở cả hai cửa sổ (−4,8% / −6,3% ở 0,94). VN1: cửa sổ chính ngang ở 0,90–0,92 và đúng từ 0,94; cửa sổ thứ hai ngang ở 0,90–0,92 và Tweedie cần ít tồn kho hơn ở 0,94–0,96 | Ủng hộ ở M5; không vững ở VN1 |
| H3: ML có lợi rõ ở smooth/erratic; TSB đủ tốt ở intermittent | M5: ML tốt nhất ở mọi nhóm. VN1 (vững qua hai cửa sổ): **ngược với giả thuyết**: TSB-NB tốt nhất ở smooth, LightGBM quantile tốt nhất ở intermittent và lumpy (đường đánh đổi); theo SQL từng chuỗi, TSB-NB tốt ở intermittent | Không ủng hộ dạng ban đầu; kết luận phụ thuộc dataset |
| H4: Thanh lý theo phân vị giảm tồn kho mà mất ít fill rate hơn quy tắc cố định | Đúng trên VN1, rõ nhất ở lumpy; trên M5 hầu như không kích hoạt. Về kinh tế, s\* ≈ 0,91–1,04 | Ủng hộ về KPI; lợi ích kinh tế chưa chứng minh |
| (bổ sung) Dead-stock tốt hơn quy tắc phân vị cho hàng tồn chết | VN1: giảm tồn kho intermittent nhiều hơn nhưng tăng tuần hết hàng 68%; M5: làm mất fill rate. s\* > 1 | Không ủng hộ trong cửa sổ 26 tuần |

## 10. Độ vững: cửa sổ kiểm thử thứ hai (việc 2)

**Cách làm:**

- Bỏ 26 tuần cuối của panel, rồi chạy lại toàn bộ (8 mô hình dự báo lại từ đầu) trên 26 tuần liền trước (`run_pipeline.py --offset 26`).
- Cửa sổ kiểm thử:
  - M5: 2015-05-23 → 2015-11-14, 29.917 chuỗi;
  - VN1: 2023-04-10 → 2023-10-02, 11.442 chuỗi. Cửa sổ này nằm hoàn toàn trong Phase 0, nên không dùng đáp án chính thức.
- Chạy kịch bản mặc định + lưới τ và 5 chính sách thanh lý; **không** chạy lưới L, H và ngưỡng hòa vốn cho cửa sổ này.
- Nguồn: `tables/comparison_w26.md`, `tables/stat_tests_w26.md`, `figures/fig_tradeoff_M5_w26.png`, `figures/fig_tradeoff_VN1_w26.png`.

**Bảng 11.** So sánh hai cửa sổ.

| Kết quả | Cửa sổ chính | Cửa sổ thứ hai | Vững? |
|---|---|---|---|
| SQL trung bình h = 3, LightGBM quantile (M5 / VN1) | 0,208 / 0,336, tốt nhất | 0,215 / 0,539, tốt nhất | ✅ |
| Hạng theo chuỗi, M5 h = 3: lgb_quantile / hgb_quantile | 3,40 / 3,66 | 3,50 / 3,72 | ✅ |
| Hạng theo chuỗi, M5 h = 13: lgb_quantile / hgb_quantile | 3,81 / 3,72 | 3,80 / 3,82 | ✅ ngang nhau |
| Hạng theo chuỗi, VN1 h = 3, ba mô hình đầu | tsb_nb 3,62; lgb_quantile 3,68; hgb 3,73 | lgb_quantile 3,62; hgb 3,68; tsb_nb 3,72 (chênh < CD 0,098) | ✅ ngang nhau |
| Hạng theo chuỗi, VN1 h = 13, đứng đầu | tsb_nb 3,36 | tsb_nb 3,45 | ✅ |
| Hạng theo đường đánh đổi, M5: lgb_quantile / hgb_quantile | 1,0 / 2,0 | 1,2 / 1,8 | ✅ |
| Hạng theo đường đánh đổi, VN1 (toàn bộ) | **lgb_quantile 1,4**; conformal 3,0; tweedie 3,3; tsb_nb 4,8 | **tsb_nb 1,8**; conformal 2,0; tweedie 3,5; lgb_quantile 3,8 | ❌ |
| Đứng đầu đường đánh đổi theo nhóm, VN1 | smooth tsb_nb; erratic lgb_quantile; intermittent lgb_quantile; lumpy lgb_quantile | smooth tsb_nb; erratic conformal; intermittent lgb_quantile; lumpy lgb_quantile | ✅ trừ erratic |
| Spearman M5–VN1 theo đường đánh đổi (toàn bộ / intermittent) | 0,88 / 0,90 | 0,50 (p 0,21) / 0,95 | ❌ toàn bộ; ✅ intermittent |
| Spearman M5–VN1 theo fill rate ở τ = 0,9 (toàn bộ / intermittent) | 0,69 / 0,83 | 0,93 / 0,93 | Không ổn định |
| Quy tắc phân vị, VN1, lgb_quantile: tồn kho / Δfill | −4,3% / −0,02 | −1,7% / −0,02 | ✅ ít mất fill; mức giảm nhỏ hơn |
| dead13, VN1 intermittent: tỷ lệ tuần hết hàng | 0,081 → 0,135 | 0,087 → 0,140 | ✅ |
| dead13, M5, lgb_quantile: Δfill | −0,66 | −0,46 | ✅ |

**Tồn kho cần để đạt fill rate, cửa sổ thứ hai** (toàn bộ chuỗi):

| | fill 0,92 | fill 0,94 | fill 0,96 |
|---|---|---|---|
| M5 | lgb_quantile 1,24; hgb 1,25; tsb_nb, tweedie 1,31 | lgb_quantile 1,49; hgb 1,51; tweedie 1,59 | lgb_quantile 1,80; hgb 1,85; tweedie 1,98 |
| VN1 | **tsb_nb 1,22**; conformal 1,30; tweedie 1,37; lgb_quantile 1,38 | **tsb_nb 1,63**; tweedie 1,65; conformal 1,71; lgb_quantile 1,79 | **tweedie 2,13**; conformal 2,23; tsb_nb 2,27; lgb_quantile 2,33 |

**Kết luận về độ vững:**

1. **M5 vững.** LightGBM quantile chính xác nhất và cần ít tồn kho nhất ở cả hai cửa sổ. Ở fill rate 0,94–0,96, nó cần ít hơn Tweedie, TSB-NB, ETS và conformal 4–13% (tùy cửa sổ và mức fill); HistGradientBoosting bám sát.
2. **VN1 — độ chính xác vững.** LightGBM quantile có SQL trung bình thấp nhất. Nhưng xét từng chuỗi, nó chỉ ngang TSB-NB (h = 3) và kém TSB-NB (h = 13) ở cả hai cửa sổ.
3. **VN1 — hiệu quả tồn kho không vững.**
   - Ở cửa sổ chính, TSB-NB cần nhiều tồn kho hơn LightGBM quantile 5–10% (fill rate 0,92–0,94).
   - Ở cửa sổ thứ hai thì ngược lại: LightGBM quantile cần nhiều hơn 10–13%.
   - [Nhận định nhóm] Trên VN1, chưa có phương pháp nào hiệu quả nhất một cách ổn định; SQL tốt hơn **không** chắc chắn chuyển thành ít tồn kho hơn. Nguyên nhân khác nhau giữa hai cửa sổ chưa được kiểm chứng. Hai giả thuyết:
     - khác biệt mùa vụ;
     - Phase 2 không có giá (cửa sổ chính dùng giá điền tiếp từ tuần trước).
4. **Theo nhóm, VN1:** hai kết luận giữ ở cả hai cửa sổ:
   - TSB-NB hiệu quả nhất ở nhóm smooth;
   - LightGBM quantile hiệu quả nhất ở intermittent và lumpy.
5. **Thanh lý:**
   - Quy tắc phân vị luôn mất rất ít fill rate.
   - Dead13 luôn làm tăng mạnh số tuần hết hàng của nhóm intermittent (+61% đến +68%), và luôn làm mất fill rate trên M5.
6. **Độ nhất quán giữa dataset:** chỉ nhóm intermittent có thứ hạng nhất quán ở cả hai cửa sổ và cả hai cách xếp hạng (ρ = 0,83–0,95). Nhận định "xếp theo đường đánh đổi nhất quán hơn" ở mục 6 **không lặp lại** ở cửa sổ thứ hai.

**Hệ quả khi viết bài** [Nhận định nhóm]:

- Kết luận chính nên dựa trên những điểm vững qua hai cửa sổ: M5; kết quả theo chuỗi của VN1; kết quả theo nhóm smooth / intermittent / lumpy; và các quy tắc thanh lý.
- Kết quả hiệu quả tồn kho tổng thể của VN1 phải trình bày là **phụ thuộc giai đoạn**.

Thời gian dự báo của cửa sổ thứ hai (VN1, h = 3 / 13, `code/outputs/logs/run_VN1_w26.log`):

- Empirical 28 / 17 s; TSB 14 / 13 s; ETS 1 / 1 s;
- TSB-NB 29 / 26 s; Tweedie 12 / 11 s; conformal 11 / 13 s;
- HistGradientBoosting 77 / 129 s; LightGBM quantile 264 / 109 s.

### 10.1 Cửa sổ kiểm thử thứ ba (w52)

**Cách làm:** như mục 10, nhưng bỏ 52 tuần cuối (`run_pipeline.py --offset 52`, `code/outputs/logs/rerun_w52.sh`). Cửa sổ kiểm thử:

- M5: 2014-11-22 → 2015-05-16, 28.824 chuỗi;
- VN1: 2022-10-10 → 2023-04-03, 9.383 chuỗi (nằm trong Phase 0).

Nguồn: `code/outputs/comparison_w52.md`, `stat_tests_w52.md`, `equal_fill_ci_w52.md`, `fig_tradeoff_*_w52.png`.

**Bảng 12.** Các kết quả chính qua ba cửa sổ (chính / thứ hai / thứ ba).

| Kết quả | Chính | Thứ hai | Thứ ba | Vững qua 3 cửa sổ? |
|---|---|---|---|---|
| SQL trung bình h = 3, M5: tốt nhất | lgb_quantile 0,208 | lgb_quantile 0,215 | lgb_quantile 0,222 | ✅ |
| Hạng theo chuỗi M5 h = 3: lgb_quantile / hgb_quantile | 3,40 / 3,66 | 3,50 / 3,72 | 3,48 / 3,62 | ✅ |
| Hạng theo chuỗi VN1 h = 3, ba mô hình đầu (chênh < CD) | tsb_nb, lgb_q, hgb | lgb_q, hgb, tsb_nb | lgb_q 3,60; tsb_nb 3,65; hgb 3,66 (CD 0,108) | ✅ ngang nhau |
| Hạng theo chuỗi VN1 h = 13: đứng đầu | tsb_nb 3,36 | tsb_nb 3,45 | tsb_nb 3,75 | ✅ |
| Trung vị SQL theo chuỗi VN1 h = 3, lgb_quantile / tsb_nb | 0,152 / 0,152 | 0,140 / 0,150 | 0,184 / 0,186 | ✅ ngang nhau |
| Hạng theo đường đánh đổi, M5: lgb_quantile / hgb_quantile | 1,0 / 2,0 | 1,2 / 1,8 | 1,0 / 2,0 | ✅ |
| Hạng theo đường đánh đổi, VN1 (toàn bộ): đứng đầu | lgb_quantile 1,4 | tsb_nb 1,8 (lgb_q 3,8) | lgb_quantile 1,25 (conformal 2,25; hgb 2,5; tsb_nb 5,5) | ❌ (lgb_q 2/3 cửa sổ) |
| VN1 smooth: đứng đầu | tsb_nb 2,4 | tsb_nb 2,0 | conformal 1,8 (tsb_nb 2,6; lgb_q 3,6) | ❌ |
| VN1 intermittent: đứng đầu | lgb_quantile 1,4 | lgb_quantile 2,0 | không xác định (\*) | ✅ ở 2 cửa sổ có số liệu |
| VN1 lumpy: đứng đầu | lgb_quantile 1,0 | lgb_quantile 2,0 | lgb_quantile 1,33 | ✅ |
| VN1 erratic: đứng đầu | lgb_quantile 1,2 | conformal 2,2 | lgb_quantile 1,0 | ❌ |
| VN1 intermittent, % chuỗi lgb_q có pinball loss thấp hơn tsb_nb (mọi q) | 24–33% | 29–34% | 30–34% | ✅ |
| Quy tắc phân vị, VN1, lgb_q: tồn kho / Δfill | −4,3% / −0,02 | −1,7% / −0,02 | −7,4% / −0,02 | ✅ |
| dead13, VN1 intermittent: thay đổi tỷ lệ tuần hết hàng | +68% | +61% | +43% | ✅ luôn tăng |
| dead13, M5, lgb_q: Δfill (điểm %) | −0,66 | −0,46 | −0,54 | ✅ |
| Spearman M5–VN1, hạng đường đánh đổi: toàn bộ | 0,88 | 0,50 | 0,67 | ❌ |
| Spearman M5–VN1, fill rate ở τ = 0,9: intermittent | 0,83 | 0,93 | 0,83 | ✅ |

(\*) Ở cửa sổ thứ ba, nhóm intermittent của VN1 không phương pháp nào đạt fill rate 0,90 trong lưới τ (lgb_quantile chỉ đạt 0,84 ở τ = 0,9), nên không xếp hạng được theo đường đánh đổi.

**Nhận xét:**

- **M5 vững qua cả ba cửa sổ.**
- **VN1 tổng thể:** lgb_quantile hiệu quả nhất ở 2/3 cửa sổ; TSB-NB ở cửa sổ thứ hai. Kết luận "phụ thuộc giai đoạn" vẫn đúng, nhưng nghiêng về lgb_quantile.
- **VN1 theo nhóm:** chỉ còn **lumpy** (và intermittent ở hai cửa sổ có số liệu) là vững cho lgb_quantile. Nhận định "TSB-NB tốt nhất ở nhóm smooth" của mục 10 **không lặp lại** ở cửa sổ thứ ba.
- **SQL trung bình của VN1 không ổn định:** 0,336 / 0,539 / 2,008 cho lgb_quantile, trong khi trung vị gần như không đổi (0,152 / 0,140 / 0,184). Ở cửa sổ thứ ba, 10 chuỗi tệ nhất chiếm 29% tổng SQL của lgb_quantile (giá trị lớn nhất 895); bỏ 1% chuỗi tệ nhất thì trung bình còn 0,550 (`data/cache/series_metrics_VN1_w52.parquet`). [Nhận định nhóm] Trên VN1, SQL trung bình bị chi phối bởi một số ít chuỗi có quy mô naive rất nhỏ; cần báo cáo trung vị và hạng theo chuỗi.
- Dead13 luôn làm tăng tỷ lệ tuần hết hàng của nhóm intermittent VN1 (+43% đến +68%) và luôn làm mất fill rate trên M5.

### 10.2 Khoảng tin cậy bootstrap cho tồn kho ở cùng fill rate

Cách làm (`code/equal_fill_ci.py`): với mỗi lần lấy mẫu lại chuỗi (B = 200, seed 2026), dựng lại đường đánh đổi của từng phương pháp và nội suy lượng tồn kho cần để đạt fill rate mục tiêu như mục 4. Chênh lệch tương đối Δ = I_phương pháp / I_lgb_quantile − 1 (dương = lgb_quantile cần ít tồn kho hơn). Khoảng tin cậy chỉ báo cáo khi mục tiêu đạt được trong ≥ 95% số lần lấy mẫu. Đây là kiểm định còn thiếu ở mục 11 (hạn chế 1).

**Bảng 13.** Toàn bộ chuỗi, fill rate 0,94: hạng theo đường đánh đổi của lgb_quantile [KTC 95%], xác suất lgb_quantile có hạng tốt nhất P(best), và Δ của từng baseline [KTC 95%]. "Giá trị" = KPI trọng số theo giá bán (mục 10.3). Nguồn: `code/outputs/equal_fill_ci*.csv`.

| Dataset | Cửa sổ | KPI | Hạng lgb_q | P(best) | hgb_quantile | lgb_tweedie | lgb_conformal | tsb_nb | ets |
|---|---|---|---|---|---|---|---|---|---|
| M5 | chính | đơn vị | 1,0 [1,0; 1,0] | 1,00 | +1,2% [+0,9; +1,6] | +5,1% [+4,4; +5,9] | +4,5% [+3,2; +5,8] | +10,0% [+9,1; +11,0] | +10,6% [+9,8; +11,5] |
| VN1 | chính | đơn vị | 1,4 [1,0; 2,6] | 0,93 | +4,5% [+2,9; +6,7] | +0,9% [-7,5; +9,9] | +1,7% [-6,3; +8,7] | +10,5% [-0,5; +19,8] | +12,0% [+3,8; +19,7] |
| M5 | chính | giá trị | 1,0 [1,0; 1,0] | 1,00 | +1,2% [+0,9; +1,6] | +4,8% [+4,1; +5,4] | +6,6% [+5,3; +7,8] | +7,7% [+6,9; +8,5] | +9,7% [+8,9; +10,5] |
| VN1 | chính | giá trị | 1,8 [1,0; 2,4] | 0,98 | +5,0% [+2,4; +9,6] | -1,4% [-18,0; +13,0] | +7,2% [-0,0; +19,1] | +15,3% [-1,2; +27,7] | +17,1% [+0,3; +30,1] |
| M5 | thứ hai | đơn vị | 1,2 [1,0; 1,4] | 1,00 | +1,4% [+1,2; +1,7] | +6,8% [+6,2; +7,6] | +8,2% [+6,8; +9,3] | +7,5% [+6,7; +8,3] | +8,0% [+7,1; +8,9] |
| VN1 | thứ hai | đơn vị | 3,8 [2,8; 4,8] | 0,00 | -1,2% [-2,5; +0,2] | -7,7% [-11,8; -3,8] | -4,1% [-7,3; -0,9] | -8,8% [-12,8; -4,9] | -0,4% [-5,7; +4,2] |
| M5 | thứ hai | giá trị | 1,0 [1,0; 1,4] | 1,00 | +1,2% [+1,0; +1,4] | +5,3% [+4,7; +6,1] | +6,7% [+5,4; +8,0] | +5,7% [+5,0; +6,4] | +7,2% [+6,4; +8,0] |
| VN1 | thứ hai | giá trị | 4,8 [3,6; 5,2] | 0,00 | -1,7% [-3,1; +0,5] | -12,5% [-26,2; -6,1] | -9,7% [-18,4; -6,5] | -13,0% [-23,0; -7,2] | -2,6% [-16,1; +3,7] |
| M5 | thứ ba | đơn vị | 1,0 [1,0; 1,2] | 1,00 | +0,2% [-0,2; +0,5] | +3,3% [+2,7; +4,0] | +7,5% [+6,3; +8,4] | +4,9% [+4,2; +5,7] | +5,9% [+5,0; +6,6] |
| VN1 | thứ ba | đơn vị | 1,2 [1,0; 2,0] | 0,95 | +1,3% [-0,7; +3,5] | — | +11,5% [+1,6; +116,5] | — | — |
| M5 | thứ ba | giá trị | 1,0 [1,0; 1,2] | 1,00 | +0,3% [-0,0; +0,5] | +4,4% [+3,7; +5,2] | +9,2% [+7,5; +11,2] | +4,4% [+3,5; +5,3] | +6,6% [+5,7; +7,6] |
| VN1 | thứ ba | giá trị | 1,5 [1,2; 3,0] | 0,59 | +0,4% [-4,1; +3,4] | — | +1,8% [-7,6; +79,9] | — | — |

**Nhận xét:**

- **M5:** ở cả ba cửa sổ, lgb_quantile có hạng tốt nhất ở mọi lần lấy mẫu (P(best) = 1,00) và cần ít tồn kho hơn Tweedie, conformal, TSB-NB, ETS với KTC không chứa 0. Chênh lệch với HistGradientBoosting nhỏ (0–1,5%) và ở cửa sổ thứ ba không có ý nghĩa.
- **VN1, cửa sổ chính:** lgb_quantile đứng đầu với P(best) = 0,93, nhưng chênh lệch với Tweedie, conformal và TSB-NB ở fill rate 0,94 đều có KTC chứa 0. Nhận định "TSB-NB cần nhiều hơn 5–10%" (mục 10) **không có ý nghĩa thống kê**.
- **VN1, cửa sổ thứ hai:** TSB-NB, Tweedie và conformal cần ít tồn kho hơn lgb_quantile với KTC không chứa 0.
- **VN1, cửa sổ thứ ba:** lgb_quantile đứng đầu (P(best) = 0,95); TSB-NB, ETS và Tweedie không đạt fill rate 0,94.

### 10.3 KPI theo giá trị

KPI được tính lại với trọng số là giá bán của tuần đó (giá điền tiếp; M5: `sell_prices.csv`; VN1: giá Phase 0–1, Phase 2 dùng giá điền tiếp). Fill rate theo giá trị = Σ giá·bán / Σ giá·nhu cầu; tồn kho theo giá trị = Σ giá·tồn / Σ giá·nhu cầu (tuần nhu cầu). Kết quả trong Bảng 13 (dòng "giá trị") và `equal_fill_ci*.md`.

- Kết luận theo giá trị **trùng** với theo đơn vị ở cả hai dataset và ba cửa sổ: M5 lgb_quantile luôn đứng đầu với P(best) = 1,00; VN1 đổi giữa các cửa sổ như theo đơn vị.
- [Nhận định nhóm] Việc cộng gộp theo đơn vị (hạn chế 6) không làm thay đổi kết luận chính.

### 10.4 Case study: chuỗi bán lẻ giày dép Việt Nam (VNF)

**Dữ liệu** (`f2d.data.load_vnf`): Vietnam Datathon 2023 (Kaggle `tienanh2003/sales-and-inventory-snapshot-data`), kênh bán lẻ, chuỗi mẫu–màu × toàn chuỗi cửa hàng, theo tuần.

- Mã tuần trong dữ liệu là năm + tuần ISO của năm giao dịch, nên gán sai ở ranh giới năm: 202153 chứa ngày 1–2/1/2022 (phần đuôi của tuần ISO 2021-W52) → bỏ; 202352 chứa ngày 1/1/2023 (thuộc tuần ISO 2022-W52) → gộp vào 202252. Tuần 202331 chỉ có ngày 31/7/2023 → bỏ. Không trừ hàng trả lại vào nhu cầu.
- Panel: 1.001 chuỗi × 82 tuần (2022-01-03 → 2023-07-24); 909 chuỗi được đánh giá (smooth 187, erratic 285, intermittent 272, lumpy 165); tỷ lệ tuần bằng 0: 35,4%.
- Cửa sổ kiểm thử: 2023-01-30 → 2023-07-24. Một cửa sổ, vì panel chỉ có 82 tuần.
- Giá vốn và giá bán thực tế: trung vị biên lợi nhuận (giá bán ròng / giá vốn − 1) là 45,5%.
- **Cảnh báo dữ liệu:** (1) mức bán toàn chuỗi giảm từ khoảng 8–17 nghìn đơn vị/tuần trong năm 2022 xuống khoảng 5 nghìn từ tuần 202304 (Tết 2023) và giữ ở mức đó trong toàn bộ cửa sổ kiểm thử; chưa xác định được đây là thay đổi thực hay dữ liệu thiếu; (2) như `05_methodology/dataset.md` đã nêu, nghi ngờ file doanh số (`*_split_1`) chỉ chứa một phần giao dịch; (3) giấy phép "Unknown". Vì vậy case study chỉ dùng để **minh họa** và đánh giá bằng tiền, không dùng để xếp hạng chung.

**Kết quả** (9 phương pháp, có Chronos-2; nguồn: `code/outputs/comparison_VNF.md`, `equal_fill_ci_VNF.md`, `stat_tests_VNF.md`, `VNF/breakeven.csv`):

| | SQL h = 3 | RMSSE h = 3 | Độ phủ q = 0,8 | Hạng đường đánh đổi (toàn bộ) |
|---|---|---|---|---|
| tsb | **0,150** | 0,325 | 0,882 | 4,2 |
| lgb_quantile | 0,154 | **0,292** | 0,890 | **2,6** (P(best) = 0,91) |
| hgb_quantile | 0,154 | 0,299 | 0,880 | 4,2 |
| tsb_nb | 0,158 | 0,321 | 0,882 | 4,0 |
| chronos2 | 0,170 | 0,324 | 0,940 | 5,8 |
| ets | 0,171 | 0,319 | 0,961 | 3,0 |
| lgb_conformal | 0,175 | 0,359 | 0,855 | 7,6 |
| lgb_tweedie | 0,187 | 0,358 | 0,960 | 5,4 |
| empirical | 0,268 | 0,466 | 0,972 | 8,2 |

- Hầu hết phương pháp **dự báo dư**: độ phủ của phân vị 0,8 là 0,86–0,97, fill rate ở τ = 0,9 là 0,93–0,99. [Nhận định nhóm] Phù hợp với việc mức bán giảm ngay trước cửa sổ kiểm thử.
- lgb_quantile hiệu quả tồn kho nhất (hạng 2,6, P(best) = 0,91), dù TSB Poisson có SQL trung bình thấp nhất. Chronos-2 xếp 5,8, cần nhiều hơn lgb_quantile 11–26% ở fill rate 0,90–0,96 (KTC không chứa 0).
- Nhóm intermittent: fill rate ở τ = 0,9 chỉ 0,58–0,75, không phương pháp nào đạt 0,90 nên không xếp hạng được.
- **Thanh lý tính bằng tiền** (giá vốn và giá bán thực của từng chuỗi, chi phí lưu kho 10–40%/năm, cận trên): với 4 mô hình ML, quy tắc phân vị và quy tắc cố định có s\* ≈ 0,90–1,01 lần giá vốn; dead13 ≈ 1,26–1,43; dead26 ≈ 1,15–1,33. Với Chronos-2: quy tắc phân vị 1,04–1,09; dead13 1,21–1,30; dead26 1,14–1,22. Lượng thanh lý nhỏ (≤ 3% nhu cầu). Kết luận giống M5 và VN1: trong cửa sổ 26 tuần, thanh lý chỉ có lợi khi bán thanh lý gần bằng giá vốn.

### 10.5 Chronos-2 (foundation model, zero-shot)

- Mô hình: `amazon/chronos-2` (120 triệu tham số, Apache-2.0), chạy trên CPU, không fine-tune, không dùng biến ngoại sinh. Để dự báo trực tiếp phân vị của D_h như các phương pháp khác, ngữ cảnh là chuỗi các tổng h tuần không chồng lấn kết thúc ngay trước origin (tối đa 104 tuần), dự báo 1 bước; các phân vị 0,5–0,99 nằm trong tập phân vị huấn luyện của mô hình (`f2d.models.chronos2`).
- **Rò rỉ dữ liệu:** tập huấn luyện của Chronos-2 gồm một phần `autogluon/chronos_datasets` và `Salesforce/GiftEvalPretrain` (model card); **cả hai đều có M5**, không có VN1. Kết quả trên M5 vì vậy không phải zero-shot "sạch"; VN1 và VNF thì sạch.
- Kết quả 9 phương pháp ghi vào `code/outputs/<D>[_wN]_c2/` để không thay đổi kết quả 8 phương pháp ở trên (`code/outputs/logs/rerun_c2.sh`). Đã chạy: M5 cửa sổ chính; VN1 ba cửa sổ; VNF (mục 10.4). M5 ở cửa sổ thứ hai, thứ ba **không** chạy (khoảng 13 giờ CPU mỗi cửa sổ). Nguồn: `comparison_c2.md`, `comparison_w26_c2_VN1.md`, `comparison_w52_c2_VN1.md`, `stat_tests_c2.md`, `stat_tests_w26_c2_VN1.md`, `stat_tests_w52_c2_VN1.md`, `equal_fill_ci*_c2.md`.

**Bảng 14.** Chronos-2 so với LightGBM quantile (h = 3; hạng theo chuỗi trong 9 phương pháp; Δ tồn kho = I_chronos2 / I_lgb_quantile − 1 ở cùng fill rate, KTC 95% bootstrap).

| | SQL TB chronos2 / lgb_q | Hạng theo chuỗi chronos2 (CD) | % chuỗi lgb_q có SQL thấp hơn | Hạng đường đánh đổi chronos2 (9 PP) | Δ tồn kho ở fill 0,90 | Δ ở fill 0,94 |
|---|---|---|---|---|---|---|
| M5, chính (\*) | 0,242 / 0,208 | 5,56 (0,069) | 72,8% | 5,6 | +14,3% [+13,5; +14,9] | +12,8% [+12,0; +13,6] |
| VN1, chính | 0,620 / 0,336 | 5,45 (0,102) | 68,8% | 6,2 | +41,5% [+29,0; +55,2] | +56,4% [+29,4; +97,8] |
| VN1, thứ hai | 0,653 / 0,539 | 5,61 (0,112) | 72,6% | 4,0 | −0,6% [−3,8; +3,0] | −3,2% [−7,5; +1,7] |
| VN1, thứ ba | 2,404 / 2,008 | 5,37 (0,124) | 69,4% | 5,25 | +46,5% [+32,7; +63,9] | +73,9% [+51,2; +101,0] |
| VNF | 0,170 / 0,154 | — | — | 5,8 | +12,9% [+1,3; +21,8] | +26,0% [+17,6; +30,3] |

(\*) M5 có trong tập huấn luyện của Chronos-2.

- **Độ chính xác:** Chronos-2 kém lgb_quantile ở mọi dataset và cửa sổ, cả theo trung bình lẫn theo chuỗi (lgb_quantile tốt hơn ở 64–79% chuỗi, h = 3 và 13). Trên M5, dù có thể đã thấy dữ liệu khi huấn luyện, SQL của Chronos-2 (0,242) chỉ ngang ETS (0,246). Trên VN1, SQL trung bình của Chronos-2 rất cao ở nhóm lumpy (1,471 ở cửa sổ chính).
- **Hiệu quả tồn kho:** Chronos-2 không đứng đầu ở bất kỳ dataset, cửa sổ hay nhóm nào; P(best) = 0 ở mọi trường hợp tổng thể. Ở cửa sổ thứ hai của VN1, Chronos-2 ngang lgb_quantile (KTC chứa 0) và đứng thứ hai ở nhóm smooth (3,0, sau TSB-NB 2,4).
- **Thời gian chạy** (CPU, có lúc chạy song song với tiến trình khác): VN1 cửa sổ chính 2.692 s (h = 3) và 2.360 s (h = 13); M5 19.324 s và 28.618 s; VNF 373 s và 331 s. So với lgb_quantile (VN1 146 / 314 s; M5 1.251 / 686 s, mục 4 của `experimental_setup.md`), Chronos-2 chậm hơn khoảng 8–42 lần.
- [Nhận định nhóm] Với cách dùng zero-shot, không biến ngoại sinh, một foundation model tổng quát chưa vượt được mô hình boosting toàn cục không tinh chỉnh ở tầng quyết định tồn kho trên dữ liệu bán lẻ rời rạc. **[Chưa kiểm chứng]** Cách tạo ngữ cảnh bằng tổng h tuần (để dự báo trực tiếp D_h) làm ngữ cảnh ngắn (khoảng 8 điểm với h = 13); dùng chuỗi tuần với biến ngoại sinh hoặc cross-learning có thể cho kết quả khác.
- Thêm Chronos-2 làm thay đổi nhẹ hạng của các phương pháp khác. Ví dụ ở VN1 cửa sổ thứ hai, TSB-NB từ 1,8 thành 2,0 và đồng hạng với conformal. Các kết luận về phương pháp đứng đầu ở Bảng 12 không thay đổi, trừ trường hợp đồng hạng này.

## 11. Hạn chế và việc còn lại

**Hạn chế**

1. Kiểm định thống kê đã chạy cho SQL và KPI theo chuỗi (mục 2). KPI ở **cùng fill rate** không kiểm định được theo từng chuỗi (fill rate của từng chuỗi rời rạc); thay vào đó dùng khoảng tin cậy bootstrap theo chuỗi (mục 10.2).
2. **Ba cửa sổ kiểm thử** (mục 10, 10.1). Kết quả VN1 về hiệu quả tồn kho tổng thể và theo nhóm smooth/erratic đổi giữa các cửa sổ.
3. **M5 chưa chạy lưới L, H, q_L, k.**
4. **Nhu cầu bị kiểm duyệt; siêu tham số cố định; HistGradientBoosting dùng mẫu con và early stopping khác.**
5. **Tầm nhìn 26 tuần quá ngắn** để thấy lợi ích của thanh lý hàng lỗi thời (mục 7.2).
6. KPI được cộng gộp theo đơn vị, nên chuỗi lớn chi phối kết quả. Kiểm định theo chuỗi (mục 2) bổ sung góc nhìn không trọng số; KPI theo giá trị (mục 10.3) cho cùng kết luận.
7. **Case study VNF** chỉ có một cửa sổ, có dấu hiệu dữ liệu thiếu và mức bán giảm đột ngột trước cửa sổ kiểm thử (mục 10.4).
8. **Chronos-2 trên M5 có rủi ro rò rỉ dữ liệu** (mục 10.5).

**Việc còn lại trước khi viết bài (Bước 11)**

- [x] Kiểm định thống kê (mục 2).
- [x] Xếp hạng theo đường đánh đổi (mục 4, 6).
- [x] Sửa lỗi Tweedie (mục 1.1).
- [x] Quy tắc dead-stock (mục 7.1).
- [x] Cửa sổ kiểm thử thứ hai (mục 10).
- [x] Cửa sổ kiểm thử thứ ba (mục 10.1).
- [x] Khoảng tin cậy bootstrap ở cùng fill rate; KPI theo giá trị (mục 10.2, 10.3).
- [x] Case study VNF (mục 10.4).
- [x] Chronos-2 (mục 10.5).
- [ ] (Tùy chọn) lưới L, H cho M5.
- [ ] Đọc W3 và bài 20 để định vị lại phần "độ chính xác theo chuỗi ≠ hiệu quả tồn kho" trước khi đưa vào bài (`03_problem_and_gap/research_gap.md` mục 6).
