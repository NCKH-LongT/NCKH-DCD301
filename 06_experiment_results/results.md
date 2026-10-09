# Results

Mọi số liệu lấy từ `code/outputs/` (bản sao: `tables/`).

- Bảng đầy đủ: `tables/comparison_full.md`.
- Hình: `figures/fig_tradeoff_M5.png`, `figures/fig_tradeoff_VN1.png`.

Quy ước:

- Kịch bản mặc định: τ = 0,9; L = 2; R = 1; H = 13; q_L = 0,95; k = 26.
- Tồn kho tính bằng **tuần nhu cầu**.
- **Chưa có kiểm định thống kê** giữa các phương pháp (mục 9). Vì vậy các chênh lệch nhỏ (dưới khoảng 0,01 SQL hoặc 0,005 fill rate) chỉ được mô tả, không kết luận là khác biệt.
- [Nhận định nhóm] đánh dấu phần diễn giải, không phải số đo.

## 0. Tóm tắt

1. **Độ chính xác:** LightGBM quantile có SQL thấp nhất trên cả hai dataset, ở cả hai horizon và cả 4 nhóm nhu cầu. HistGradientBoosting quantile sát ngay sau.
2. **Hiệu quả tồn kho ở cùng fill rate:**
   - M5: LightGBM quantile cần ít tồn kho nhất để đạt fill rate 0,94–0,96, ít hơn khoảng 8–12% so với các baseline mạnh.
   - VN1: lợi thế này **không còn**. LightGBM-Tweedie + safety stock chuẩn ngang hoặc tốt hơn ở fill rate 0,90–0,94; chỉ các mô hình phân vị trực tiếp đạt được 0,96.
3. **Theo nhóm:** kết luận khác nhau giữa hai dataset.
   - M5: mô hình phân vị trực tiếp tốt nhất ở mọi nhóm.
   - VN1: TSB negative binomial hiệu quả nhất ở nhóm smooth và intermittent; mô hình ML tốt hơn ở erratic và lumpy.
4. **Thanh lý:**
   - Quy tắc theo phân vị giảm tồn kho mà gần như không mất fill rate; quy tắc cố định mất nhiều hơn, rõ nhất ở nhóm lumpy của VN1.
   - Về kinh tế, quy tắc cố định có ngưỡng giá thu hồi hòa vốn s\* > 1 lần giá vốn, nên không có lợi.
   - Với quy tắc phân vị trên VN1, s\* nằm trong khoảng 0,64–0,98 lần giá vốn, tùy cách định giá hàng tồn cuối kỳ. Vì vậy, trong cửa sổ 26 tuần, chưa khẳng định được lợi ích kinh tế.
5. **Độ nhất quán giữa dataset:** Spearman ρ của thứ hạng fill rate giữa M5 và VN1 là 0,69 cho toàn bộ chuỗi, 0,90 cho nhóm intermittent và 0,12 cho nhóm erratic.

## 1. RQ1 — Độ chính xác dự báo

**Bảng 1.** SQL, RMSSE và độ phủ của phân vị 0,9 (toàn bộ chuỗi). Thấp hơn là tốt hơn, trừ độ phủ (lý tưởng = 0,9).

| Mô hình | M5 SQL h=3 | M5 SQL h=13 | M5 RMSSE h=3 | M5 cov₀.₉ h=3 | VN1 SQL h=3 | VN1 SQL h=13 | VN1 RMSSE h=3 | VN1 cov₀.₉ h=3 |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,340 | 0,347 | 0,765 | 0,855 | 0,522 | 0,557 | 0,799 | 0,909 |
| tsb | 0,283 | 0,361 | 0,596 | 0,793 | 0,454 | 0,506 | 0,645 | 0,849 |
| tsb_nb | 0,251 | 0,317 | 0,610 | 0,881 | 0,411 | 0,458 | 0,650 | 0,903 |
| ets | 0,246 | 0,254 | 0,601 | 0,890 | 0,431 | 0,445 | 0,654 | 0,912 |
| lgb_tweedie | 0,226 | 0,215 | **0,567** | 0,860 | 0,496 | 0,664 | 0,819 | 0,922 |
| lgb_conformal | 0,229 | 0,231 | 0,574 | 0,899 | 0,436 | 0,590 | 0,800 | 0,907 |
| hgb_quantile | 0,211 | 0,201 | 0,572 | 0,872 | 0,338 | 0,423 | **0,593** | 0,917 |
| **lgb_quantile** | **0,208** | **0,198** | 0,570 | 0,883 | **0,336** | **0,410** | 0,594 | 0,921 |

