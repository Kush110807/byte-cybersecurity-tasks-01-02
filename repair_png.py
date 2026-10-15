#!/usr/bin/env python3
"""Reproduce repairs for BYTE Task 02's deliberately malformed challenge.png."""
from pathlib import Path
import struct
import zlib
from PIL import Image

here = Path(__file__).resolve().parent
src = Path(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else here / "challenge_corrupted.png"
dst = Path(__import__("sys").argv[2]) if len(__import__("sys").argv) > 2 else here / "challenge_repaired.png"
data = src.read_bytes()
signature = b"\x89PNG\r\n\x1a\n"
iend = b"\x00\x00\x00\x00IEND\xaeB\x60\x82"
if not data.startswith(signature):
    raise ValueError("Not a PNG signature")
if data[12:16] != b"IHDR":
    raise ValueError("Missing expected IHDR chunk")

first = data.find(iend)
last = data.rfind(iend)
if first < 0 or first == last:
    raise ValueError("Expected extra embedded IEND marker not found")
print(f"Removing invalid, embedded 12-byte IEND at file offset {first}")
data = data[:first] + data[first + len(iend):]
expected_crc = struct.unpack(">I", data[29:33])[0]
width, corrupt_height = struct.unpack(">II", data[16:24])
candidates = []
for height in range(1, 20001):
    ihdr = struct.pack(">II", width, height) + data[24:29]
    crc = zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF
    if crc == expected_crc:
        candidates.append(height)
if len(candidates) != 1:
    raise ValueError(f"Expected a unique CRC-confirmed height, got {candidates!r}")
height = candidates[0]
print(f"IHDR CRC verifies true dimensions: {width} x {height} (original reported {corrupt_height})")
data = data[:20] + struct.pack(">I", height) + data[24:]
assert zlib.crc32(data[12:29]) & 0xFFFFFFFF == expected_crc
dst.write_bytes(data)
with Image.open(dst) as img:
    img.load()
    print("Pillow validated repaired PNG dimensions:", img.size)
print("Saved", dst)
print("FLAG: Read text along bottom of the repaired image.")
