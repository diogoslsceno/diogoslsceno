#!/usr/bin/env python3
"""Regenerate ``dark_mode.svg`` and ``light_mode.svg`` from the data below.

Read ``CONTEXT.md`` (repository root) before touching this file.

Design goal: every past bug in this project's SVGs (dot-leader padding not
reaching the target width, the header separator line stopping short after the
username changed, the ASCII art overlapping the text column) happened because
someone hand-edited the raw SVG text. This script removes that failure mode:

* Row ids/labels come from ``today.SIMPLE_ROW_SPECS`` (imported, not
  duplicated) so the ids this script writes can never drift from the ids
  ``today.py`` looks for at Action runtime.
* Dot-leader padding is computed by the exact same width-60 algorithm
  ``today.py`` itself uses (``build_dot_leader`` / target width 60), so a
  freshly generated file is already exactly what ``today.align_simple_rows``
  would produce anyway.
* The header/section separator lines are generated to a fixed total visible
  width (``SEPARATOR_TARGET_WIDTH``), not a hardcoded dash count, so renaming
  the header user (``HEADER_USER``) can't leave a short separator again.
* The ASCII art horizontal offset (``ART_X``) is a named constant with the
  measurement that produced it recorded in a comment, not a magic number.

Only edit the data section below, then run:

    python3 scripts/build_svgs.py

from the repository root. It overwrites ``dark_mode.svg`` and
``light_mode.svg``. Run the test suite afterwards
(``python -m unittest discover -s tests -v``) before committing.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import today  # noqa: E402  (path must be extended first)

# --------------------------------------------------------------------------
# DATA -- edit this section only.
# --------------------------------------------------------------------------

# The "user@host" line at the very top of the card.
HEADER_USER = "diogo@diogoslsceno"

# Static values for every row in today.SIMPLE_ROW_SPECS *except* "age_data",
# keyed by the row's value id (the second item of each SIMPLE_ROW_SPECS
# tuple). "age_data" is intentionally excluded: today.py recalculates it
# automatically from BIRTHDAY on every Action run (see CONTEXT.md).
VALUES = {
    "os_value": "Linux (Ubuntu 26.04.1 LTS)",
    "host_value": "None, Inc.",
    "kernel_value": "Student (Diogo Sales UFPA)",
    "ide_value": "Vim 9.2.0875, VS Code 1.132",
    "languages_programming_value": "C, Java, Python",
    "languages_computer_value": "Linux, Docker, Git, GitHub",
    "languages_real_value": "PT-BR (Native), EN (Intermediate)",
    "hobbies_software_value": "Programming Projects, Learning ML",
    "hobbies_systems_value": "Linux, Windows, System Configuration",
    "hobbies_others_value": "Installing, Testing & Breaking OSes",
    "email_value": "diogoslsceno@gmail.com",
}

# Only used for the very first render, before any Action run has ever
# overwritten "age_data". Keep it roughly correct, but don't stress about
# precision -- the workflow recalculates it from BIRTHDAY the first time it
# runs (push, workflow_dispatch, or the daily cron).
AGE_PLACEHOLDER = "21 years, 9 months, 16 days"

# Explicit y position (px) for every row, keyed by the row's value id from
# today.SIMPLE_ROW_SPECS. Row-to-row spacing in this card is *not* uniform
# (blank spacer rows use the standard 20px step, but the gap before/after a
# section header varies -- 30px before/after "- Contact", 40px from the last
# Contact row to "- GitHub Stats", 20px from that header to its first row).
# That irregularity comes from the original template this project started
# from; it's simplest and least error-prone to keep it as an explicit table
# rather than re-derive it with a generic formula (a generic version of this
# was tried and got the Contact/GitHub Stats gaps wrong -- see git history).
ROW_Y = {
    "os_value": 50,
    "age_data": 70,
    "host_value": 90,
    "kernel_value": 110,
    "ide_value": 130,
    "languages_programming_value": 170,
    "languages_computer_value": 190,
    "languages_real_value": 210,
    "hobbies_software_value": 250,
    "hobbies_systems_value": 270,
    "hobbies_others_value": 290,
    "email_value": 350,
}
BLANK_ROW_Y = {150, 230}  # spacer rows with just a bullet, no key/value
CONTACT_HEADER_Y = 320
STATS_HEADER_Y = 390
STATS_ROW_1_Y = 410
STATS_ROW_2_Y = 430
STATS_ROW_3_Y = 450

# GitHub Stats block: structure is fixed (see CONTEXT.md for why -- today.py
# looks for these exact ids), values are placeholders overwritten by the
# Action on every run.
STATS_PLACEHOLDER_VALUES = {
    "repo_data": "0",
    "contrib_data": "0",
    "star_data": "0",
    "commit_data": "0",
    "follower_data": "0",
    "loc_data": "0",
    "loc_add": "0",
    "loc_del": "0",
}

# ASCII art: 22 rows x 33 columns, in the same "$&Xx+;:. " density ramp the
# original template used (darkest to lightest: '&' '$' 'X' 'x' '+' ';' ':'
# '.' ' '). Produced by area-weighted downsampling + Floyd-Steinberg
# dithering of a neofetch-style ASCII art piece, cropped to its content
# bounding box before downsampling. Rows are left-padded with today's
# ART_X offset (not embedded in the strings) so re-centering only requires
# changing ART_X below, not regenerating this list.
ASCII_ART = [
    "          ..;+++Xx++;.           ",
    "       .;x$&&&$&X$$$$X;.         ",
    "      ;$&&&$$$$$$$$$$X$X.        ",
    "     .$&&&$&$$$$&$$$&$&&+        ",
    "      ;xXxxXxxX$$$$XX$XX&x       ",
    "     ..:.:..::;xXXXXXxXX$$       ",
    "    .........:+xxx+++xxX$$       ",
    "    :.......:;+;+;;;++xXX+       ",
    "    ..;;:....::;++;+;++xX:       ",
    "     :;+;;.....:;;;;;++Xx.       ",
    "   ...;;:;::...;;;;;;:+x.        ",
    "   .:.:.......::..;x:;+.         ",
    "    ++:.......:;::..:::          ",
    "    .;+:.....;;+:::::.:x         ",
    "    ..::..::++++;;::  x$x        ",
    "    X;:;;:;+x++;::...x$$$x       ",
    "   :$$$x++++;;;:.. :X$$&$Xx:     ",
    "   x$$$x ;X:...  :x$$$$$XXXX:    ",
    "  .$$$&$;;x..  ;X$$$$$$$XXXXX.   ",
    "  x$$$&$+   .;X$$$$$$$XXXXXXXX;  ",
    " +X$$&&$$: .x$X$&$$$$XXXXXXXXXX; ",
    "x$$$$&$X: ;X$$X$X$XXXXXXXXXXXXXX.",
]

# Horizontal offset (px) of the ASCII art from the card's left edge.
# Derivation: the art occupies x=[15, 390) (390 is where the info column's
# "x" attribute starts). Rendering ASCII_ART at x=15 and measuring the
# actual ink bounding box (cairosvg, scale 1.5, threshold on pixel diff from
# the card background) gave a rendered content width of ~306px. Centering
# that inside the 375px-wide [15, 390) band means a left margin of
# (375 - 306) / 2 ~= 34.5px, i.e. ART_X = 15 + 34.5 ~= 48 (rounds to a
# left/right margin of ~34px each, confirmed by re-measuring after the
# change). If ASCII_ART's dimensions change, re-measure -- don't guess.
ART_X = 48

# Card geometry. Height must equal the y of the last content row + 20.
CARD_WIDTH = 985
CARD_HEIGHT = 470
ART_ROW_HEIGHT = 20
INFO_X = 390
SEPARATOR_TARGET_WIDTH = 60  # same target width today.py's dot leaders use

THEMES = {
    "light": {
        "key": "#953800", "value": "#0a3069", "add": "#1a7f37",
        "del": "#cf222e", "cc": "#c2cfde", "bg": "#f6f8fa", "text": "#24292f",
    },
    "dark": {
        "key": "#ffa657", "value": "#a5d6ff", "add": "#3fb950",
        "del": "#f85149", "cc": "#616e7f", "bg": "#161b22", "text": "#c9d1d9",
    },
}

# --------------------------------------------------------------------------
# BUILD LOGIC -- shouldn't normally need to change.
# --------------------------------------------------------------------------


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def separator_line(label_html, label_visible_len, y):
    """A '<label> ----...' line padded to SEPARATOR_TARGET_WIDTH total chars."""
    dashes = SEPARATOR_TARGET_WIDTH - label_visible_len - 1  # -1 for the space
    dashes = max(1, dashes)
    return f'<tspan x="{INFO_X}" y="{y}">{label_html}</tspan> ' + ("-" * dashes)


def emit_row(y, dots_id, value_id, prefix, value_raw):
    assert prefix.startswith(". ") and prefix.endswith(":")
    key_part = prefix[2:-1]
    dots = today.build_dot_leader(
        max(1, SEPARATOR_TARGET_WIDTH - len(prefix) - len(value_raw))
    )
    if "." in key_part:
        k1, k2 = key_part.split(".", 1)
        key_html = f'<tspan class="key">{esc(k1)}</tspan>.<tspan class="key">{esc(k2)}</tspan>'
    else:
        key_html = f'<tspan class="key">{esc(key_part)}</tspan>'
    return (
        f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>{key_html}:'
        f'<tspan class="cc" id="{dots_id}">{esc(dots)}</tspan>'
        f'<tspan class="value" id="{value_id}">{esc(value_raw)}</tspan>'
    )


def build_info_block():
    lines = []
    for dots_id, value_id, prefix in today.SIMPLE_ROW_SPECS:
        y = ROW_Y[value_id]
        value_raw = AGE_PLACEHOLDER if value_id == "age_data" else VALUES[value_id]
        lines.append((y, emit_row(y, dots_id, value_id, prefix, value_raw)))

    for y in BLANK_ROW_Y:
        lines.append((y, f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>'))

    lines.append(
        (CONTACT_HEADER_Y, separator_line("- Contact", len("- Contact"), CONTACT_HEADER_Y))
    )
    lines.sort(key=lambda item: item[0])
    ordered_lines = [line for _y, line in lines]

    # GitHub Stats section: structure copied verbatim from the original
    # template (today.py expects exactly these ids/layout -- see
    # CONTEXT.md). Values are placeholders the Action overwrites.
    ordered_lines.append(
        separator_line("- GitHub Stats", len("- GitHub Stats"), STATS_HEADER_Y)
    )
    v = STATS_PLACEHOLDER_VALUES
    ordered_lines.append(
        f'<tspan x="{INFO_X}" y="{STATS_ROW_1_Y}" class="cc">. </tspan>'
        f'<tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan>'
        f'<tspan class="value" id="repo_data">{v["repo_data"]}</tspan> '
        f'{{<tspan class="key">Contributed</tspan>: <tspan class="value" id="contrib_data">{v["contrib_data"]}</tspan>}}'
        f'<tspan class="cc" id="repo_stats_gap"> |  </tspan>'
        f'<tspan class="key">Stars</tspan>:<tspan class="cc" id="star_data_dots"> ............ </tspan>'
        f'<tspan class="value" id="star_data">{v["star_data"]}</tspan>'
    )
    ordered_lines.append(
        f'<tspan x="{INFO_X}" y="{STATS_ROW_2_Y}" class="cc">. </tspan>'
        f'<tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> ................... </tspan>'
        f'<tspan class="value" id="commit_data">{v["commit_data"]}</tspan>'
        f'<tspan class="cc" id="commit_stats_gap"> |  </tspan>'
        f'<tspan class="key">Followers</tspan>:<tspan class="cc" id="follower_data_dots"> ........ </tspan>'
        f'<tspan class="value" id="follower_data">{v["follower_data"]}</tspan>'
    )
    ordered_lines.append(
        f'<tspan x="{INFO_X}" y="{STATS_ROW_3_Y}" class="cc">. </tspan>'
        f'<tspan class="key">GitHub LOC</tspan>:<tspan class="cc" id="loc_data_dots"> ...................... </tspan>'
        f'<tspan class="value" id="loc_data">{v["loc_data"]}</tspan> ( '
        f'<tspan class="addColor">+</tspan><tspan class="addColor" id="loc_add">{v["loc_add"]}</tspan>, '
        f'<tspan id="loc_del_dots"></tspan><tspan class="delColor">-</tspan>'
        f'<tspan class="delColor" id="loc_del">{v["loc_del"]}</tspan> )'
    )
    return ordered_lines, STATS_ROW_3_Y


def make_svg(theme_name):
    t = THEMES[theme_name]

    header_line = separator_line(esc(HEADER_USER), len(HEADER_USER), 30)
    info_lines, last_y = build_info_block()

    parts = []
    parts.append("<?xml version='1.0' encoding='UTF-8'?>")
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'font-family="ConsolasFallback,Consolas,monospace" '
        f'width="{CARD_WIDTH}px" height="{CARD_HEIGHT}px" font-size="16px">'
    )
    parts.append("<style>")
    parts.append("@font-face {")
    parts.append("src: local('Consolas'), local('Consolas Bold');")
    parts.append("font-family: 'ConsolasFallback';")
    parts.append("font-display: swap;")
    parts.append("-webkit-size-adjust: 109%;")
    parts.append("size-adjust: 109%;")
    parts.append("}")
    parts.append(f'.key {{fill: {t["key"]};}}')
    parts.append(f'.value {{fill: {t["value"]};}}')
    parts.append(f'.addColor {{fill: {t["add"]};}}')
    parts.append(f'.delColor {{fill: {t["del"]};}}')
    parts.append(f'.cc {{fill: {t["cc"]};}}')
    parts.append("text, tspan {white-space: pre;}")
    parts.append("</style>")
    parts.append(f'<rect width="{CARD_WIDTH}px" height="{CARD_HEIGHT}px" fill="{t["bg"]}" rx="15"/>')

    parts.append(f'<text x="{ART_X}" y="30" fill="{t["text"]}" class="ascii">')
    for i, row in enumerate(ASCII_ART):
        y = 30 + i * ART_ROW_HEIGHT
        parts.append(f'<tspan x="{ART_X}" y="{y}">{esc(row)}</tspan>')
    parts.append("</text>")

    parts.append(f'<text x="{INFO_X}" y="30" fill="{t["text"]}">')
    parts.append(header_line)
    parts.extend(info_lines)
    parts.append("</text>")
    parts.append("</svg>")

    art_bottom = 30 + (len(ASCII_ART) - 1) * ART_ROW_HEIGHT
    if abs(art_bottom - last_y) > ART_ROW_HEIGHT:
        print(
            f"warning: ASCII art bottom (y={art_bottom}) and info block "
            f"bottom (y={last_y}) differ by more than one row -- "
            "see CONTEXT.md rule 5.",
            file=sys.stderr,
        )

    return "\n".join(parts) + "\n"


def main():
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    for theme in ("light", "dark"):
        out_path = repo_root / f"{theme}_mode.svg"
        out_path.write_text(make_svg(theme), encoding="utf-8")
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
