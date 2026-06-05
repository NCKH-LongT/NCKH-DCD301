# Research Gap & Contributions

## 1. How Previous Studies Addressed the Problem
Recent research has approached logic synthesis and decoder optimization from three distinct angles:
- **Algorithmic Verification:** Ikwunne & Okide (2020) developed interactive algorithms to mathematically verify the equality between complex Boolean expressions and simplified equations, eliminating human error in truth-table evaluation.
- **Hardware Optimization:** Balobas & Konofaos (2025) optimized CMOS decoders at the transistor level using Three-Transistor Logic (3TL), significantly reducing active/standby power and propagation delays compared to conventional static CMOS.
- **Boolean Decomposition:** Costamagna & De Micheli (2023) proposed the Don't Knows-Aware Disjoint Support Decomposition (DK-DSD) algorithm to systematically partition variables and synthesize partially-specified Boolean functions, recovering exact functional accuracy for Machine Learning models.

## 2. Limitations of Previous Studies
Despite these advancements, several critical gaps remain:
- **Disconnection between Verification and Hardware Synthesis:** Existing verification algorithms are purely mathematical; they do not automatically translate the verified minterms into a machine-readable physical routing schema.
- **Computational Overhead in Decomposition:** Advanced decomposition algorithms like DK-DSD suffer from high computational complexity ($O(n^2N)$) and rely heavily on external approximate circuits to function, making them difficult to map directly to structured hardware without bottlenecks.
- **Flat vs. Hierarchical Integration:** While low-level transistor optimizations (like 3TL) exist, there is a lack of high-level workflows that automatically integrate these efficient decoder blocks into multi-stage OR-gate networks for irregular Boolean expressions.

## 3. The Research Gap
*Existing logic synthesis methodologies mainly focus on low-level transistor optimization or computationally heavy mathematical decomposition. Limited attention has been given to creating a fully automated, machine-readable pipeline (e.g., JSON schema) that translates verified Boolean minterms directly into structurally optimized Decoder-OR hardware configurations.*

## 4. Proposed Improvements
Our team will bridge the gap between mathematical minterm verification, decomposition, and hardware synthesis by:
- Standardizing the minterm-to-decoder mapping process into an automated, machine-readable **JSON routing schema**.
- Utilizing the theoretical foundations of variable decomposition to systematically segment inputs into discrete blocks, routing them directly into Decoders and OR gates to avoid the computational overhead of searching for arbitrary gate nodes.

## 5. Expected Contributions
1. A systematic, automated procedure to translate any Boolean function into a Decoder-OR hardware configuration.
2. The creation of a JSON-based routing schema that acts as a bridge for EDA tools.
3. A theoretical demonstration of hardware efficiency (transistor count reduction and modularity) by replacing discrete gate networks with an optimized Decoder-OR architecture.