"""python -m codescan gen-qr "text" out.png | gen-code128 "ID-001" out.png | scan img.png"""
from __future__ import annotations

import argparse

from . import annotate, make_code128, make_qr, scan_image


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="codescan")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("gen-qr", "gen-code128"):
        s = sub.add_parser(name)
        s.add_argument("data")
        s.add_argument("out")
    s = sub.add_parser("scan")
    s.add_argument("image")
    s.add_argument("--annotate", help="сохранить картинку с контурами")
    a = p.parse_args(argv)

    if a.cmd == "gen-qr":
        print(make_qr(a.data, a.out))
    elif a.cmd == "gen-code128":
        print(make_code128(a.data, a.out))
    else:
        found = scan_image(a.image)
        if not found:
            print("Код не найден (проверьте поля вокруг кода и контраст).")
            return 1
        for r in found:
            print(f"{r.kind}: {r.data}")
        if a.annotate:
            print(annotate(a.image, found, a.annotate))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
