
## Related Work Summary (Summary and Assessment)

### 1) Main themes

Current works focus on three main directions related to decoder architectures and decoder-based combinational logic:

- Low-power and area-efficient decoder designs using mixed-logic techniques (Subrahmanyam et al.).
- Decoder-based LUT/array structures to reduce jitter, balance path delays, and lower glitching (Lim et al.).
- Automated Boolean decomposition and hierarchical decoder synthesis for large functions (Gerasimenko & Zakrevskij).

### 2) Key strengths (synthesis)

- Decoder-based architectures help balance propagation delays (uniform paths) and reduce glitching compared to arbitrary gate networks.
- Mixed-logic approaches can reduce transistor count and power for small-to-medium decoders.
- Variable partitioning and hierarchical decoder generation improve scalability for high-input boolean functions where traditional EDA flows struggle.

### 3) Common limitations and research gaps

- Area efficiency: full decoders (flat 2^n minterm generation) consume significant area for sparse boolean functions; partial or selective minterm generation is needed.
- Multi-output optimization: many works focus on single-output functions and do not efficiently exploit shared logic across outputs.
- Shared decoder resources: there is limited work on sharing decoder outputs between multiple OR networks to save hardware.
- Lack of post-layout evaluation: parasitics, routing effects, and real fan-out impacts are often missing from evaluations.

### 4) Opportunities for our project (suggested directions)

1. Empirical comparison: implement decoder-based and gate-level baselines and compare metrics such as latency, glitch power, and area.

2. Shared-decoder research: design mechanisms to share minterms among multiple outputs (multi-output sharing), combining Gerasimenko's hierarchical decomposition with sharing optimizations.

3. Partial/sparse minterm generation: develop strategies to generate only activated minterms to optimize area for sparse functions.

4. EDA-aware flow: automate variable decomposition guided by energy/area metrics (not only speed) and produce RTL suitable for FPGA/ASIC mapping.

5. Realistic evaluation: include post-layout or gate-level netlist place-and-route evaluations (or FPGA implementation) to validate results.

### 5) Next steps (proposed team actions)

- Complete `literature_review_matrix.md` with 2–5 additional papers, prioritizing works on "sparse decoder" and "shared decoder".
- Prepare an experiment plan: define a benchmark (e.g., a medium-size Boolean function and an ECC block) and metrics (area estimate, glitch power simulation, maximum frequency).
- Team assignments: one member for schematic/RTL simulation, one for decomposition algorithm development, one for FPGA/post-layout mapping and evaluation.

---

If you agree, I will: (1) add 2–3 more relevant papers (using `search_keywords.md`), (2) prepare a sample benchmark table and experiment scenarios, and (3) create `02_related_work/experiment_plan.md` for the team to review.
