#!/usr/bin/env python3
"""BYTE Task 01: exact Base64 + Beaufort CYBR candidate, with round-trip tests.

Important: the key CYBR is *inferred* from desired BYTE prefix using
known plaintext and so the flag needs independent verification/acceptance.
"""
import base64
import re

CIPHERTEXT = "QkFJTntiQTczX1E4Ul9BcmhIQ19YNHlHY0R9"
EXPECTED_PREFIX = "BYTE"
KEY = "CYBR"


def beaufort_letters_only(source: str, key: str) -> str:
    """Classic Beaufort C = K - P mod 26; preserve case, punctuation, digits.

    Consume the key for A-Z or a-z only, *not* digits, braces, underscores.
    Beaufort is reciprocal (same function for encoding and decoding).
    """
    output = []
    j = 0
    for char in source:
        if char.isascii() and char.isalpha():
            offset = ord(char.upper()) - ord('A')
            keynum = ord(key[j % len(key)].upper()) - ord('A')
            transformed = chr(ord('A') + (keynum - offset) % 26)
            output.append(transformed if char.isupper() else transformed.lower())
            j += 1
        else:
            output.append(char)
    return ''.join(output)


def known_plaintext_key(cipher_prefix: str, plain_prefix: str) -> str:
    """Beaufort key letters K = (C + P) mod 26."""
    assert len(cipher_prefix) == len(plain_prefix)
    return ''.join(chr(ord('A') +
        (ord(cipher) - ord('A') + ord(plain) - ord('A')) % 26)
        for cipher, plain in zip(cipher_prefix, plain_prefix))


def main():
    intermediate = base64.b64decode(CIPHERTEXT, validate=True).decode('ascii')
    inferred_key = known_plaintext_key(intermediate[:4], EXPECTED_PREFIX)
    decoded = beaufort_letters_only(intermediate, inferred_key)
    roundtrip = beaufort_letters_only(decoded, inferred_key)
    print('Encrypted text:', CIPHERTEXT)
    print('Base64 result:', intermediate)
    print('Known-prefix key derived from BAIN -> BYTE:', inferred_key)
    print('Beaufort result:', decoded)
    print('Matches BYTE{...} format:', bool(re.fullmatch(r'BYTE\{[^{}]+\}', decoded)))
    print('Roundtrip verified:', roundtrip == intermediate)
    assert inferred_key == KEY
    assert decoded == 'BYTE{bY73_L8A_ChuKA_B4dLaV}'
    assert roundtrip == intermediate
    print('Status: exact reproducible candidate; no independent challenge checker confirmation.')

if __name__ == '__main__':
    main()
