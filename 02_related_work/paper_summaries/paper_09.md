# Paper 09 Summary

## Citation
- **Title:** Practical Use of Datakey Tokens in Electronic Lock Systems
- **Year:** 2025
- **Source:** Embedded Systems Publication (Embedded.com)
- **Link:** https://www.embedded.com/practical-use-of-datakey-tokens/

## Problem
- Modern access control systems must balance user convenience with strict hardware security, requiring reliable communication between credential readers and access control processors.

## Method
- The article surveys commercial electronic lock architectures, detailing how physical security tokens and multi-step credentials interface with embedded validation circuits.

## Dataset / Tools
- **Tools:** Commercial access control tokens, oscilloscope measurements, embedded protocol analyzers.

## Evaluation
- Evaluated based on commercial reliability metrics, response time, and physical tamper resistance.

## Results
- Outlined a safe, industry-standard operational flow for electronic validation circuits to prevent false-triggering.

## Limitations
- The paper focuses heavily on the physical token interfaces rather than detailing the underlying FSM transition math.

## Relevance to our topic
- It provides our group with real-world context on how hardware security systems operate outside of a classroom environment.

## Possible improvement
- We can model our FSM input behavior to replicate the secure debouncing and validation stages recommended in this industrial article.
