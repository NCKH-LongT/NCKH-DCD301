# Topic Proposal: Combinational Logic Design using Decoders

Class: SE1930

Group: 6

Team members:

Phạm Lê Nhật Minh-SE193155

Phan Trí Dũng-SE193224

Trần Minh Nhựt-SE193149

Lê Nguyễn Hoàng Lộc-SE193098

---

### 1. Topic Title

**Implementing Arbitrary Logic Functions using Decoders and OR Gates.**

### 2. Domain

This project belongs to the field of **Combinational Logic Circuit Design**. It will focus on a standardized and modular method for implementing any given Boolean function.

### 3. Problem Statement

In traditional digital logic design, implementing a Boolean function often requires a custom network of basic logic gates (AND, OR, NOT). This process can be complex, time-consuming, and difficult to modify. An alternative approach is to use standardized components like decoders. This project aims to explore and document the methodology of using a decoder combined with an OR gate to realize any logic function, thereby creating a more structured and flexible design process.

### 4. Research Questions

This study will be guided by the following research questions:

-   **RQ-02: How can a decoder be used in combination with OR gates to implement a logic function instead of using basic logic gates?**
    -   **RQ2.1:** What is the relationship between the outputs of a Decoder and the minterms of a logic function?
    -   **RQ2.2:** For a given Boolean function, how do you select the correct Decoder outputs to connect to the OR gate?
    -   **RQ2.3:** What are the advantages of implementing with a Decoder compared to designing with discrete AND/OR/NOT gates?

### 5. Scope

-   **In-Scope:**
    -   Analyze the theoretical foundation of decoders and their relationship to Boolean minterms.
    -   Develop a step-by-step procedure for implementing any `n`-variable logic function using an `n-to-2^n` decoder and OR gates.
    -   Provide concrete implementation examples (e.g., a 1-bit full adder).
    -   Compare the decoder-based method with traditional methods in terms of modularity, scalability, and ease of modification.

-   **Out-of-Scope:**
    -   Implementation using physical hardware or FPGAs.
    -   Analysis of timing, power consumption, or other physical characteristics.
    -   Sequential logic circuits (e.g., flip-flops, counters).

### 6. Expected Outcome

The primary outcome will be a technical report that clearly explains the principles and procedures for decoder-based logic design. The system's output will be a structured JSON object that describes the implementation details for a given logic function, following a predefined schema. This provides a machine-readable representation of the design.
