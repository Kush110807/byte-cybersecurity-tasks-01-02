# BYTE Cybersecurity — Cryptography & Steganography

I attempted the first two BYTE cybersecurity challenges. This repo contains the Python scripts, the original image, the repaired image and notes on how I approached each problem.

| Challenge | Result | Status |
| --- | --- | --- |
| Task 01 — Cryptography | `BYTE{bY73_L8A_ChuKA_B4dLaV}` | Possible flag |
| Task 02 — Steganography | `flag{g0t_1t_in_pLAin_sight}` | Recovered from the PNG |

## Task 01: Cryptography

The challenge text was:

```text
QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9
```

I tried Base64 first and got:

```text
BAIN{bA73_Q8R_ArhHC_X4yGcD}
```

It looked like a flag, but the prefix was wrong: the required format is `BYTE{...}`.

I then looked at a possible second layer using the **Beaufort cipher**. If `BAIN` is the encrypted prefix and `BYTE` is the expected plaintext, the Beaufort formula `K = (P + C) mod 26` gives the key `CYBR` (using A = 0). Repeating that key over letters, while leaving numbers and punctuation unchanged, produces:

```text
BYTE{bY73_L8A_ChuKA_B4dLaV}
```

This result can be recreated and reversed with the script. **I haven't had the full flag confirmed by BYTE.** The key was worked out using the known prefix, so the match alone isn't enough to prove it is the intended solution.

```bash
python decode_and_audit.py
```

More on the key calculation: [analysis.md](analysis.md).

## Task 02: Steganography

The supplied PNG only showed part of the picture. The issue turned out to be in the file structure, rather than the visible pixels:

- The image header said the height was **800 px**, but its saved CRC checksum matched **850 px**.
- An extra `IEND` (end-of-image) marker appeared in the file before the real ending.

The Python script removes that extra marker and fixes the height. The recovered **724 × 850** image shows the flag near the bottom:

```text
flag{g0t_1t_in_pLAin_sight}
```

```bash
python -m pip install -r requirements.txt
python repair_png.py
```

Files: [corrupted PNG](challenge_corrupted.png) · [repaired PNG](challenge_repaired.png) · [flag close-up](recovered_flag_crop.png)

![Flag visible after PNG repair](recovered_flag_crop.png)

## Tools

Python (`base64`, `struct`, `zlib`) and Pillow. ChatGPT helped me explore approaches, work through the scripts, debug issues and refine these notes.

[Original BYTE challenge](https://bytesoc.dev/tasks/cybersecurity/)