- LightGBM quantile có SQL thấp nhất trong cả 4 cột SQL. HistGradientBoosting quantile cách 0,002–0,013, dù chỉ huấn luyện trên tối đa 300.000 dòng. Như vậy kết quả **không phụ thuộc riêng vào thư viện LightGBM**.
- Về dự báo điểm (RMSSE), LightGBM-Tweedie tốt nhất trên M5, nhưng chênh lệch giữa 4 mô hình ML trên M5 nhỏ (0,567–0,574).
- **Bất thường cần kiểm tra:** trên VN1, LightGBM-Tweedie (và conformal, vì dùng cùng mô hình điểm) có RMSSE ở h = 13 bằng 1,13 (conformal 1,07), kém cả Empirical (0,64). SQL h = 13 của Tweedie cũng kém nhất (0,664).
  - [Nhận định nhóm] Mô hình Tweedie học D_h không chuẩn hóa, nên có thể bị một số chuỗi quy mô lớn chi phối. Chưa xác minh.
  - Ảnh hưởng: chỉ đến ngưỡng thanh lý của hai mô hình này (dùng h = 13), không ảnh hưởng đến đặt hàng (h = 3).
- **Hiệu chỉnh:** trên M5, các phân vị 0,9 của mọi mô hình đều phủ dưới 0,9 (0,79–0,90), tức hơi lệch thấp. Trên VN1, phần lớn phủ 0,90–0,92; riêng TSB Poisson chỉ phủ 0,849, do khoảng Poisson quá hẹp.

## 2. RQ1 — KPI tồn kho ở kịch bản mặc định (không thanh lý)

**Bảng 2.** Fill rate, CSL, tỷ lệ hết hàng (trên tuần có nhu cầu) và tồn kho; khoảng tin cậy bootstrap 95% trong ngoặc.

| Mô hình | M5 fill | M5 CSL | M5 hết hàng | M5 tồn kho | VN1 fill | VN1 CSL | VN1 hết hàng | VN1 tồn kho |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,935 | 0,906 | 0,117 | 1,78 | 0,888 | 0,943 | 0,137 | 2,80 |
| tsb | 0,891 | 0,873 | 0,158 | **1,00** | 0,823 | 0,910 | 0,216 | **1,31** |
| tsb_nb | 0,950 | 0,929 | 0,088 | 1,65 | 0,911 | 0,948 | 0,125 | 2,40 |
| ets | 0,960 | 0,946 | 0,067 | 1,87 | 0,917 | 0,958 | 0,100 | 2,74 |
| lgb_tweedie | 0,947 | 0,931 | 0,086 | 1,59 | 0,926 | 0,966 | 0,082 | 2,60 |
| lgb_conformal | **0,965** (0,964–0,967) | **0,954** | **0,057** | 2,04 | 0,930 | 0,967 | 0,079 | 2,70 |
| hgb_quantile | 0,951 | 0,937 | 0,079 | 1,53 | 0,945 | 0,972 | 0,068 | 3,47 |
| lgb_quantile | 0,956 (0,954–0,957) | 0,942 | 0,072 | 1,58 (1,55–1,61) | **0,948** (0,943–0,953) | **0,973** | **0,066** | 3,41 (3,13–3,70) |

- Ở cùng τ = 0,9, các phương pháp **không** đạt cùng mức phục vụ. Vì vậy so sánh fill rate hoặc tồn kho riêng lẻ ở một τ dễ gây hiểu lầm. Ví dụ:
  - TSB Poisson có tồn kho thấp nhất nhưng fill rate thấp nhất;
  - trên VN1, LightGBM quantile có fill rate cao nhất nhưng tồn kho cũng cao nhất.
- Mục 3 so sánh ở **cùng fill rate**.
- CSL của VN1 cao hơn fill rate vì nhiều tuần không có nhu cầu (không thể hết hàng).

## 3. RQ1 — Đánh đổi tồn kho – fill rate

![M5 trade-off](figures/fig_tradeoff_M5.png)

