### "Component" and "Logic Function" Table

Within the scope of this project, we do not use "sensors" and "actions" as in the sample AIoT project. Instead, we will define the "components" and "logic functions" that the system can implement.

| Component | Meaning / Function | Related Logic Function (Example) |
| :--- | :--- | :--- |
| **Inputs** | The input logic variables of the function. E.g., A, B, C. | `F(A, B, C)` |
| **Decoder** | The main component of the project. It has n inputs and 2^n outputs. Its function is to "decode" the input combination to activate a single output. Each output corresponds to a minterm. | A 3-to-8 Decoder has 3 inputs (A, B, C) and 8 outputs (Y0 to Y7). Output Y3 is activated when (A,B,C) = (0,1,1). |
| **OR Gate** | A supplementary component. Used to "sum" the necessary minterms from the Decoder's outputs to create the final logic function. | To create the function `F = m(1) + m(3) + m(5)`, we need a 3-input OR gate to connect the outputs Y1, Y3, Y5 of the Decoder. |
| **Output** | The final result of the logic function after implementation. | `F = 1` or `F = 0` depending on the values of the inputs A, B, C. |

**Example of a specific logic function:**
- **Function Name:** 1-bit Full Adder.
- **Inputs:** `A`, `B`, `Cin` (Carry-in).
- **Outputs:** `S` (Sum), `Cout` (Carry-out).
- **Implementation:**
    - `S(A, B, Cin) = Σm(1, 2, 4, 7)`
    - `Cout(A, B, Cin) = Σm(3, 5, 6, 7)`
- **Method:** Use a 3-to-8 Decoder.
    - To create `S`, connect the outputs `Y1, Y2, Y4, Y7` to a 4-input OR gate.
    - To create `Cout`, connect the outputs `Y3, Y5, Y6, Y7` to a 4-input OR gate.
