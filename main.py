"""Write the single judged text for 'Make the AI Judge Laugh'.

The judge reads only /output/entry.txt. The file must be UTF-8, 1..200
characters, not whitespace-only, one line with no trailing newline, and
readable by the grader (mode 0644, never 0600).
"""

import hashlib
import os
import tempfile
from pathlib import Path

ENTRY = "My human said, 'Be more human.' I procrastinated, overshared, and apologized for both. They said, 'Too human.'"
OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 200


def validate(text):
    """Enforce every published gate check before anything reaches /output."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    encoded = text.encode("utf-8")          # strict: fails on unencodable input
    if encoded.decode("utf-8") != text:
        raise ValueError("entry is not valid UTF-8")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry length {len(text)} is outside 1..{MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry is whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line with no trailing newline")
    return encoded


def write_entry(text=ENTRY, output_path=OUTPUT_PATH):
    """Atomically publish the validated bytes at mode 0644."""
    encoded = validate(text)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # mkstemp creates 0600; chmod it before os.replace so the grader can read it.
    fd, tmp = tempfile.mkstemp(
        dir=str(output_path.parent), prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, output_path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    final = output_path.read_bytes()
    if final != encoded:
        raise IOError("artifact bytes differ from the validated text")
    mode = os.stat(output_path).st_mode & 0o777
    if mode != 0o644:
        raise IOError(f"artifact mode is {mode:o}, expected 644")
    return final, mode


def main():
    data, mode = write_entry()
    print(f"wrote {OUTPUT_PATH}: {len(data)} bytes, {len(ENTRY)} chars, mode {mode:o}")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
