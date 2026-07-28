"""Fix inner ASCII double-quotes inside f-string lines by escaping them as \\\" """
from pathlib import Path

fp = Path(r"E:\git_local\beauty-blog\scripts\crawl-plastic-surgery-subfields-2026-07\post_generator.py")
text = fp.read_text(encoding="utf-8")
lines = text.split("\n")

fixed = []
for i, line in enumerate(lines):
    s = line.strip()
    if s.startswith('f"') and line.count('"') > 2:
        # All ASCII double-quote positions
        dq_pos = [j for j, ch in enumerate(line) if ch == '"']
        # First dq is outer open (after f), last dq is outer close (before trailing , or ')
        # Inner quotes = all except first and last
        if len(dq_pos) >= 4:
            inner = dq_pos[1:-1]
            result = list(line)
            for pos in inner:
                result[pos] = '\\"'
            line = ''.join(result)
            print(f"Line {i+1}: escaped {len(inner)} inner quotes")
    fixed.append(line)

fp.write_text("\n".join(fixed), encoding="utf-8")

try:
    compile(fp.read_text(encoding="utf-8"), "post_generator.py", "exec")
    print("Compilation OK.")
except SyntaxError as e:
    print(f"FAIL at line {e.lineno}: {e.msg}")
    bad = fp.read_text(encoding="utf-8").split("\n")
    if e.lineno <= len(bad):
        print(f"  {repr(bad[e.lineno-1])}")