![VN1 trade-off](figures/fig_tradeoff_VN1.png)

**Bảng 3.** Tồn kho (tuần nhu cầu) cần để đạt fill rate mục tiêu, toàn bộ chuỗi (nội suy trên τ ∈ {0,8; 0,9; 0,95}). "—" = mục tiêu nằm ngoài khoảng fill rate mà phương pháp đạt được trong lưới τ (cao hơn mức tối đa, hoặc thấp hơn mức tối thiểu).

| Mô hình | M5 0,94 | M5 0,96 | VN1 0,90 | VN1 0,92 | VN1 0,94 | VN1 0,96 |
|---|---|---|---|---|---|---|
| empirical | 1,88 | — | 3,16 | 3,73 | — | — |
| tsb | — | — | — | — | — | — |
| tsb_nb | 1,51 | 1,92 | 2,21 | 2,67 | — | — |
| ets | 1,52 | 1,87 | 2,38 | 2,83 | — | — |
| lgb_tweedie | 1,50 | 1,88 | **2,16** | **2,50** | **3,02** | — |
| lgb_conformal | 1,52 | 1,93 | 2,24 | 2,55 | 3,17 | — |
| hgb_quantile | 1,39 | 1,74 | — | 2,68 | 3,31 | 4,36 |
| **lgb_quantile** | **1,38** | **1,69** | — | 2,54 | 3,17 | **4,13** |

**M5:**

- Đường của LightGBM quantile và HistGradientBoosting nằm trên – trái các đường khác.
- Để đạt fill rate 0,94, LightGBM quantile cần 1,38 tuần tồn kho. Các phương pháp khác cần:
  - Tweedie + safety stock: 1,50 (LightGBM quantile cần ít hơn 8,0%);
  - TSB-NB: 1,51 (ít hơn 8,6%);
  - ETS và conformal: 1,52 (ít hơn 9,2%).
- Ở fill rate 0,96, LightGBM quantile cần ít tồn kho hơn 10–12% so với Tweedie, TSB-NB, ETS và conformal; ít hơn 2,9% so với HistGradientBoosting.

**VN1:**

- Các đường ML và TSB-NB gần như chồng lên nhau ở fill rate 0,90–0,93.
- LightGBM-Tweedie + safety stock chuẩn cần ít tồn kho nhất ở 0,90–0,94 (ở 0,94: 3,02 so với 3,17 của LightGBM quantile).
- Chỉ hai mô hình phân vị trực tiếp đạt được 0,96.
- [Nhận định nhóm] Trên VN1, SQL tốt hơn rõ (0,336 so với 0,496) **không** chuyển thành hiệu quả tồn kho tốt hơn ở mức phục vụ trung bình. Lợi thế của phân vị trực tiếp chỉ thể hiện ở mức phục vụ cao.

## 4. RQ2 — Theo nhóm nhu cầu

**Bảng 4.** SQL (h = 3) theo nhóm.

| Mô hình | M5 smooth | M5 erratic | M5 intermittent | M5 lumpy | VN1 smooth | VN1 erratic | VN1 intermittent | VN1 lumpy |
|---|---|---|---|---|---|---|---|---|
| empirical | 0,208 | 0,230 | 0,556 | 0,384 | 0,437 | 0,448 | 0,514 | 0,669 |
| tsb | 0,196 | 0,215 | 0,425 | 0,309 | 0,376 | 0,428 | 0,459 | 0,533 |
| tsb_nb | 0,172 | 0,189 | 0,381 | 0,270 | 0,314 | 0,353 | 0,443 | 0,465 |
| ets | 0,168 | 0,178 | 0,376 | 0,261 | 0,319 | 0,350 | 0,474 | 0,490 |
| lgb_tweedie | 0,165 | 0,173 | 0,326 | 0,251 | 0,289 | 0,310 | 0,637 | 0,485 |
| lgb_conformal | 0,166 | 0,169 | 0,332 | 0,262 | 0,280 | 0,288 | 0,544 | 0,428 |
| hgb_quantile | 0,157 | 0,162 | 0,300 | 0,236 | 0,262 | 0,260 | 0,387 | 0,349 |
| **lgb_quantile** | **0,155** | **0,160** | **0,295** | **0,232** | **0,260** | **0,258** | **0,384** | **0,345** |

