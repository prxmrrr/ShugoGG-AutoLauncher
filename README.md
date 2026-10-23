# Shugo.GG Auto-Launch

A tiny Windows script that opens the [Shugo.GG](https://shugo.gg) companion app when **Aion 2** starts and closes it when the game closes. Pure Python standard library, nothing to `pip install`.

- Game starts → Shugo opens (within ~5 seconds)
- Game closes → Shugo closes (~10 seconds later)
- Only closes Shugo if the script was the one that opened it, so a Shugo you opened yourself is left alone

> **Disclaimer:** Unofficial, personal-use script. Not affiliated with or endorsed by Shugo.GG, NCSOFT, or Valve. It only checks the Windows process list and starts/stops a separate app; it does not read from or interact with the game. Use at your own risk, and check the terms of your game and companion app if you're unsure about running companion tools.

## Requirements

- Windows 10 or 11
- [Python 3](https://www.python.org/downloads/) (tick "Add python.exe to PATH" when installing)
- The Shugo.GG companion app
- Aion 2 (written for the Steam version, process name `AION2.exe`)

## Quick start

1. Download or clone this repo and put `ShugoGG_Watcher.py` somewhere permanent, e.g. `C:\Users\YOURNAME\Documents\Scripts`.
2. Open an **admin** terminal in that folder and run:
   ```
   python ShugoGG_Watcher.py
   ```
3. Launch Aion 2. Shugo should open. Close the game and Shugo should close shortly after.
4. Press `Ctrl+C` to stop it.
5. To run it automatically at login, follow the Task Scheduler steps in the **[full setup tutorial](docs/SETUP.md)**.

## Settings

Edit the block at the top of `ShugoGG_Watcher.py`:

| Setting | Default | Purpose |
|---|---|---|
| `GAME_EXE` | `"AION2.exe"` | Game process name, as shown in Task Manager > Details |
| `SHUGO_DIR` | `None` | Shugo install folder. `None` auto-detects common locations |
| `SHUGO_EXE` | `None` | Full path to Shugo's `.exe` if auto-detect picks the wrong file |
| `POLL_SECONDS` | `5` | How often to check for the game |
| `CLOSE_DELAY` | `10` | Seconds the game must be gone before Shugo closes |

To use it with another game, change `GAME_EXE`.

## Why Shugo is launched through `explorer.exe`

The script runs with admin rights so it can reliably close Shugo. If it launched Shugo directly, Shugo would inherit admin rights too, and in testing that interfered with a global Discord mute hotkey. Launching through `explorer.exe` starts Shugo at normal permissions while the elevated script can still close it.

## Troubleshooting

See the [troubleshooting section](docs/SETUP.md#troubleshooting) of the setup tutorial. It covers silent Task Scheduler failures, Shugo not closing or going blank, wrong `.exe` detection, and the Discord hotkey issue.

## License

[MIT](LICENSE)
