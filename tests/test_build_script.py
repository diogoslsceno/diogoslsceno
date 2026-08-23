"""Guard against hand-edited SVGs drifting away from scripts/build_svgs.py.

If this test fails, someone edited dark_mode.svg / light_mode.svg by hand
instead of editing scripts/build_svgs.py and re-running it. Run:

    python3 scripts/build_svgs.py

and commit the result.

Note: "Uptime" and every id in the GitHub Stats block are recalculated and
committed back by the Action on every run (see CONTEXT.md), so their *text*
legitimately differs from this script's placeholders in a live repository.
This test only compares the parts of the file the Action never touches:
everything except those specific ids.
"""

import pathlib
import re
import sys
import unittest

from lxml import etree

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_svgs  # noqa: E402

# Ids the Action (today.py) recalculates and commits back on every run.
# Their text is allowed to differ between the repo and a fresh
# build_svgs.py output; everything else must match exactly.
DYNAMIC_IDS = {
    "age_data", "age_data_dots",
    "repo_data", "repo_data_dots", "contrib_data",
    "star_data", "star_data_dots", "repo_stats_gap",
    "commit_data", "commit_data_dots",
    "follower_data", "follower_data_dots", "commit_stats_gap",
    "loc_data", "loc_data_dots", "loc_add", "loc_del", "loc_del_dots",
}


def _blank_dynamic_ids(svg_text):
    root = etree.fromstring(svg_text.encode("utf-8"))
    for dynamic_id in DYNAMIC_IDS:
        for el in root.iter():
            if el.get("id") == dynamic_id:
                el.text = ""
    return etree.tostring(root, encoding="unicode")


def _collapse_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


class GeneratedSvgsMatchBuildScriptTests(unittest.TestCase):
    def _assert_matches(self, theme, filename):
        committed = (REPO_ROOT / filename).read_text(encoding="utf-8")
        generated = build_svgs.make_svg(theme)
        self.assertEqual(
            _collapse_whitespace(_blank_dynamic_ids(committed)),
            _collapse_whitespace(_blank_dynamic_ids(generated)),
        )

    def test_light_mode_matches_build_script_output(self):
        self._assert_matches("light", "light_mode.svg")

    def test_dark_mode_matches_build_script_output(self):
        self._assert_matches("dark", "dark_mode.svg")


if __name__ == "__main__":
    unittest.main()