**Bảng 5.** Tồn kho cần để đạt fill rate mục tiêu, theo nhóm. Mỗi ô ghi phương pháp hiệu quả nhất và hai phương pháp kế tiếp; nguồn: `tables/comparison_full.md`.

| Nhóm | M5 (fill 0,94) | VN1 (mục tiêu cao nhất mà ≥ 3 phương pháp đạt được) |
|---|---|---|
| smooth | lgb_quantile 1,12; hgb 1,14; tsb_nb 1,22 | 0,94: **tsb_nb 1,67**; ets 1,74; lgb_quantile 1,85 |
| erratic | lgb_quantile 2,16; conformal 2,17; hgb 2,19 | 0,92: **conformal 4,07**; lgb_quantile 4,28; hgb 4,62 |
| intermittent | lgb_quantile 1,96; hgb 2,01; tweedie 2,16 | 0,92: **tsb_nb 2,64**; lgb_quantile 2,90; hgb 3,07 |
| lumpy | lgb_quantile 3,00; hgb 3,04; ets 3,16 | 0,90: **conformal 5,00**; lgb_quantile 6,06; hgb 6,27 |

- **M5:** mô hình phân vị trực tiếp có SQL thấp nhất **và** cần ít tồn kho nhất ở cả 4 nhóm. Chênh lệch lớn nhất (tính tương đối) ở nhóm smooth và intermittent.
- **VN1:** mô hình chính xác nhất (theo SQL) không phải lúc nào cũng hiệu quả nhất về tồn kho.
  - TSB negative binomial hiệu quả nhất ở nhóm smooth và intermittent, ở những mức phục vụ mà nó đạt được. Tuy vậy, nó không đạt fill rate 0,94 ở nhóm intermittent.
  - Ở nhóm lumpy, chỉ ba mô hình (conformal, LightGBM quantile, HistGradientBoosting) đạt fill rate ≥ 0,90, và phải giữ 5–6 tuần tồn kho.
- Fill rate ở kịch bản mặc định giảm dần từ smooth đến lumpy ở mọi phương pháp (VN1 LightGBM quantile: 0,961 → 0,928; Empirical: 0,926 → 0,720).
- [Nhận định nhóm] Kết quả ủng hộ việc **chọn phương pháp theo nhóm nhu cầu** trên dữ liệu thương mại điện tử rời rạc. Ở mức phục vụ trung bình, baseline thống kê có phân phối phù hợp (TSB-NB) vẫn cạnh tranh.

## 5. RQ3 — Thanh lý

**Bảng 6.** Kịch bản mặc định, toàn bộ chuỗi. Ký hiệu: Δfill = thay đổi fill rate so với không thanh lý (điểm %); tồn kho = tuần nhu cầu; % thanh lý = đơn vị thanh lý / nhu cầu.

| Mô hình | Dataset | Tồn kho (không) | Quantile: tồn kho | Quantile: % thanh lý | Quantile: Δfill | Fixed: tồn kho | Fixed: % thanh lý | Fixed: Δfill |
|---|---|---|---|---|---|---|---|---|
| lgb_quantile | M5 | 1,581 | 1,579 | 0,02 | 0,00 | 1,545 | 0,79 | −0,29 |
| tsb_nb | M5 | 1,650 | 1,591 | 1,07 | −0,48 | 1,644 | 0,17 | −0,09 |
| lgb_quantile | VN1 | 3,405 | 3,261 | 1,18 | −0,02 | 3,198 | 2,76 | −0,67 |
| hgb_quantile | VN1 | 3,475 | 3,066 | 3,66 | −0,10 | 3,245 | 2,95 | −0,64 |
| lgb_tweedie | VN1 | 2,598 | 2,518 | 0,70 | −0,05 | 2,466 | 2,23 | −0,28 |
| lgb_conformal | VN1 | 2,697 | 2,628 | 0,51 | −0,02 | 2,548 | 2,23 | −0,37 |
| tsb_nb | VN1 | 2,401 | 2,246 | 2,28 | −0,45 | 2,370 | 0,54 | −0,05 |

