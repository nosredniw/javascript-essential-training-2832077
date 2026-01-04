#!/usr/bin/env python3
import os
from pathlib import Path

root = Path.cwd()
skip_dirs = {'.git', 'node_modules', 'assets', 'Practice', 'dist', 'build'}
max_size = 500 * 1024
modified = []

text_ext_skip = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.exe', '.bin', '.zip', '.tar', '.gz', '.7z'}


def process_file(p: Path):
      try:
            data = p.read_text(encoding='utf-8')
      except Exception:
            return False
      lines = data.splitlines(True)
      changed = False
      new_lines = []
      for line in lines:
            if not line.startswith(' '):
                  new_lines.append(line)
                  continue
            # count leading spaces
            i = 0
            while i < len(line) and line[i] == ' ':
                  i += 1
            n = i
            groups = n // 2
            rem = n % 2
            new_n = groups * 3 + rem
            new_prefix = ' ' * new_n
            new_line = new_prefix + line[n:]
            if new_line != line:
                  changed = True
            new_lines.append(new_line)
      if changed:
            p.write_text(''.join(new_lines), encoding='utf-8')
            modified.append(str(p.relative_to(root)))
            return True
      return False


for p in root.rglob('*'):
      if p.is_dir():
            continue
      # skip paths containing skip dirs
      if any(part in skip_dirs for part in p.parts):
            continue
      if not p.is_file():
            continue
      if p.suffix.lower() in text_ext_skip:
            continue
      try:
            if p.stat().st_size > max_size:
                  continue
      except Exception:
            continue
      process_file(p)

print(f"Modified {len(modified)} files:")
for m in modified:
      print(m)
