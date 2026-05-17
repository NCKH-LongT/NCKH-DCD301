# RQ-09: Distinction between Combinational and Sequential Circuits. Why do Sequential Circuits require memory elements such as Latch or Flip-Flop?

## Comparison between Combinational and Sequential Circuits

| Attribute | Combinational Circuit | Sequential Circuit |
|---|---|---|
| **Definition** | The output depends strictly on the current values of inputs at that exact moment. | The output depends on both the current inputs and the previous states (operation history) of the circuit. |
| **Memory / Storage** | No memory elements integrated. | Built-in memory elements to store the current state. |
| **Feedback Loop** | No feedback path from outputs to inputs. | Features a feedback path returning signal from the memory elements' output to the combinational input logic. |
| **Clock Synchronization** | Completely asynchronous (no clock required). | Typically synchronous, utilizing a clock signal for unified state transitions (or controlled asynchronous). |
| **Storage Element** | None. | Uses Latches or Flip-Flops to preserve logic states. |
| **Applications** | Adders, Multiplexers, Decoders, encoders. | Counters, Registers, Memory Units (RAM/ROM), Finite State Machines (FSM). |

### Why do Sequential Circuits require Latch or Flip-Flop memory elements?
Sequential circuits operate chronologically across time cycles. Without memory elements to store the "current state", the circuit would lose its historical context and immediately act as a combinational circuit, reacting only to instantaneous input transitions. Storing state parameters is vital to execute multi-step operations and timed workflows.

---

## RQ9.1: What factors determine the output of a Combinational Circuit?

The outputs of a combinational logic circuit depend solely on:
- **The current physical input values (Current Inputs)** active at the logic gate terminals at that exact moment.

The combinational circuit **is completely independent of**:
- The prior operational states of the system (due to the lack of storage mechanisms).
- Synchronization clock pulses (outputs change immediately following the propagation delay of the physical logic gates).

---

## RQ9.2: How does the output of a Sequential Circuit depend on both the current input and the previous state?

In sequential logic design, the relationship governing the Output $Y(t)$, Input $X(t)$, and State $S(t)$ is categorized into two classic Finite State Machine (FSM) architectural models:

1. **Mealy FSM Model (Mealy Machine):**
   - The current output $Y(t)$ is a function of both the **current inputs $X(t)$** and the **current state $S(t)$** (which represents the accumulated history from previous cycles).
   - Formally: $Y(t) = f(X(t), S(t))$
   - *Characteristic:* The output can change immediately when inputs change, regardless of clock edge timing.

2. **Moore FSM Model (Moore Machine):**
   - The current output $Y(t)$ depends strictly and solely on the **current state $S(t)$**.
   - Formally: $Y(t) = g(S(t))$
   - *Characteristic:* The output is highly stable as it changes in perfect synchronization with clock edges (when flip-flop states transition).

### Real-world Greenhouse Context
When soil moisture drops below the threshold (current input), the system does not simply turn on the pump instantly. It references the current state (e.g., state is `WATERING` and has been active for 2 minutes). Guided by the state memory, the AgriAgent maintains the irrigation state instead of re-triggering, preventing component degradation.

---

## RQ9.3: What roles do Latch and Flip-Flop play in storing the state of a Sequential Circuit?

Latches and Flip-Flops act as **fundamental 1-bit memory elements** in digital logic. They support sequential operations via two primary roles:

1. **State Parameter Storage:**
   - Each Latch or Flip-Flop holds a single binary digit (`0` or `1`). By grouping multiple Flip-Flops together (forming a State Register), we can represent complex operational states for FSM-based controllers.

2. **Creating the Feedback Path:**
   - They capture the "Next State" signal computed by the combinational input logic, hold it, and feed it back to the input block as the "Present State" in the next clock cycle.

3. **Distinction in Synchronization Roles:**
   - **Latch:** **Level-sensitive**. It updates its stored state whenever the Enable signal is active. It operates asynchronously, making it susceptible to race conditions if not carefully controlled.
   - **Flip-Flop:** **Edge-triggered** (only updates on the rising or falling edge of the clock signal). Flip-flops are the building blocks of **Synchronous Sequential Circuits**, ensuring highly stable, unified state transitions across the entire system.
