# Paper List

Below is the structured list of selected references formatted in accordance with the **IEEE Citation Style** required for the Information Technology (IT) sub-committee.

### [1] Hierarchical Parallel Evaluation of a Hamming Code
* **Authors:** Francisco García-Carballeira, Javier Carretero, Fernando Pérez-Costeira
* **Year:** 2017
* **Source:** *Algorithms (MDPI)*, vol. 10, no. 2, p. 50.
* **DOI/Link:** https://www.mdpi.com/1999-4893/10/2/50
* **Core Problem:** Slow execution speeds of traditional sequential Hamming algorithms when processing massive data blocks or meeting strict real-time requirements.
* **Methodology:** Proposes a hierarchical parallel evaluation method to accelerate both error encoding and decoding phases.
* **Project Relevance:** Provides theoretical directions for optimizing decoding speeds, suggesting a transition from sequential to dual-core (e.g., ESP32) parallel execution paths.

### [2] Implementasi Deteksi Dan Koreksi Error Pada Komunikasi Serial Arduino Berbasis UART Dengan Metode Hamming Code
* **Authors:** Muhammad Rizki Maulana, Eko Setijadi, Gamantyo Hendrantoro
* **Year:** 2018
* **Source:** *Jurnal Pengembangan Teknologi Informasi dan Ilmu Komputer (J-PTIIK)*
* **DOI/Link:** https://j-ptiik.ub.ac.id/index.php/j-ptiik/article/view/3186
* **Core Problem:** Data transmission corruption in Arduino-to-Arduino serial UART communication channels caused by ambient electromagnetic interference.
* **Methodology:** Implements software-defined Hamming Code routines injected directly into the UART transmit/receive pipelines to evaluate single-bit flip recovery.
* **Project Relevance:** Highly relevant; maps closely to our objective of securing data streams over communication links using software-based codecs without extra physical hardware.

### [3] Application of Hamming Code for Error Control in Memory
* **Authors:** Do H. N. Tran et al.
* **Year:** 2022
* **Source:** *Journal of Technical Education Science*
* **DOI/Link:** https://jte.edu.vn/index.php/jte/article/view/1141
* **Core Problem:** Spontaneous bit-flips inside the volatile memory blocks of embedded IoT systems leading to data corruption or application crashes.
* **Methodology:** Designs a memory Error Correction Code (ECC) framework using systemic Hamming generation before committing data to storage units.
* **Project Relevance:** Validates the stability and accuracy of standard Hamming encoder/decoder modules for single-bit flips, backing our simulation's mathematical foundation.

### [4] Análisis del impacto de la inclusión de Códigos Correctores de Errores en un Sistema Empotrado basado en Arduino
* **Authors:** Carlos Andrés Hernández Suárez et al.
* **Year:** 2022
* **Source:** *ResearchGate Conference Paper*
* **DOI/Link:** https://www.researchgate.net/publication/363791708_Análisis_del_impacto_de_la_inclusión_de_Códigos_Correctores_de_Errores_en_un_Sistema_Empotrado_basado_en_Arduino
* **Core Problem:** Evaluating the hardware performance penalties and computational trade-offs when forcing lightweight microcontrollers to execute Error Correction Codes (ECC).
* **Methodology:** Measures data error rate reductions, correction accuracy, and overall processor throughput behaviors after embedding an ECC engine onto Arduino platforms.
* **Project Relevance:** Highlights potential real-world overhead bottlenecks, emphasizing the explicit need to monitor and log processing latencies in our own simulation testing suite.