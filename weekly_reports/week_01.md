# WEEK 1 REPORT: FOUNDATION & SYSTEM ARCHITECTURE

## 1. Weekly Progress Checklist
- [x] Formed the research team and allocated project roles.
- [x] Conducted domain research and resolved 4 core Research Questions (RQ-08).
- [x] Defined System Input/Output data boundaries.
- [x] Engineered the Functional System Processing Action Table.
- [x] Validated the mathematical correctness via a 1-bit error-correction test case.

---

## 2. Core Research & Technical Achievements

### 2.1. Answers to Research Questions (Summary)
The team has mathematically validated the Hamming boundary formula $2^r \ge m + r + 1$. For a 4-bit data word ($m = 4$), the condition requires exactly $r = 3$ parity bits ($P_1, P_2, P_4$), producing a structured 7-bit codeword. By computing the Syndrome vector $S = [S_4, S_2, S_1]$ at the receiver via localized XOR ($\oplus$) parity checks, the system derives a binary indicator whose decimal equivalent ($1 \dots 7$) directly isolates the corrupted bit index.

### 2.2. Architectural Specifications
* **System Input:** Raw analog/digital sensor telemetry parsed and segmented into independent 4-bit arrays $D = \{D_1, D_2, D_3, D_4\}$.
* **System Output:** Pure, recovered 4-bit payload data alongside system telemetry logs containing operational status codes (`00`: Clean, `01`: Corrected, `10`: Severe Error).
* **Functional Actions:** Modulated the software architecture into 6 distinct, low-coupling service blocks (`ACT-01` through `ACT-06`) to ensure a highly scalable codebase.

### 2.3. Mathematical Validation Case
A standard execution trace was simulated against the original payload `1011`:
* **Encoding Stage:** Successfully produced the 7-bit codeword `0110011`.
* **Noise Injection:** Simulated a channel bit-flip at Position 5, changing the stream to `0110111`.
* **Syndrome Evaluation:** Recalculated parity to find $S = 101_2 = 5_{10}$. The matrix successfully targeted index 5, flipped it back to its valid state, and seamlessly recovered the clean data.

---

## 3. Team Member Contributions

| Member Name | Student ID | Assigned Tasks / Deliverables | Progress |
| :--- | :--- | :--- | :---: |
| **Huynh Anh Khoi** | SE193685 | - Research Question Drafting (`rq_explanation.md`)<br>- Project Domain Definition (`domain_scope.md`) | 100% |
| **Nguyen Nhat An** | SE192555 | - System Data Boundary Design (`system_input_output.md`)<br>- Modular Functional Table Specification (`processing_action_table.md`) | 100% |
| **Huỳnh Thị Thanh Nguyên** | SE183370 | - Mathematical Structural Analysis (`hamming_structure.md`)<br>- Test-case Implementation (`sample_error_case.md`)<br>- JSON Output Data Structuring (`system_output_schema.md`) | 100% |
| **Nguyen Duong Hoai An** | SE184221 | - Mathematical Structural Analysis (`hamming_structure.md`)<br>- Test-case Implementation (`sample_error_case.md`)<br>- JSON Output Data Structuring (`system_output_schema.md`) | 100% |

---

## 4. Plan for Week 2 (Literature Review & Search Strategy)
In Week 2, the team will transition into academic literature investigation to find relevant IEEE/ACM papers that support our research domain. 

* **Main Objective:** Conduct a systematic literature review to benchmark existing error-correction methods in IoT networks against our proposed Hamming implementation.
* **Files to be Created/Updated:**
    * `search_keywords.md`: To define the exact Boolean search strings (e.g., *“Hamming Code (7,4)” AND “IoT Sensor Transmission”*) used on IEEE Xplore, Google Scholar, and Scopus.
    * `paper_list.md`: To compile a curated table of relevant academic papers, including their titles, authors, publishers, core methodologies, and key takeaways for our project.
    * `week_02.md`: To document Week 2 progress, research insights, and team member workload distribution.