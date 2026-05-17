# System Output Schema

Describes the JSON output structure of the Hamming (7,4) transmission and error-correction simulation system.

```json
{
  "input_data": "1011",           
  // Original 4-bit data before encoding (String)

  "encoded_data": "0110011",      
  // 7-bit encoded data after parity bits are inserted (String)

  "received_data": "0110111",     
  // 7-bit data received at the destination (String)

  "syndrome": "101",              
  // Calculated binary syndrome value (String)

  "error_detected": true,         
  // Indicates whether an error is detected (Boolean)

  "error_position": 5,            
  // Position of the erroneous bit, 0 if no error exists (Integer)

  "corrected_data": "0110011",    
  // 7-bit data after error correction (String)

  "extracted_data": "1011",       
  // Successfully recovered original 4-bit data (String)

  "status": "Error detected and corrected successfully"
  // System status message (String)
}
```