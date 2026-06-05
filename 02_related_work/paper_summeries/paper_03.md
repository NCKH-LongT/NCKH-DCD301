# Paper 03 Summary

## Citation

- **Paper Title:** Interactive Algorithms for the Verification of the Equality between Complex and Simplified Boolean-Algebra Expressions in Digital Decoders
- **Authors:** Tochukwu Arinze Ikwunne, Samuel Obiora Okide
- **Year:** 2020
- **Journal:** Review of Computer Engineering Research (Conscientia Beam)
- **DOI/Link:** https://archive.conscientiabeam.com/index.php/76/article/view/1476

## Problem

The fabrication of digital decoders relies heavily on accurate Boolean logic. However, manually evaluating and verifying that a complex Boolean expression (canonical sum of products) is logically equal to its simplified version (e.g., using Karnaugh maps) is tedious, time-consuming, and highly prone to human errors, which can lead to faulty logic circuit implementations.

## Method

The authors developed an interactive algorithm (implemented in C++) designed to automatically evaluate and verify the mathematical equivalence between complex and simplified Boolean expressions. The algorithm dynamically generates truth tables for both expressions and compares them to ensure they yield the exact same outputs for all possible input combinations.

## Dataset

The study utilizes truth table combinations, minterms, and Boolean expressions specifically derived from a standard BCD to Seven-Segment Display Decoder (4 input variables and 7 output segments: a, b, c, d, e, f, g).

## Evaluation

The verification system is evaluated based on its accuracy in matching the truth table outputs. It checks if the computational results of the unsimplified (minterm-based) equations perfectly align with the results of the simplified equations across all states.

## Results

The implemented algorithm successfully and accurately verified that the simplified Boolean expressions for the seven-segment decoder are mathematically and logically equal to their complex canonical minterm expressions. This computational approach effectively eliminates the risk of human error during logic verification.

## Limitations

The study is strictly algorithmic and focuses purely on mathematical truth-table verification for small-scale logic circuits (4-input decoders). It does not address the physical hardware synthesis, routing complexity, or area/power optimization when implementing these expressions in actual VLSI semiconductor architectures.

## Relevance to our topic

This paper strongly supports our theoretical foundations, specifically **RQ2.1** and **RQ2.2**. It provides algorithmic proof that any complex logic function can be perfectly represented by summing specific mathematical minterms. Since each output pin of a hardware Decoder represents exactly one minterm, this paper justifies our core methodology: we can accurately implement any Boolean function by identifying its minterms and selectively routing the corresponding Decoder output pins into an OR gate.

## Possible improvement

Our project can take this mathematical verification a step further into automated hardware implementation. While this paper only verifies the equations computationally, we can utilize these verified minterm sets to automatically generate a structured JSON schema. This schema will dictate the physical routing connections between the Decoder outputs and the OR gates, bridging the gap between theoretical verification and actual circuit synthesis.