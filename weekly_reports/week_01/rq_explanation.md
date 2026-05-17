1. Introduction

- In sequential circuits, the output depends not only on the current input but also on the previous state of the system. The two most common Finite State Machine (FSM) models are:
+ Mealy Machine
+ Moore Machine

- These two models generate outputs differently, leading to differences in:
+ response speed
+ signal stability
+ glitch generation capability
+ timing behavior

- In particular, when the input changes unexpectedly between clock cycles, the Mealy machine and Moore machine will exhibit different output behaviors.

RQ-04 Analyze the difference in output signal behavior between the Mealy and Moore models when the input signal changes unexpectedly between clock cycles.

*What is a Mealy Machine?

- A Mealy Machine is a type of FSM where the output depends on:
• Current state
• Current input
Output = f(State, Input)

- Meaning:
• When the input changes → the output can change immediately
• No need to wait for the next clock edge
• Responds quickly to input signals

Simple example

Assume:
- Input = button
- Output = LED light
- Clock = “tick-tock” sound

If the user presses the button before the next clock arrives:
→ The LED light may turn on immediately.
That is a characteristic of Mealy.

-Advantages and Disadvantages of Mealy

Advantages
• Fast response
• Requires fewer states
• Hardware optimization

Disadvantages
• Prone to glitches
• Unstable output
• Sensitive to input changes

*What is a Moore Machine?

A Moore Machine is a type of FSM where the output depends only on:
• Current state

Output = f(State)

- Meaning:
• Input changes do not immediately change the output
• Output changes only when the state changes
• State changes only at the clock edge

- Simple example

Assume:
- The user presses the button
- The system has not yet reached the next clock
→ The LED light still does not turn on.

When the clock edge arrives:
- The new state is updated
- The output changes afterward

- Advantages and Disadvantages of Moore

Advantages
• Stable output
• Fewer glitches
• Safer for digital systems

Disadvantages
• Slower response than Mealy
• May require more states

RQ4.1: What factors does the output of a Mealy machine depend on?

The output of a Mealy machine depends on:
1. Current state
2. Current input

Output = f(State, Input)

Example operation table

![alt text](image.png)<img width="781" height="89" alt="image" src="https://github.com/user-attachments/assets/08197e5d-da5c-495a-988f-233fcffb6502" />


If the system is currently at:
- State S0
- Input = 0
- Output = 0

When the input changes:
0 → 1

the output can immediately change:
0 → 1

without waiting for the clock.

Conclusion RQ4.1

depends on state
depends on input
fast response
prone to glitches

RQ4.2: What factors does the output of a Moore machine depend on?

The output of a Moore machine depends only on:
1. Current state

Output = f(State)

Example table

![alt text](image-1.png)<img width="733" height="90" alt="image-1" src="https://github.com/user-attachments/assets/4c1017ea-74d4-45ac-8e60-b4898e741866" />


Assume:
- the system is currently at S0
- output = 0

If the input changes:
0 → 1

the output still remains 0 until a clock edge occurs.

After the clock edge:
- the state changes to S1
- the output changes to 1

Conclusion RQ4.2

depends only on state
does not change immediately when the input changes
more stable
fewer glitches

RQ4.3 Why can a Mealy machine generate momentary false outputs?

A momentary false output (glitch) is:

an incorrect output that appears for a very short period of time

- occurs temporarily
- then disappears automatically
- This is a common phenomenon in sequential circuits

The phenomenon of temporary incorrect outputs (momentary false outputs or glitches) in a Mealy machine originates from its hardware architecture.

Direct Combinational Path: In the Mealy model, the input X(t) is connected directly to the combinational logic block that generates the output Y(t). This combinational circuit is not synchronized by the clock signal.

Asynchronous changes: If the input signal changes (toggles) between two active clock edges, the combinational logic block reacts immediately to this change.

Propagation Delay: The logic gates inside the combinational circuit have different delays. When the input changes, signals propagate through different paths at different times, leading to temporary race conditions.

Consequence: Before the new input signal becomes completely stable and waits for the next clock cycle, the output Y(t) may generate unwanted spikes (glitches) for a very short period of time (a few nanoseconds). This is extremely dangerous if this output is used as an asynchronous control signal for another module.
