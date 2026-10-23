# This script monitors the AION2 game process and automatically launches or closes the Shugo.GG App based on the game's running state.
# May have to adjust the directory based on your installation. The default is the standard Program Files directory.
# Dev Note: This script is intended for personal use and may not be suitable for all environments. Use at your own risk.

"""
Watches for a game process (default: AION2.exe) and:
  - launches the Shugo.GG App when the game starts
  - closes the Shugo.GG App when the game closes

Windows only. Uses only Python's standard library (no pip installs).
See README.md for setup instructions.

Use at your own risk. This script only checks the Windows process list and
starts/stops a separate app. It does not read from or interact with the game.
"""

import glob
import os
import subprocess
import time

# ----------------------------- SETTINGS ------------------------------------

# Process name of the game, exactly as shown in Task Manager > Details.
GAME_EXE = "AION2.exe"

# Folder where the Shugo.GG App is installed. Leave as None to auto-detect
# from the common install locations listed below.
SHUGO_DIR = None

# Optional: set this to the full path of Shugo's .exe if auto-detect picks
# the wrong file. Example: r"C:\Program Files\Shugo.GG App\Shugo.GG App.exe"
SHUGO_EXE = None

POLL_SECONDS = 5     # how often to check whether the game is running
CLOSE_DELAY = 10     # game must be gone this many seconds before Shugo closes

# ---------------------------------------------------------------------------

NO_WINDOW = 0x08000000  # keeps tasklist/taskkill from flashing console windows

COMMON_DIRS = [
    r"C:\Program Files\Shugo.GG App",
    r"C:\Program Files (x86)\Shugo.GG App",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Shugo.GG App"),
    os.path.expandvars(r"%LOCALAPPDATA%\Shugo.GG App"),
]


def find_shugo_exe():
    """Return the full path to Shugo's .exe, or exit with a clear message."""
    if SHUGO_EXE:
        if not os.path.isfile(SHUGO_EXE):
            raise SystemExit(f"SHUGO_EXE not found: {SHUGO_EXE}")
        print(f"Using Shugo exe: {SHUGO_EXE}")
        return SHUGO_EXE

    search_dirs = [SHUGO_DIR] if SHUGO_DIR else COMMON_DIRS
    for folder in search_dirs:
        exes = [
            f for f in glob.glob(os.path.join(folder, "*.exe"))
            if "uninstall" not in os.path.basename(f).lower()
            and not os.path.basename(f).lower().startswith("unins")
        ]
        if exes:
            # Prefer a file with "shugo" in its name
            exes.sort(key=lambda f: "shugo" not in os.path.basename(f).lower())
            print(f"Using Shugo exe: {exes[0]}")
            return exes[0]

    raise SystemExit(
        "Could not find the Shugo.GG App. Set SHUGO_DIR or SHUGO_EXE "
        "at the top of this script."
    )


def is_running(exe_name):
    out = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {exe_name}", "/NH", "/FO", "CSV"],
        capture_output=True, text=True, creationflags=NO_WINDOW,
    ).stdout
    return exe_name.lower() in out.lower()


def launch_app(path):
    # Launching through explorer.exe starts the app at normal (non-admin)
    # permissions, even though this script may be running elevated.
    # (Shugo launched as admin was found to interfere with some global
    # hotkeys, e.g. Discord push-to-mute.)
    subprocess.Popen(["explorer.exe", path])


def close_app(exe_name):
    # Force-kill; /T also closes child (WebView) processes.
    r = subprocess.run(
        ["taskkill", "/F", "/IM", exe_name, "/T"],
        capture_output=True, text=True, creationflags=NO_WINDOW,
    )
    print("taskkill exit code:", r.returncode)
    print(r.stdout.strip() or r.stderr.strip())


def main():
    shugo_path = find_shugo_exe()
    shugo_name = os.path.basename(shugo_path)
    launched_by_us = False   # only close Shugo if this script opened it
    game_gone_since = None

    while True:
        game_up = is_running(GAME_EXE)

        if game_up:
            game_gone_since = None
            if not launched_by_us and not is_running(shugo_name):
                launch_app(shugo_path)
                launched_by_us = True
        elif launched_by_us:
            if game_gone_since is None:
                game_gone_since = time.time()
            elif time.time() - game_gone_since >= CLOSE_DELAY:
                close_app(shugo_name)
                launched_by_us = False
                game_gone_since = None

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