- **M5:** quy tắc phân vị gần như không kích hoạt với các mô hình ML, ETS và Empirical (≤ 0,02% nhu cầu). Nó chỉ kích hoạt với TSB và TSB-NB (khoảng 1,1%), làm mất khoảng 0,5 điểm % fill rate. [Nhận định nhóm] Với L = 2 và tồn kho khoảng 1,6 tuần, M5 ít có tồn dư trong cửa sổ này.
- **VN1:** với các mô hình ML, quy tắc phân vị giảm tồn kho 2,5–12% và mất ≤ 0,1 điểm % fill rate. Quy tắc cố định giảm tồn kho nhiều hơn với LightGBM quantile (−6,1%), nhưng mất 0,3–0,7 điểm % fill rate và chạm khoảng 50% số chuỗi (quy tắc phân vị: 5–12%).
- **Nhóm lumpy, VN1, LightGBM quantile** — rõ nhất:

  | Chính sách | % thanh lý | Fill rate | Tồn kho |
  |---|---|---|---|
  | Không thanh lý | 0 | 0,928 | 7,52 |
  | Quantile | 6,4 | 0,926 | 6,73 (−10,5%) |
  | Fixed | 14,6 | 0,877 | 6,40 (−14,9%) |

**Ngưỡng giá thu hồi hòa vốn s\*** (chi phí lưu kho 25%/năm, biên lợi nhuận 50%; cận trên (a) / cận dưới (b); `tables/breakeven_*.csv`):

| Mô hình | M5 quantile | M5 fixed | VN1 quantile | VN1 fixed |
|---|---|---|---|---|
| lgb_quantile | 1,00 / 1,00 (*) | 1,14 / 1,16 | 0,95 / 0,78 | 1,09 / 1,15 |
| hgb_quantile | 0,93 / — (*) | 1,14 / 1,16 | 0,96 / 0,83 | 1,07 / 1,12 |
| lgb_tweedie | 0,95 / 0,93 (*) | 1,15 / 1,16 | 0,98 / 0,97 | 1,04 / 1,06 |
| lgb_conformal | 1,15 / 1,31 (*) | 1,14 / 1,15 | 0,96 / 0,64 | 1,05 / 1,07 |
| tsb_nb | 1,20 / 1,23 | 1,22 / 1,27 | 1,07 / 1,14 | 1,03 / 1,07 |
| ets | 1,05 / 1,20 (*) | 1,10 / 1,10 | 1,07 / 1,13 | 1,00 / 1,00 |

(*) Dưới 1.200 đơn vị bị thanh lý trên toàn M5, nên s\* không ổn định. Cận (b) của Empirical trên VN1 (−7,7) cũng không có ý nghĩa, vì mẫu số gần 0. Hai giá trị này không dùng để kết luận.

- Trên toàn lưới (chi phí lưu kho 10–40%/năm × biên lợi nhuận 30–100%), với 4 mô hình ML trên VN1:
  - quy tắc phân vị: cận trên s\* từ 0,91 đến 1,05;
  - quy tắc cố định: cận trên s\* từ 1,00 đến 1,22.
- Trên M5, quy tắc cố định với các mô hình ML có s\* từ 1,07 đến 1,32.
- **Phân rã mỗi đơn vị thanh lý** (so với không thanh lý, toàn bộ 26 tuần; tính từ `breakeven_*.csv`):

  | Quy tắc | Phải đặt lại | Mất doanh số | Lẽ ra còn tồn ở cuối kỳ |
  |---|---|---|---|
  | VN1, quantile, 4 mô hình ML | 0,07–0,48 | 0,02–0,07 | 0,45–0,89 |
  | VN1, fixed, 4 mô hình ML | 0,35–0,54 | 0,13–0,23 | 0,31–0,42 |
  | M5, fixed, 4 mô hình ML | 0,57–0,62 | 0,31–0,33 | 0,06–0,11 |

  "Phải đặt lại" = Δđặt hàng / X; "Mất doanh số" = −Δbán / X; "Lẽ ra còn tồn" = −Δvị trí cuối / X.

