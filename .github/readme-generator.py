from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
MAP_NAME_SPLITTER = "_v"
PREVIEW_IMAGES_DIR = REPO_ROOT / ".github" / "images"
PREVIEW_IMAGES_URL = ".github/images/"

HEADER = (
    "# C&C Red Alert: The Strandvasker Collection (Map Pack)\n"
    "A collection of the absolute best maps created for C&C Red Alert post anno 2020 in Jutland, Denmark.<br>\n\n"
    "### Installation\n"
    "For CnCNet, clone this repo to the `...\\CnCNet\\RedAlert1_Online\\Maps` folder.<br><br>\n\n"
)


def GenerateReadme(outputFile: Path):
    mapFileNames = sorted(f.name for f in REPO_ROOT.glob("*.mpr"))

    mapGroups = defaultdict(list)
    for fileName in mapFileNames:
        if MAP_NAME_SPLITTER in fileName:
            groupName = fileName.split(MAP_NAME_SPLITTER)[0]
            mapGroups[groupName].append(fileName)

    with open(outputFile, "w", encoding="utf-8", newline="\n") as readmeFile:
        readmeFile.write(HEADER)

        for groupName, mapVersions in sorted(mapGroups.items()):
            readmeFile.write(f"## {groupName}\n")

            for mapNameFull in sorted(mapVersions):
                mapNameClean = mapNameFull.replace("_", " ").replace(".mpr", "")
                readmeFile.write(GetDownloadURL(mapNameClean, mapNameFull) + "<br>\n")

                preview = GetMapPreviewImageStr(mapNameClean, mapNameFull)
                if preview:
                    readmeFile.write(preview + "<br>\n")

            readmeFile.write("<br>\n")

    print(f"Successfully written to '{outputFile}'.")


def GetDownloadURL(mapNameClean: str, mapNameFull: str) -> str:
    # Relative link; GitHub resolves it against the current repo and branch.
    return f"### [{mapNameClean}]({quote(mapNameFull)}?raw=true)"


def GetMapPreviewImageStr(mapNameClean: str, mapNameFull: str) -> str:
    imageName = mapNameFull.replace(".mpr", ".png")
    if not (PREVIEW_IMAGES_DIR / imageName).exists():
        return ""
    return f"![{mapNameClean}]({PREVIEW_IMAGES_URL}{quote(imageName)})"


if __name__ == "__main__":
    GenerateReadme(README_PATH)
