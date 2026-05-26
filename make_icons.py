import struct, zlib, os

BG = (26, 35, 50)
FG = (212, 165, 116)

def write_png(path, w, h, pixels):
    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            r, g, b = pixels[y * w + x]
            raw += bytes([r, g, b])
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n')
        f.write(chunk(b'IHDR', struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)))
        f.write(chunk(b'IDAT', zlib.compress(raw, 9)))
        f.write(chunk(b'IEND', b''))

def make_icon(size, maskable=False):
    px = [BG] * (size * size)
    s = size / 512.0

    # Two filled "quote dots" centered horizontally
    r = int(70 * s)
    cy = int(200 * s)
    cx1 = int(190 * s)
    cx2 = int(322 * s)

    # Comma tails: each dot has a triangular tail extending down-left
    tail_h = int(110 * s)
    tail_w = int(70 * s)

    inset = int(40 * s) if maskable else 0

    for y in range(size):
        for x in range(size):
            if maskable and (x < inset or y < inset or x >= size - inset or y >= size - inset):
                continue
            # Circles
            d1 = (x - cx1) ** 2 + (y - cy) ** 2
            d2 = (x - cx2) ** 2 + (y - cy) ** 2
            if d1 <= r * r or d2 <= r * r:
                px[y * size + x] = FG
                continue
            # Tails: trapezoid from circle bottom curving down-left
            for cx in (cx1, cx2):
                top_y = cy
                bot_y = cy + tail_h
                if top_y <= y <= bot_y:
                    t = (y - top_y) / max(1, (bot_y - top_y))
                    # Tail starts at width = 2*r at top, narrows toward bottom-left
                    left = cx - r + int((1 - t) * 0) - int(t * tail_w)
                    right = cx + r - int(t * (2 * r - 8 * s))
                    if left <= x <= right:
                        px[y * size + x] = FG
    return px

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for size in (192, 512):
    write_png(f'icon-{size}.png', size, size, make_icon(size))
    print(f'wrote icon-{size}.png')

# Maskable: leave safe zone
write_png('icon-maskable-512.png', 512, 512, make_icon(512, maskable=True))
print('wrote icon-maskable-512.png')
