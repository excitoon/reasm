# `reasm`

## Install

```bash
pip3 install reasm
```

## Tools

### MZ

#### `mzinfo`

Shows information about executable in JSON format. In particular, it determines compiler and memory model.

```
% mzinfo --help
usage: mzinfo [-h] [--hex] [--fast] [--content] [--indent INDENT] [--max-width MAX_WIDTH] path

positional arguments:
  path                  path to executable file

options:
  -h, --help            show this help message and exit
  --hex                 hexadecimal output
  --fast                skip long checks
  --content             output content
  --indent INDENT       indent
  --max-width MAX_WIDTH
                        max width
```

Useful flags:

- `--hex` is most useful for humans, the tool outputs JSON with numbers as decimals by default;
- `--content` outputs full content of sections (segments), it may produce too large outputs;
- `--fast` removes checks for compiler at the moment, it is currently made in non-efficient way and it shall be rewritten using Aho-Corasick algorithm, which shall also reduce code size;
- `--indent` controls output JSON indentation;
- `--max-width` formats lists in JSON to the specified width as they may be long and inconvenient to read, it is also worth mentioning that looking for a reliable way to apply such formatting, it was made it such way that it has negligible chance of failing (giving an error), so when running from a tool, `--max-width=0` is preferred. It is not quite efficient too but it takes only ~20ms on typical executable and can be rewritten using API which can work with deque-like strings.

#### `mzfix`

The tool can manipulate executables on low level. The following operations are supported:

- `set-entry-point <cs> <ip>`;
- `set-stack <ss> <sp>`;
- `set-minimum-allocation <size>`;
- `set-maximum-allocation <size>`;
- `set-relocations <offset>...`;
- `strip-tail`;
- `add-text-size <size>`;
- `fix-text-size [<fill>]`;
- `fill-last-page [<fill>]`;
- `preallocate-minimum [<fill>]`.

Example:

```
% mzfix XEEN.DAT XEEN0.DAT fill-last-page 'last-page\0' # Filled text up to nearest (next) page.
% mzfix XEEN0.DAT XEEN1.DAT add-text-size 128           # Increased text size by 8 paragraphs.
% mzfix XEEN1.DAT XEEN2.DAT fix-text-size 'new-page\0'  # Added space according to that size.
% xxd -g 4 -c 32 XEEN2.DAT | tail
0005c140: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000  ................................
0005c160: c7065c00 504b8cd8 05100050 b8000050 cb6c6173 742d7061 6765006c 6173742d  ..\.PK.....P...P.last-page.last-
0005c180: 70616765 006c6173 742d7061 6765006c 6173742d 70616765 006c6173 742d7061  page.last-page.last-page.last-pa
0005c1a0: 6765006c 6173742d 70616765 006c6173 742d7061 6765006c 6173742d 70616765  ge.last-page.last-page.last-page
0005c1c0: 006c6173 742d7061 6765006c 6173742d 70616765 006c6173 742d7061 6765006c  .last-page.last-page.last-page.l
0005c1e0: 6173742d 70616765 006c6173 742d7061 6765006c 6173742d 70616765 006c6173  ast-page.last-page.last-page.las
0005c200: 6e65772d 70616765 006e6577 2d706167 65006e65 772d7061 6765006e 65772d70  new-page.new-page.new-page.new-p
0005c220: 61676500 6e65772d 70616765 006e6577 2d706167 65006e65 772d7061 6765006e  age.new-page.new-page.new-page.n
0005c240: 65772d70 61676500 6e65772d 70616765 006e6577 2d706167 65006e65 772d7061  ew-page.new-page.new-page.new-pa
0005c260: 6765006e 65772d70 61676500 6e65772d 70616765 006e6577 2d706167 65006e65  ge.new-page.new-page.new-page.ne
```

### NE

Under construction.

### LE/LX

Under construction.

### PE

Under construction.

### ELF

Under construction.

### Mach-O

Under construction.

### OMF

Under construction.

### RES

Under construction.

### COFF

Under construction.

### CV

Under construction.

### DWARF

Under construction.

### FLIRT

Under construction. Meanwhile, see [siginfo](https://github.com/excitoon/siginfo).

## Contributions

Feel free to contribute, there are some rules however:

- we are aimed at correctness first, performance is second;
- we honor PEP-8, but put PEP-20 above it;
- chaotic changes of APIs are discouraged, the chaos itself is good though;
- we appreciate retro software and technologies but utilize modern ones when appropriate;
- we wouldn't use Black but Lack instead, `pytest` is strictly forbidden no matter what;
- we don't like crappy dependencies and creepy toolsets;
- we are against of “graphomania”, “not invented here” and “premature refactoring” patterns;
- this is a bad choice for college project.
