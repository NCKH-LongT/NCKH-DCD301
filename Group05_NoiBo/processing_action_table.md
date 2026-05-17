# System Processing Action Table (Compact View)

This table outlines the core functional modules of the Hamming (7,4) IoT reliability system. Actions have been encapsulated to reflect high-level software engineering processes and system services.

| Action ID | Module / Action Name | Technical Description | Inputs | Outputs |
| :---: | :--- | :--- | :--- | :--- |
| **ACT-01** | `Acquire_and_Format` | Reads physical signals from IoT sensors, digitizes the telemetry, and chunks the bitstream into fixed 4-bit payload blocks. | Raw analog/digital sensor signals | 4-bit data arrays `[d1, d2, d3, d4]` |
| **ACT-02** | `Encode_Payload` | Calculates the 3 parity bits via XOR logic and maps them with the 4-bit payload into a complete 7-bit Hamming codeword structure. | 4-bit data arrays | 7-bit encoded Codewords |
| **ACT-03** | `Transmit_Data` | Modulates and broadcasts the 7-bit codewords over the wireless IoT communication channel. | 7-bit encoded Codewords | Wireless electromagnetic signals |
| **ACT-04** | `Receive_Data` | Captures incoming radio signals at the gateway and demodulates them back into a raw 7-bit stream. | Incoming radio signals | 7-bit received stream (potentially noisy) |
| **ACT-05** | `Process_and_Decode` | Generates the Syndrome vector to detect errors. If an error exists, it flips the corrupted bit to correct it, then strips parity bits to recover the original payload. | 7-bit received stream | Clean 4-bit original data arrays |
| **ACT-06** | `Store_and_Monitor` | Reassembles the 4-bit chunks into standard data types, persists records to the database, and pushes metrics to the dashboard. | Clean 4-bit arrays + Error logs | Database Records + Dashboard updates |