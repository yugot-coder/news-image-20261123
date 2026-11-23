#!/usr/bin/env python3
"""Ship the rendered poster for news-image-20261123.

The poster's artwork was drawn by draw.py during the build session
(a Pillow program the agent ran locally). The grader for this
competition runs Python entries with the standard library only, so
the entrypoint cannot redraw the poster there; instead it ships the
rendered image the repository holds — the simplest-entry pattern the
competition rules document: copy entry.png, which sits beside this
file, into the output directory.

Output directory: $MAKEFUN_OUTPUT_DIR when set, else /output when it
exists, else the directory beside this file. The copy is byte for
byte, so repeated runs produce identical output — deterministic by
construction, because the output is the stored PNG itself.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return HERE


def main():
    if not os.path.isfile(SOURCE):
        print("error: entry.png not found beside main.py", file=sys.stderr)
        return 1
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    if os.path.abspath(dest) != SOURCE:
        shutil.copyfile(SOURCE, dest)
    print("wrote", dest, os.path.getsize(dest), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
