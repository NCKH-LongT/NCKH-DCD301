# Paper 10 Summary

## Citation
- **Title:** Hardware-based Security for IoT Edge Devices: Electronic Access Control
- **Authors:** Y. Liu, et al.
- **Year:** 2017
- **Source:** 2017 IEEE 60th International Midwest Symposium on Circuits and Systems (MWSCAS)
- **Link:** https://ieeexplore.ieee.org/document/8053155/

## Problem
- Asynchronous input changes in edge devices can introduce signal glitches and timing hazards into FSM logic, potentially allowing attackers to bypass lock security through clock glitches.

## Method
- The authors analyze hardware-level timing vulnerabilities in electronic access circuits and propose synchronous filtering structures to mitigate input noise.

## Dataset / Tools
- **Tools:** Timing analysis software, signal hazard simulators.

## Evaluation
- Evaluated by injecting intentional timing misalignments and measuring whether the access FSM entered illegal states.

## Results
- The proposed filtering and synchronization logic successfully eliminated transitional glitches, ensuring the FSM remained stable under harsh input fluctuations.

## Limitations
- Adding extensive synchronization flip-flops introduces slight input latency to the overall circuit response.

## Relevance to our topic
- This paper directly addresses the "glitches when inputs change unexpectedly between clock cycles" mentioned in our project description, giving us a clear path to study timing behaviors.

## Possible improvement
- We can simulate an asynchronous input change for our password lock and design a synchronizer circuit to prove we can prevent these security vulnerabilities.
