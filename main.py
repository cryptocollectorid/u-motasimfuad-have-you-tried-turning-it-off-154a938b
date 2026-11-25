"""Have You Tried Turning It Off? — make.fun entry.

Writes one funny single line, spoken by a hopeless tech support agent
to a desperate customer, to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of
1 to 199 characters, not only white space, a single non-blank line.
"""

import os
import sys

ENTRY = (
    "Please hold while I Google your exact error message "
    "and read you the first result in a confident voice."
)

MAX_CHARS = 199


def validate_entry(text: str) -> None:
    """Fail loudly unless the entry satisfies the sealed gate."""
    if not text or not text.strip():
        raise ValueError("entry must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )


def write_entry(text: str, out_path: str = "/output/entry.txt") -> None:
    validate_entry(text)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # Round-trip read-back: confirm the file on disk is exactly the entry.
    with open(out_path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != text:
        raise ValueError("read-back mismatch: file does not hold the entry")
    print(f"Wrote {len(text)} characters to {out_path}")


def main() -> int:
    write_entry(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
