# Password Door Lock System using FSM

##  Sensor – Meaning – Related Actions Table

| Sensor / Input                 | Meaning                                         | Related Actions                   |
|---|---|---|
| **Keypad Input**               | Receive password characters from user           | Check Password, Update State      |
| **Clock Signal**               | Synchronize FSM operation with clock signal     | State Transition, Synchronize Output  |
| **Reset Button**               | Return system to initial state                  | Reset Input, Lock Door            |
| **Door Sensor**                | Check if door is open or closed                 | Unlock Door, Lock Door            |
| **Password Buffer**            | Store entered character strings                 | Compare Password, Clear Buffer    |
| **Current FSM State**          | Monitor current state of the system             | Generate Output, Change State     |
| **Timeout Timer**              | Check password entry time                       | Reset Session, Trigger Timeout    |
| **Attempt Counter**            | Count number of failed attempts                 | Trigger Alarm, Lock System        |
| **Confirm/Input Enter Signal** | Confirm user has finished entering password     | Validate Password                 |
| **Glitch Detector**            | Detect false output or abnormal signal          | Trigger Warning, Prevent False Unlock |

---

#  FSM Real-world Example

| State     | Sensor/Input    | Action                            |
|---        |---              |---                                |
| S0_IDLE   | Keypad Input    | Transition to password input state |
| S1_INPUT  | Clock Signal    | Read next character               |
| S2_CHECK  | Password Buffer | Compare password                  |
| S3_UNLOCK | Door Sensor     | Unlock door                       |
| S4_ERROR  | Attempt Counter | Error notification / Alarm        |

---

#  Short version for slide

| Sensor          | Meaning            | Action         |
|---              |---                 |---             |
| Keypad          | Enter password     | Check Password |
| Clock           | Synchronize FSM    | Update State   |
| Reset           | Restart system     | Reset System   |
| Door Sensor     | Check door         | Lock/Unlock    |
| Timer           | Limit time         | Timeout        |
| Attempt Counter | Count failed tries | Alarm          |

---

#  Important points for Mealy vs Moore topic

## In Mealy FSM

Output depends on:
- Current State
- Current Input

=> Sudden Keypad Input change can cause:
- glitch
- false unlock

---

## In Moore FSM

Output depends only on:
- Current State

=> More stable, fewer false outputs.
