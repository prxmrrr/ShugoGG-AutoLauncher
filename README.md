# Shugo.GG Auto-Launch

A tiny Windows script that opens the [Shugo.GG](https://shugo.gg/app) companion app a little after **Aion 2** starts and closes it when the game closes. Pure Python standard library, nothing to `pip install`.

- Game starts → Shugo opens after a delay you control (**60 seconds by default**, so it doesn't pop up while the game is still starting)
- Game closes → Shugo closes (~10 seconds later)
- Only closes Shugo if the script was the one that opened it, so a Shugo you opened yourself is left alone
- If you close Shugo yourself during a game session, the script doesn't reopen it

> ## Disclaimer
> This is an **unofficial, community-made, personal-use** script. It is **not affiliated with, endorsed by, or supported by Shugo.GG**, NCSOFT, or Valve, and the Shugo.GG team can't help with it (please open an issue here instead).
>
> The script only checks the Windows process list and starts/stops a separate app. It does not read from or interact with the game, and it does not modify the Shugo.GG App.
>
> The Shugo.GG App is itself an unofficial tool. Its own Privacy screen explains that the game's terms may not allow tools like it. **You are responsible for following the terms of the game and of every tool you run.** Use this script at your own risk. It is provided "as is", without warranty of any kind (see the [license](LICENSE)).

## Requirements

- Windows 10 or 11
- Python 3 (a normal install, or the no-installer "embeddable package"; the tutorial explains which one you need)
- The Shugo.GG companion app
- Aion 2 (currently set up and tested for the Steam version, process name `AION2.exe`; Purple launcher support is planned)

## Start here

**Read the [full setup tutorial](docs/SETUP.md).** It walks through every click, including Task Scheduler, and starts with a short section on which of two setups you need. The choice depends on one setting inside Shugo: **Run as administrator**.

## Quick try (no scheduled task)

1. Put `ShugoGG_Watcher.py` somewhere permanent and open a terminal in that folder. If Shugo's **Run as administrator** setting is on, use an **admin** terminal (right-click Start > **Terminal (Admin)**), otherwise a normal one.
2. Run:
   ```
   python ShugoGG_Watcher.py
   ```
3. Launch Aion 2. About a minute later (the default `LAUNCH_DELAY`), Shugo should open. Close the game and Shugo should close about 10 seconds later.
4. Press `Ctrl+C` to stop it.

To make it start by itself at login, follow the tutorial.

## Settings

Edit the block at the top of `ShugoGG_Watcher.py`:

| Setting | Default | Purpose |
|---|---|---|
| `GAME_EXE` | `"AION2.exe"` | Game process name, as shown in Task Manager > Details |
| `SHUGO_DIR` | `None` | Shugo install folder. `None` auto-detects common locations |
| `SHUGO_EXE` | `None` | Full path to Shugo's `.exe` if auto-detect picks the wrong file |
| `SHUGO_SHORTCUT` | `None` | Optional shortcut (`.lnk`) to open instead of the `.exe` |
| `LAUNCH_DELAY` | `60` | Seconds to wait after the game is detected before opening Shugo. Raise it if Shugo opens too early, lower it (or set `0`) if you want it sooner |
| `POLL_SECONDS` | `5` | How often to check for the game |
| `CLOSE_DELAY` | `10` | Seconds the game must be gone before Shugo closes |

To use it with another game, change `GAME_EXE`. After changing any setting, restart the script. The tutorial has a short section on [changing the launch delay](docs/SETUP.md#changing-the-launch-delay).

## Security: read this before using Task Scheduler

Shugo can run itself as administrator (a setting inside its app, so its overlays can hide in the game's menus). If it does, a normal-rights script can't close it, and the script has to run elevated too. **Don't run an elevated task from a folder you can edit as a normal user.** Any program running as you could modify the script or the Python it uses, and it would run as admin at your next login with no prompt.

The tutorial covers both safe layouts: a plain non-admin setup if Shugo's admin setting is off, and an admin-only folder layout (the script plus its own Python under `Program Files`) if it's on. (Thanks to the Shugo.GG dev team for flagging the risk.)

## Alternative: Shugo's own "Start with Windows"

Shugo has a built-in option to start with Windows and stay in the system tray, with the overlays showing over the game. If you don't mind Shugo running whenever you're logged in, that may be all you need, with no script at all. This script's only advantage is that Shugo isn't running when you aren't playing.

## Troubleshooting

See the [troubleshooting section](docs/SETUP.md#troubleshooting) of the tutorial. It also covers a Discord hotkey that can toggle when Shugo starts. That isn't caused by this script, and the fix is in Discord's keybind settings.

## License

[MIT](LICENSE)
