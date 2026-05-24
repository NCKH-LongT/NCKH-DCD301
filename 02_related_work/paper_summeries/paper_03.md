# Paper 3: Automated EDA Optimization for Decoder-OR Combinational Logic Architectures

## 1. Publication Information

- **Paper Title:**  
  *Automated Synthesis of Combinational Logic Using Decoders and Multiplexers for Post-Quantum Cryptography Hardware*

- **Authors:**  
  M. Gerasimenko and A. Zakrevskij

- **Year of Publication:**  
  2022

- **Journal / Conference:**  
  ScienceDirect - Microprocessors and Microsystems  
  (Scopus Indexed, Q2/Q3 ranking in embedded systems and microelectronics)

- **DOI / Link:**  
  https://doi.org/10.1016/j.micpro.2022.104567

---

# 2. Research Background

The rapid development of **Post-Quantum Cryptography (PQC)** introduces new challenges for hardware implementation.

PQC algorithms typically require:

- Extremely complex combinational logic
- Large Boolean functions
- High parallelism
- Fast hardware execution
- Efficient ASIC and FPGA mapping

Many PQC circuits involve Boolean functions with:

\[
n > 8
\]

input variables, making manual logic implementation impractical.

Traditional combinational logic synthesis methods often rely on:

- NAND-NAND structures
- NOR-NOR structures
- Standard gate-level optimization

However, these approaches are not well optimized for:

- Array-based decoder architectures
- Hierarchical minterm generation
- Structured logic decomposition

As a result, automated synthesis techniques specifically designed for decoder-based architectures are increasingly important.

---

# 3. Problem Statement

The paper addresses the following major issue:

> Existing EDA synthesis tools are inefficient when generating large decoder-based combinational logic structures for complex Boolean functions used in Post-Quantum Cryptography hardware.

The main challenges include:

- Very large input variable counts
- Exponential growth of truth tables
- Difficult manual decoder design
- Inefficient hardware mapping
- Poor optimization for structured decoder arrays

Conventional EDA tools generally optimize circuits toward:

- NAND-only implementations
- NOR-only implementations

instead of efficiently exploiting:

- Decoder-OR architectures
- Hierarchical logic decomposition
- Structured modular hardware

This limits performance and scalability for modern PQC systems.

---

# 4. Proposed Methodology

The authors propose a new **Boolean Decomposition Algorithm** for automated combinational logic synthesis using decoders and multiplexers.

---

## 4.1 Core Concept

Instead of synthesizing the entire Boolean function directly as a large gate-level network, the algorithm:

1. Analyzes the truth table automatically.
2. Divides input variables into smaller groups.
3. Maps each group into low-level decoders.
4. Combines intermediate outputs using hierarchical OR structures.

This creates a modular and scalable hardware architecture.

---

# 5. Boolean Decomposition Strategy

The proposed synthesis flow uses hierarchical decomposition.

---

## 5.1 Input Variable Partitioning

Large Boolean functions are divided into fixed-size variable groups.

Examples include:

- 3-variable groups
- 4-variable groups

These groups are independently processed by smaller decoders.

---

## 5.2 Low-Level Decoder Generation

The grouped variables are mapped into standard decoder blocks such as:

- \(3 \times 8\) decoders
- \(4 \times 16\) decoders

These decoders generate local minterms efficiently.

---

## 5.3 Hierarchical OR Combination

After local minterm generation:

- Outputs are combined using multiple layers of OR gates.
- The OR network is organized hierarchically.
- Large Boolean functions are reconstructed incrementally.

This reduces synthesis complexity compared to flat logic generation.

---

# 6. Architecture Characteristics

The synthesized architecture has several important properties.

---

## 6.1 Modular Design

The generated circuit structure is highly modular because:

- Decoder blocks are reusable
- OR stages are hierarchical
- Functional partitions are isolated

This simplifies large-scale hardware implementation.

---

## 6.2 FPGA and ASIC Compatibility

The architecture can be mapped efficiently onto:

- ASIC structured logic arrays
- FPGA lookup-table resources
- Reconfigurable logic fabrics

This improves hardware deployment flexibility.

---

## 6.3 Structured Hardware Layout

Compared to random gate-level synthesis:

- Routing becomes more predictable
- Timing analysis becomes easier
- Hardware regularity improves significantly

---

# 7. Experimental Results

The proposed algorithm was compared with traditional Boolean decomposition and synthesis methods.

---

## 7.1 Faster Synthesis Time

The proposed method achieved:

- Approximately **50% reduction in synthesis time**

compared to classical decomposition algorithms.

This improvement comes from:

- Structured decomposition
- Reduced optimization complexity
- Modular synthesis flow

---

## 7.2 Improved Hardware Mapping

The generated circuits showed excellent compatibility with:

- FPGA logic blocks
- ASIC array-based architectures

The modular decoder structure simplifies direct hardware mapping.

---

## 7.3 Scalable Logic Construction

The hierarchical architecture successfully handled:

- Large Boolean functions
- High-input-variable systems
- PQC-oriented combinational logic

more effectively than conventional flat synthesis methods.

---

# 8. Contributions of the Paper

The paper provides several important contributions to EDA and combinational logic synthesis.

## Main Contributions

1. Proposed a new Boolean decomposition algorithm for decoder-based logic synthesis.

2. Automated the generation of hierarchical decoder-OR architectures.

3. Reduced synthesis time significantly.

4. Improved compatibility with FPGA and ASIC hardware mapping.

5. Demonstrated scalable combinational logic synthesis for PQC applications.

---

# 9. Research Gap

Although the proposed approach shows strong performance improvements, several limitations remain.

---

## 9.1 Single-Output Optimization Limitation

The current algorithm is primarily optimized for:

- Single-output Boolean functions

However, real-world digital systems often contain:

- Multi-output combinational functions

where multiple outputs share common input variables and logic structures.

---

## 9.2 Lack of Shared Decoder Optimization

The current synthesis method does not efficiently share decoder outputs between multiple OR networks.

As a result:

- Hardware duplication occurs
- Redundant decoder structures are generated
- Area efficiency decreases

This becomes problematic in large-scale practical systems.

---

## 9.3 Scalability for Ultra-Large Systems

Although hierarchical decomposition improves scalability, challenges still remain for:

- Extremely large PQC circuits
- Deep hierarchical logic trees
- Very high fan-out OR networks

---

# 10. Conclusion

This paper presents an automated decoder-based combinational logic synthesis algorithm for Post-Quantum Cryptography hardware.

By using:

- Boolean decomposition
- Hierarchical decoder structures
- Structured OR-based reconstruction

the proposed method successfully improves:

- Synthesis speed
- Hardware modularity
- FPGA/ASIC mapping efficiency

The work is highly relevant for:

- EDA tool optimization
- FPGA synthesis
- ASIC implementation
- Post-Quantum Cryptography accelerators
- Large-scale combinational logic systems

However, further research is still required to optimize multi-output function sharing and reduce redundant hardware generation.

---

# 11. Suggested Future Work

Possible future research directions include:

- Multi-output logic sharing optimization
- Shared decoder resource allocation
- AI-assisted Boolean decomposition
- FPGA-aware decoder synthesis
- Low-power hierarchical OR structures
- Parallel synthesis algorithms
- Adaptive decomposition strategies for sparse logic functions

---