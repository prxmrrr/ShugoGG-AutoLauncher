# Full Setup Tutorial

Opens the Shugo.GG companion app when Aion 2 starts and closes it when Aion 2 closes. Windows only.

**Contents**

1. [Install Python](#step-1--install-python)
2. [Put the script somewhere permanent](#step-2--put-the-script-somewhere-permanent)
3. [Check the settings](#step-3--check-the-settings)
4. [Test it by hand](#step-4--test-it-by-hand)
5. [Find your pythonw.exe path](#step-5--find-your-pythonwexe-path)
6. [Start automatically with Task Scheduler](#step-6--start-automatically-with-task-scheduler)
7. [Test the scheduled task](#step-7--test-the-scheduled-task)
8. [Verify everything](#step-8--verify-everything)
9. [Using it for a different game](#using-it-for-a-different-game)
10. [Updating, stopping, or removing it](#updating-stopping-or-removing-it)
11. [Troubleshooting](#troubleshooting)
12. [How it works](#how-it-works)

---

## Step 1 — Install Python

Skip this if Python is already installed. Check in Command Prompt:

```
python --version
```

If you see a version number, you're set. If you get "python is not recognized" (or the Microsoft Store opens):

1. Download Python 3 from <https://www.python.org/downloads/>.
2. Run the installer and **tick "Add python.exe to PATH"** if shown.
3. Finish the install, open a **new** Command Prompt, and run `python --version` again.

## Step 2 — Put the script somewhere permanent

The scheduled task points at the script's exact location, so choose a folder you won't move or delete.

1. Create a folder such as `C:\Users\YOURNAME\Documents\Scripts` (replace `YOURNAME` with your Windows username).
2. Copy `ShugoGG_Watcher.py` into it.
3. Note the full path, e.g. `C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py`. You'll need it in Step 6.

Tip: in Windows 11, right-click a file and choose **Copy as path**.

## Step 3 — Check the settings

Open `ShugoGG_Watcher.py` in Notepad or VS Code and look at the `SETTINGS` block.

- **`GAME_EXE`**: the game's process name. For Aion 2 on Steam it's `"AION2.exe"`. To verify, start the game, press `Ctrl+Shift+Esc`, open the **Details** tab, and look for it.
- **`SHUGO_DIR`**: leave as `None` to auto-detect. It checks:
  - `C:\Program Files\Shugo.GG App`
  - `C:\Program Files (x86)\Shugo.GG App`
  - `%LOCALAPPDATA%\Programs\Shugo.GG App`
  - `%LOCALAPPDATA%\Shugo.GG App`

  If Shugo is elsewhere, set it, e.g. `SHUGO_DIR = r"D:\Apps\Shugo.GG App"`.
- **`SHUGO_EXE`**: only needed if auto-detect picks the wrong `.exe`. Set the full path to Shugo's main executable. To find it, right-click your Shugo shortcut and choose **Open file location**.
- **`POLL_SECONDS`**: how often to check for the game (default 5).
- **`CLOSE_DELAY`**: seconds the game must be gone before Shugo closes (default 10). This prevents flicker if the game crashes and you relaunch it.

Most people don't need to change anything.

## Step 4 — Test it by hand

Always test manually first, since errors are hidden once it runs from Task Scheduler.

1. Right-click Start and choose **Terminal (Admin)** (or **Windows PowerShell (Admin)**).
2. Go to the script's folder:
   ```
   cd "C:\Users\YOURNAME\Documents\Scripts"
   ```
3. Run:
   ```
   python ShugoGG_Watcher.py
   ```
4. You should see a line like `Using Shugo exe: C:\Program Files\Shugo.GG App\...`. Then it will look idle, which is normal.
5. Launch Aion 2. Shugo should open within about 5 seconds.
6. Close Aion 2. About 10 seconds later Shugo should close, and the terminal prints `taskkill exit code: 0`.
7. Press `Ctrl+C` to stop the script.

If something fails, see [Troubleshooting](#troubleshooting) before continuing.

**Why admin?** In testing, the script needed admin rights to reliably close Shugo. It still starts Shugo at normal permissions on purpose; see [How it works](#how-it-works).

## Step 5 — Find your pythonw.exe path

The scheduled task uses `pythonw.exe`, which is `python.exe` without the console window. Run:

```
python -c "import sys; print(sys.executable)"
```

It prints something like:

```
C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\python.exe
```

Replace `python.exe` with `pythonw.exe` to get your path:

```
C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\pythonw.exe
```

Paste the folder into File Explorer's address bar to confirm `pythonw.exe` is there.

## Step 6 — Start automatically with Task Scheduler

1. Press the Windows key, type **Task Scheduler**, and open it.
2. In the right-hand Actions panel, click **Create Task...** (not "Create Basic Task").

**General tab**

- Name: `Shugo Watcher`
- Tick **Run with highest privileges**
- Leave "Run only when user is logged on" selected

**Triggers tab** → **New...**

- Begin the task: **At log on**
- Select **Specific user** and make sure it's your account
- Make sure **Enabled** is ticked, then OK

**Actions tab** → **New...**

- Action: **Start a program**
- Program/script: your `pythonw.exe` path from Step 5
- Add arguments: the script path from Step 2, **in quotes**
  ```
  "C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py"
  ```
- Start in: the script's folder, **no quotes**
  ```
  C:\Users\YOURNAME\Documents\Scripts
  ```

**Conditions tab**

- Untick **Start the task only if the computer is on AC power** (laptops)

**Settings tab**

- Untick **Stop the task if it runs longer than 3 days**

Click OK, and enter your Windows password if asked.

> **Common mistake:** "Add arguments" needs quotes around the path; "Start in" must not have them. A wrong path makes the task fail silently because `pythonw` hides errors.

## Step 7 — Test the scheduled task

1. In Task Scheduler, open **Task Scheduler Library**.
2. Right-click **Shugo Watcher** and choose **Run**.
3. Press `Ctrl+Shift+Esc`, open **Details**, and look for `pythonw.exe`. If it's there, the watcher is running.
4. Launch Aion 2 and confirm Shugo opens. Close the game and confirm Shugo closes after ~10 seconds.

If `pythonw.exe` isn't listed, check the **Last Run Result** column:

| Code | Meaning |
|---|---|
| `0x0` | Started fine |
| `0x41301` | Currently running (normal while the watcher is active) |
| `0x2` | File not found: a path in Step 6 is wrong |
| `0x1` | Python started but the script errored: run it by hand (Step 4) to see the message |

Once it works, restart your PC once to confirm it starts by itself at login.

## Step 8 — Verify everything

- **Shugo should not be elevated.** In Task Manager > Details, right-click a column header > **Select columns** > tick **Elevated**. Shugo's row should say **No**. (`pythonw.exe` will say Yes, which is expected.)
- **Only one `pythonw.exe`** should be running. End any extras.
- Other apps (like Discord hotkeys) should behave normally when Shugo opens.

## Using it for a different game

Change `GAME_EXE` in the script to the other game's process name from Task Manager > Details, e.g. `GAME_EXE = "OtherGame.exe"`. Then end `pythonw.exe` and re-run the task so the change takes effect.

## Updating, stopping, or removing it

- **Edited the script?** The running copy won't pick up changes. End `pythonw.exe` in Task Manager > Details, then right-click the task in Task Scheduler and choose **Run**.
- **Stop it now:** end `pythonw.exe` in Task Manager > Details.
- **Stop it starting at login:** right-click the task > **Disable**.
- **Remove it:** right-click the task > **Delete**, then delete the script.
- **Moved the script or changed/reinstalled Python?** Edit the task (Properties > Actions > Edit) and update the paths from Steps 5 and 6.

## Troubleshooting

**"python is not recognized"**
Python isn't on your PATH. Reinstall it with "Add python.exe to PATH" ticked, then open a new terminal.

**"Could not find the Shugo.GG App"**
Shugo is installed in a non-standard folder. Set `SHUGO_DIR` or `SHUGO_EXE` (Step 3).

**The task does nothing at all**
Check **Last Run Result** (Step 7). Usually a path is wrong or the quotes are missing. Run the script by hand (Step 4) to see real error messages.

**Shugo doesn't open when the game starts**
- `GAME_EXE` must match the process name in Task Manager > Details exactly, including `.exe`.
- Confirm `pythonw.exe` is running.
- Compare the `Using Shugo exe:` line from a manual test with the real Shugo program. If it picked the wrong file, set `SHUGO_EXE`.

**Shugo opens but never closes, or its window goes blank**
- The script lacks permission to close it. Make sure the task has **Run with highest privileges** ticked, and that you ran your manual test from an admin terminal.
- Or the wrong `.exe` was picked. Set `SHUGO_EXE`.
- To clear a stuck blank window now, end the Shugo processes in Task Manager.

**A Discord (or other app) hotkey fires when Shugo opens**
In testing, Shugo running as admin interfered with a Discord global mute hotkey. The script avoids this by launching Shugo through `explorer.exe`. If you still see it:

1. Check Step 8: Shugo should show Elevated = No.
2. If it shows Yes, right-click Shugo's `.exe` > Properties > Compatibility and untick **Run this program as an administrator**. If the box is greyed out, the app requires admin and this workaround can't help.
3. Make sure no old copy of the script is running (more than one `pythonw.exe`). An old copy that launches Shugo directly would start it as admin.

**I opened Shugo myself and it didn't close**
By design: the script only closes Shugo if it opened it.

**Two copies are running**
End the extra `pythonw.exe` in Task Manager > Details, then re-run the task once.

## How it works

- Every `POLL_SECONDS`, the script runs Windows' built-in `tasklist` to check whether the game process exists.
- When the game appears and Shugo isn't already running, it starts Shugo through `explorer.exe`, so Shugo runs without admin rights.
- When the game has been gone for `CLOSE_DELAY` seconds, and the script opened Shugo, it runs the built-in `taskkill` on Shugo, including its child processes.
- It doesn't read game memory, inject anything, send keystrokes, or otherwise interact with the game.
- Standard library only: nothing is downloaded or installed.
- Use at your own risk. It's a personal-use script and may not suit every setup.
