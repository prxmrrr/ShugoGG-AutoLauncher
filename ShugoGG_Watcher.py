# This script monitors the AION2 game process and automatically launches or closes the Shugo.GG App based on the game's running state.
# May have to adjust the directory based on your installation. The default is the standard Program Files directory.
# Dev Note: This script is intended for personal use and may not be suitable for all environments. Use at your own risk.
# Shugo.GG App setup: in the General settings tab of the Shugo.GG App, it's recommended to tick "Run as administrator" and "Start minimized" ("Start minimized" and "Start with Windows" only affect launches at Windows startup).
# If "Run as administrator" is on, Shugo runs elevated, so this script must run elevated too in order to close it. Only run it elevated from an admin-only folder (see docs/SETUP.md, Setup 2).

"""
Watches for a game process (default: AION2.exe) and:
  - launches the Shugo.GG App when the game starts (after a short delay)
  - closes the Shugo.GG App when the game closes

Windows only. Uses only Python's standard library (no pip installs).
See README.md for setup instructions.

DISCLAIMER: This is an unofficial, community-made tool. It is not affiliated
with, endorsed by, or supported by Shugo.GG, NCSOFT, or Valve, and the
Shugo.GG team cannot help with it. It only checks the Windows process list and
starts/stops a separate app; it does not read from or interact with the game,
and it does not modify the Shugo.GG App. The Shugo.GG App is itself an
unofficial tool, and its own Privacy screen explains that the game's terms may
not allow tools like it. You are responsible for following the terms of the
game and of every tool you run. Use at your own risk. Provided "as is" under
the MIT license, without warranty of any kind.
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

# Optional: full path to a Shugo shortcut (.lnk). If set, the script opens this
# shortcut (like double-clicking it) instead of running the .exe directly.
# Most people can leave this as None.
SHUGO_SHORTCUT = None

# Seconds to wait after the game process (AION2.exe) is first detected before
# opening Shugo. Default: 60.
#   * Why: it stops Shugo from appearing the moment the game executable is
#     detected, while the game is still starting up. Shugo opens once you have
#     had time to load in.
#   * To change it: edit the number below, save the file, then restart the
#     script (end pythonw.exe in Task Manager and run the task again).
#   * Longer if your game takes longer to load, shorter if it loads quickly,
#     or 0 to open Shugo as soon as the game is detected.
#   * If the script starts while the game is already running, the wait counts
#     from the moment the script started.
LAUNCH_DELAY = 60

POLL_SECONDS = 5     # how often to check whether the game is running
CLOSE_DELAY = 10     # game must be gone this many seconds before Shugo closes

# ---------------------------------------------------------------------------

NO_WINDOW = 0x08000000  # keeps tasklist/taskkill from flashing console windows

# Full paths to Windows' own tools, so a look-alike .exe sitting in some other
# folder can never be run by mistake.
SYSTEM_ROOT = os.environ.get("SystemRoot", r"C:\Windows")
TASKLIST = os.path.join(SYSTEM_ROOT, "System32", "tasklist.exe")
TASKKILL = os.path.join(SYSTEM_ROOT, "System32", "taskkill.exe")
EXPLORER = os.path.join(SYSTEM_ROOT, "explorer.exe")

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
        [TASKLIST, "/FI", f"IMAGENAME eq {exe_name}", "/NH", "/FO", "CSV"],
        capture_output=True, text=True, creationflags=NO_WINDOW,
    ).stdout
    return exe_name.lower() in out.lower()


def launch_app(target):
    # Start Shugo through explorer.exe so it opens with normal (non-admin)
    # permissions, the same as double-clicking it, even if this script is
    # running elevated. If Shugo's own "Run as administrator" setting is on,
    # Shugo elevates itself.
    subprocess.Popen([EXPLORER, target])


def close_app(exe_name):
    # Force-kill; /T also closes child (WebView) processes.
    r = subprocess.run(
        [TASKKILL, "/F", "/IM", exe_name, "/T"],
        capture_output=True, text=True, creationflags=NO_WINDOW,
    )
    print("taskkill exit code:", r.returncode)
    print(r.stdout.strip() or r.stderr.strip())


def main():
    shugo_path = find_shugo_exe()
    launch_target = shugo_path
    if SHUGO_SHORTCUT:
        if not os.path.isfile(SHUGO_SHORTCUT):
            raise SystemExit(f"SHUGO_SHORTCUT not found: {SHUGO_SHORTCUT}")
        print(f"Launching via shortcut: {SHUGO_SHORTCUT}")
        launch_target = SHUGO_SHORTCUT
    shugo_name = os.path.basename(shugo_path)
    print(
        f"Watching for {GAME_EXE}. Shugo will open {LAUNCH_DELAY} seconds "
        "after the game is detected."
    )

    launched_by_us = False    # only close Shugo if this script opened it
    session_handled = False   # Shugo is started at most once per game session
    game_seen_since = None    # when the game process first appeared
    game_gone_since = None

    while True:
        game_up = is_running(GAME_EXE)

        if game_up:
            game_gone_since = None
            if game_seen_since is None:
                game_seen_since = time.time()
            if (
                not session_handled
                and time.time() - game_seen_since >= LAUNCH_DELAY
            ):
                # Start Shugo once per game session. If you close it yourself
                # while the game is still running, it is NOT reopened.
                if not is_running(shugo_name):
                    launch_app(launch_target)
                    launched_by_us = True
                session_handled = True
        else:
            game_seen_since = None
            session_handled = False
            if launched_by_us:
                if game_gone_since is None:
                    game_gone_since = time.time()
                elif time.time() - game_gone_since >= CLOSE_DELAY:
                    close_app(shugo_name)
                    launched_by_us = False
                    game_gone_since = None

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    main()