- [Nhận định nhóm] Cách đọc bảng phân rã:
  - Quy tắc cố định thanh lý nhiều hàng mà sau đó phải đặt lại hoặc làm mất doanh số, nên s\* > 1.
  - Quy tắc phân vị chủ yếu thanh lý hàng **lẽ ra vẫn nằm trong kho ở cuối 26 tuần**. Vì vậy s\* của nó phụ thuộc vào giá trị của hàng tồn cuối kỳ:
    - nếu tính theo giá vốn: s\* ≈ 0,95–0,98;
    - nếu số hàng đó rồi cũng phải thanh lý: s\* = 0,64–0,97.
  - Muốn đánh giá đầy đủ lợi ích của thanh lý (tránh hàng lỗi thời) cần tầm nhìn dài hơn 26 tuần, hoặc giá trị thực của hàng tồn cuối kỳ.
- Ở cấp chuỗi (VN1, LightGBM quantile, không thanh lý; `tables/series_inventory_VN1.csv`):
  - trung vị số tuần tồn kho là 6,9; phân vị 90 là 42 tuần;
  - **28,2% chuỗi không có nhu cầu** trong 22 tuần KPI, trong khi quy tắc phân vị chỉ chạm 5,4% số chuỗi;
  - trên M5, các con số tương ứng là: trung vị 2,0 tuần, phân vị 90 là 6,6 tuần, 0,3% chuỗi không có nhu cầu.
  - [Nhận định nhóm] Hàng tồn "chết" là vấn đề thực sự của VN1 mà quy tắc hiện tại chưa xử lý.

## 6. RQ4 — Độ nhạy theo kịch bản

**τ (cả hai dataset).** Fill rate và tồn kho tăng đơn điệu theo τ với mọi phương pháp (Bảng 3, hình mục 3).

| | τ = 0,8 | τ = 0,9 | τ = 0,95 |
|---|---|---|---|
| M5, LightGBM quantile: fill / tồn kho | 0,921 / 1,13 | 0,956 / 1,58 | 0,974 / 2,05 |
| VN1, LightGBM quantile: fill / tồn kho | 0,907 / 2,16 | 0,948 / 3,41 | 0,971 / 4,77 |

TSB Poisson gần như không phản ứng với τ trên VN1 (fill 0,813 → 0,830), do khoảng Poisson quá hẹp.

**Lead time L (chỉ VN1).**

| Mô hình | fill L=1 | fill L=2 | fill L=4 | tồn kho L=1 | tồn kho L=2 | tồn kho L=4 |
|---|---|---|---|---|---|---|
| lgb_quantile | 0,944 | 0,948 | 0,943 | 2,07 | 3,41 | 6,01 |
| lgb_tweedie | 0,928 | 0,926 | 0,918 | 1,75 | 2,60 | 4,36 |
| lgb_conformal | 0,931 | 0,930 | 0,926 | 1,78 | 2,70 | 4,60 |
| tsb_nb | 0,919 | 0,911 | 0,889 | 1,76 | 2,40 | 3,61 |
| ets | 0,918 | 0,917 | 0,908 | 1,83 | 2,74 | 4,70 |

- Thứ hạng fill rate gần như không đổi theo L: Spearman ρ giữa L = 2 và L = 1 là 0,96; giữa L = 2 và L = 4 là 1,00 (7 phương pháp).
- Tồn kho tăng gần tỷ lệ với L + R.
- TSB-NB mất fill rate nhanh nhất khi L tăng: −2,2 điểm % từ L = 2 lên L = 4.

**Tham số thanh lý (VN1, LightGBM quantile).**

- H = 8 / 13 / 26 → % thanh lý 3,1 / 1,2 / 0,2; fill rate gần như không đổi (0,946 / 0,948 / 0,948).
- q_L = 0,9 / 0,95 / 0,99 → % thanh lý 2,8 / 1,2 / 0,2.
- Quy tắc cố định với k = 13 / 26 / 52 → % thanh lý 7,1 / 2,8 / 1,2, và fill rate 0,929 / 0,941 / 0,946.
- [Nhận định nhóm] Quy tắc cố định với k nhỏ làm mất fill rate rõ rệt. Quy tắc phân vị an toàn hơn trong toàn bộ lưới.

## 7. Độ nhất quán giữa M5 và VN1

**Bảng 7.** Spearman ρ của thứ hạng fill rate (kịch bản mặc định, không thanh lý, 8 phương pháp).

| Nhóm | toàn bộ | smooth | erratic | intermittent | lumpy |
|---|---|---|---|---|---|
| ρ | 0,69 | 0,60 | 0,12 | **0,90** | 0,69 |
| p (scipy, xấp xỉ t) | 0,058 | 0,12 | 0,78 | **0,002** | 0,058 |

