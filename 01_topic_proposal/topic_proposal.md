1. Project Title
Research and Design of a Password Door Lock System using Finite State Machine (FSM)

2. Application Domain
Digital Logic Design, Sequential Circuits, Security Hardware.

3. Problem Statement
Traditional combinational logic systems cannot meet the requirements of a password door lock system because they only respond based on the current input. A door lock system requires the ability to remember the user's past actions to verify the correctness of a specific password sequence (e.g., the sequence 1 -> 0 -> 1 -> 1).

The challenge is to build a system capable of:

Processing data step-by-step.

Storing and tracking the user's correct password entry progress.

Making decisions to unlock or reject based on the input sequence.

Handling real-world hardware circuit issues such as timing behavior and glitches when the input signal changes unexpectedly between clock cycles.

4. Proposed Method
The system will be modeled and designed as a Sequential Circuit using a Finite State Machine (FSM).

Specifically, the research will implement in parallel and analyze the feasibility of two core FSM architectures:

Mealy Machine: A model whose output depends on both the current state and the current input.

Moore Machine: A model whose output depends only on the current state.

5. Expected Outcome

Successfully construct a State Diagram for the door lock system recognizing the password sequence 1011.

Perform an in-depth comparison between the Mealy and Moore models applied to the same problem (in terms of the number of states and differences in output logic).

Analyze and propose solutions to overcome timing and glitch phenomena during the state transitions of the circuit.
