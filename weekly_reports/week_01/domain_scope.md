* Password door lock systems are an ideal application domain for studying Finite State Machines (FSMs) because the system naturally operates using:

-step-by-step processing,
-state transitions,
-memory of previous inputs,
-sequential behavior.

-Unlike combinational logic systems that depend only on current inputs, a password lock system must remember previous user inputs to determine whether the entered password is correct.

Therefore, the system is essentially a sequential circuit and can be effectively modeled using:

-Mealy Machine,
-Moore Machine,
-Finite State Machine (FSM).


* Why is the Password Door Lock System suitable for FSM?
The Password Door Lock System is suitable for a Finite-state machine because the system operates step-by-step and needs to remember previous states to validate the password.
When the user enters each character:
1 → 0 → 1 → 1
- the system must:
+ remember how far the correct input has progressed,
+ transition to the next state,
+ decide whether to unlock the door or reject the input.

- This matches the nature of:
+ Sequential Circuit: output depends on the current input and previous state,
+ FSM: the system operates using states and state transitions.

- In addition, this domain is also very suitable for studying:
+ Mealy Machine,
+ Moore Machine,
+ timing behavior,
+ glitches when inputs change unexpectedly between clock cycles.
