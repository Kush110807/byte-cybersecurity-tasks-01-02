# BYTE Cybersecurity — Cryptography and Steganography

This repository documents **the two challenges attempted for the submission**: Task 01 (Cryptography) and Task 02 (Steganography). No Binary Exploitation solution is included or claimed here.

## Results

| Challenge | Finding | Verification |
| --- | --- | --- |
| 01 — Cryptography | `BYTE{bY73_L8A_ChuKA_B4dLaV}` | **Candidate only:** reproducible two-stage decoding; organizer/checker has not independently confirmed the full flag |
| 02 — Steganography | `flag{g0t_1t_in_pLAin_sight}` | **Verified:** recovered text visible in the repaired PNG; image structure and CRC verified |

## Task 01: Base64 and Beaufort cipher

Given ciphertext:

```text
QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9
```

Base64 decoding gives:

```text
BAIN{bA73_Q8R_ArhHC_X4yGcD}
```

The required format is `BYTE{...}`, which is not met by Base64 alone. A second candidate layer is the *classic Beaufort cipher*. Assuming the four-character known plaintext `BYTE`, the corresponding four-character key is inferred from `BAIN` using `K = (P + C) mod 26`, yielding `CYBR`.

The Beaufort transform `P = (K - C) mod 26`, applied to letters only (preserving case and leaving digits/underscores/braces unchanged), gives:

```text
BYTE{bY73_L8A_ChuKA_B4dLaV}
```

The script reproduces that candidate and checks the reverse transformation:

```bash
python Task01_Cryptography/decode_and_audit.py
```

**Evidence limitation:** The key was inferred by fitting the known format, so both the prefix match and round trip are implementation checks, *not* independent evidence that this is BYTE's intended key. This result has not been confirmed by a challenge checker. See `Task01_Cryptography/analysis.md`.

## Task 02: Repairing a corrupted PNG

The supplied `challenge_corrupted.png` begins with the expected PNG signature, but its structure has two modifications:

1. The IHDR height claims **800 pixels**, while the header's stored CRC supports **850 pixels** for a width of 724.
2. A premature 12-byte IEND end marker occurs at offset **138377**, interrupting the image before the actual final marker.

After removing the premature marker and restoring the CRC-supported height, Pillow successfully loads the **724 × 850** image. The recovered lower strip displays the flag:

```text
flag{g0t_1t_in_pLAin_sight}
```

Reproduce from the included original image:

```bash
python -m pip install -r requirements.txt
python Task02_Steganography/repair_png.py
```

The output `challenge_repaired.png` can be checked against the included repaired reference or inspected visually. The crop `recovered_flag_crop.png` highlights the visible text.

## Tools and attribution

Python, its `base64`/`zlib`/`struct` libraries and Pillow were used for decoding and PNG repair. ChatGPT assisted with investigative approaches, implementation, debugging, and drafting documentation. This repository presents reproducible methods and distinguishes the unconfirmed Task 01 candidate from the verified Task 02 recovery.

Challenge details: https://bytesoc.dev/tasks/cybersecurity/