- Với chỉ 8 phương pháp, chỉ nhóm intermittent có thứ hạng nhất quán có ý nghĩa ở mức 5%. Toàn bộ chuỗi và nhóm lumpy ở mức biên (p = 0,058).
- Thứ hạng **SQL** thì nhất quán hơn: ở h = 3, LightGBM quantile đứng đầu và Empirical đứng cuối ở cả hai dataset (Bảng 1).
- Thứ hạng theo hiệu quả tồn kho thì khác nhau (mục 3–4).

## 8. Kiểm tra giả thuyết (`05_methodology/evaluation_metrics.md` mục 7)

| Giả thuyết | Kết quả | Mức độ |
|---|---|---|
| H1: LightGBM quantile có SQL thấp nhất | Đúng trên cả hai dataset, cả hai horizon, cả 4 nhóm; HistGradientBoosting rất sát | Ủng hộ (chưa kiểm định) |
| H2: Phân vị trực tiếp cần ít tồn kho hơn dự báo điểm + safety stock | M5: đúng (−8 đến −10%). VN1: sai ở fill rate 0,90–0,94; chỉ đúng ở mức cao (0,96 chỉ mô hình phân vị đạt được) | Ủng hộ một phần |
| H3: ML có lợi rõ ở smooth/erratic; TSB đủ tốt ở intermittent | M5: ML tốt nhất ở mọi nhóm. VN1: TSB-NB tốt nhất ở intermittent **và** smooth; ML tốt hơn ở erratic, lumpy | Ủng hộ một phần, phụ thuộc dataset |
| H4: Thanh lý theo phân vị giảm tồn kho mà mất ít fill rate hơn quy tắc cố định | Đúng trên VN1, rõ nhất ở nhóm lumpy; trên M5 quy tắc phân vị hầu như không kích hoạt. Về kinh tế, s\* cao | Ủng hộ về KPI; lợi ích kinh tế hạn chế |

## 9. Hạn chế và việc còn lại

**Hạn chế của kết quả hiện tại**

1. **Chưa có kiểm định thống kê.** Cần lưu SQL và KPI theo từng chuỗi, rồi chạy Friedman–Nemenyi (SQL) và Wilcoxon + Holm (KPI). Chênh lệch giữa LightGBM quantile và HistGradientBoosting (0,002–0,013 SQL) cần kiểm định trước khi kết luận.
2. **Một cửa sổ kiểm thử 26 tuần** cho mỗi dataset. Nên thêm một cửa sổ kiểm thử sớm hơn (ví dụ dời lùi 26 tuần) để kiểm tra độ ổn định.
3. **M5 chưa chạy lưới L, H, q_L, k.** Nếu cần, chạy cho các mô hình nhanh và LightGBM quantile (khoảng 1 giờ).
4. **Bất thường RMSSE của LightGBM-Tweedie ở VN1, h = 13** (mục 1) cần tìm nguyên nhân. Một hướng: huấn luyện Tweedie trên mục tiêu chuẩn hóa D_h / s.
5. **Nhu cầu bị kiểm duyệt; siêu tham số cố định; HistGradientBoosting dùng mẫu con và early stopping khác.**
6. **Tầm nhìn 26 tuần quá ngắn** để thấy lợi ích của thanh lý hàng lỗi thời. Có thể thêm quy tắc thanh lý hàng không bán trong N tuần (dead-stock).
7. KPI được cộng gộp theo đơn vị, nên chuỗi lớn chi phối kết quả. Có thể báo cáo thêm trung vị theo chuỗi.

**Việc nên làm trước khi viết bài (Bước 11)**

- [ ] Kiểm định thống kê (mục 9.1).
- [ ] Cửa sổ kiểm thử thứ hai.
- [ ] Sửa hoặc giải thích bất thường Tweedie ở VN1, h = 13.
- [ ] (Tùy chọn) lưới L, H cho M5; quy tắc thanh lý dead-stock.
- [ ] Đọc W3 và bài 20 để định vị lại phần "độ chính xác ≠ hiệu quả tồn kho" (mục 3–4) trước khi đưa vào bài (`03_problem_and_gap/research_gap.md` mục 6).
