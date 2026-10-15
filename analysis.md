# Task 01 — key derivation and verification

**Input:** `QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9`  
**Base64 decoded:** `BAIN{bA73_Q8R_ArhHC_X4yGcD}`  
**Candidate after Beaufort/CYBR:** `BYTE{bY73_L8A_ChuKA_B4dLaV}`

The original string fits the Base64 character set. Its first decoding is not the required `BYTE{...}` flag.

For a classic Beaufort cipher, letters are numbered A=0 ... Z=25. The transformation is `P=(K-C) mod 26`; equivalently, for a known plaintext character, `K=(P+C) mod 26`.

| Intermediate cipher | B | A | I | N |
|---|---|---|---|---|
| Required prefix | B | Y | T | E |
| Derived key | C | Y | B | R |

Applying the repeating key `CYBR` to letters only, without advancing it on braces, underscores or digits, yields the candidate. The same transformation reverses it perfectly.

**Limitation:** An expected prefix is known in advance, and a key can be fitted to that prefix. Matching `BYTE` and passing a round trip therefore do not prove that Beaufort/CYBR was the intended solution. No independent BYTE checker result is supplied for Task 01.

Run: `python Task01_Cryptography/decode_and_audit.py`.
