#!/usr/bin/env python3
"""Convert a Figma variables JSON export of _lib-mule-ui into tokens.css.

Usage: python3 build-tokens.py <export.json>

Reads the "theme.stickermule" collection (light values, resolved hex) and
"screen.desktop", strips legacy and off-brand groups, and writes a Tailwind v4
@theme block to tokens.css next to this script.
"""
import json
import re
import sys
from pathlib import Path

DROP_PREFIXES = (
    "product", "pangram", "ffActive", "fwActive", "radiusButton",
    "uiAccent", "brandSm", "legacyBrand", "primaryAlt", "colorless",
    "physicalProducts", "utilityDevices", "utilityBrands3rd",
    "utilityDeprecated", "utilityGraphics", "utilityInvisible",
    "utilityBrand",
)
DROP_SUBSTRINGS = ("Skeuomorphic",)


def kebab(name: str) -> str:
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    s = re.sub(r"(?<=[A-Za-z])(?=\d)", "-", s)
    return s.lower()


def main() -> None:
    raw = Path(sys.argv[1]).read_text()
    data = json.loads(raw)
    if isinstance(data, str):  # some exports double-encode
        data = json.loads(data)

    theme = data["theme"]["stickermule"]
    desktop = data["screen"]["desktop"]

    colors = []
    for name, value in theme.items():
        if any(name.startswith(p) for p in DROP_PREFIXES):
            continue
        if any(s in name for s in DROP_SUBSTRINGS):
            continue
        if not (isinstance(value, str) and value.startswith("#")):
            continue
        colors.append(f"  --color-{kebab(name)}: {value};")

    radii = []
    for name, value in desktop.items():
        if name.startswith("radius") and name not in ("radiusNone", "radius1px"):
            unit = "px" if name != "radiusRound" else "px"
            radii.append(f"  --radius-{kebab(name[6:])}: {round(value)}{unit};")

    controls = []
    for name in ("heightControlXs", "heightControlSm", "heightControlMd",
                 "heightControlLg", "heightNav"):
        controls.append(f"  --spacing-{kebab(name[6:])}: {round(desktop[name])}px;")

    text = [
        "  --text-xxs: 10px;",
        "  --text-xs: 12px;",
        "  --text-sm: 14px;",
        "  --text-base: 16px;",
        "  --text-lg: 20px;",
        "  --text-xl: 24px;",
        "  --text-2xl: 32px;",
    ]

    fonts = [
        '  --font-heading: "Proxima Nova", "Helvetica Neue", Arial, sans-serif;',
        '  --font-body: "Helvetica Neue", Helvetica, Arial, sans-serif;',
        "  --font-code: Courier, monospace;",
    ]

    shadows = [
        "  --shadow-card: 0 1px 3px 0 #6b6b6b26;",
        "  --shadow-overlay: 0 4px 16px 0 #6b6b6b33;",
    ]

    out = Path(__file__).parent / "tokens.css"
    block = "\n".join(
        ["@theme {", "  /* _lib-mule-ui — stickermule theme, light mode */"]
        + fonts + text + radii + controls + shadows
        + ["", "  /* colors */"] + colors + ["}"]
    )
    out.write_text(block + "\n")
    print(f"wrote {out} ({len(colors)} colors)")


if __name__ == "__main__":
    main()
