# 앱 아이콘(icon-192.png, icon-512.png)을 표준 라이브러리만으로 그린다.
import os, struct, zlib

BG = (31, 111, 235)
BALLS = [((0.36, 0.40), (245, 184, 0)), ((0.64, 0.40), (229, 72, 77)), ((0.50, 0.64), (47, 168, 79))]
R = 0.17


def pixel(x, y):
    for (cx, cy), col in BALLS:
        dx, dy = x - cx, y - cy
        d2 = dx * dx + dy * dy
        if d2 <= R * R:
            # 왼쪽 위 하이라이트로 공 느낌
            hx, hy = x - (cx - R * 0.35), y - (cy - R * 0.35)
            shine = max(0.0, 1 - (hx * hx + hy * hy) / (R * R * 0.35))
            return tuple(min(255, int(c + (255 - c) * shine * 0.6)) for c in col)
    return BG


def png(size, path):
    rows = []
    for j in range(size):
        row = bytearray([0])
        for i in range(size):
            row += bytes(pixel((i + 0.5) / size, (j + 0.5) / size))
        rows.append(bytes(row))
    raw = zlib.compress(b"".join(rows), 9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", raw))
        f.write(chunk(b"IEND", b""))


here = os.path.dirname(os.path.abspath(__file__))
for s in (192, 512):
    png(s, os.path.join(here, f"icon-{s}.png"))
