# Full Setup Tutorial

Opens the Shugo.GG companion app a little after Aion 2 starts and closes it when Aion 2 closes. Windows only.

> **Disclaimer:** This is an unofficial, community-made script. It is not affiliated with, endorsed by, or supported by Shugo.GG, NCSOFT, or Valve. Please don't ask the Shugo.GG team for help with it; open an issue on this repo instead. The Shugo.GG App is itself an unofficial tool, and its own Privacy screen explains that the game's terms may not allow tools like it. You are responsible for following the terms of the game and of every tool you run. Use at your own risk.

**Contents**

1. [Which setup do you need](#which-setup-do-you-need)
2. [Setup 1: normal user](#setup-1-normal-user)
3. [Setup 2: elevated, in a protected folder](#setup-2-elevated-in-a-protected-folder)
4. [Settings reference](#settings-reference)
5. [Changing the launch delay](#changing-the-launch-delay)
6. [Using it for a different game](#using-it-for-a-different-game)
7. [Updating, stopping, or removing it](#updating-stopping-or-removing-it)
8. [Troubleshooting](#troubleshooting)
9. [How it works](#how-it-works)

---

## Which setup do you need

Shugo has a setting inside its own app, **Run as administrator**, which lets its overlays hide in the game's menus (Aion 2 itself runs as admin). When it's on, Shugo starts itself elevated through its own Task Scheduler task. Check it first:

1. Open Shugo and go to **Settings > General**. Look at **Run as administrator**.
2. Start Shugo, press `Ctrl+Shift+Esc` to open Task Manager, and open the **Details** tab. Right-click any column header, choose **Select columns**, tick **Elevated**, and click OK. Find the `shugogg-companion.exe` row and read its Elevated column.

> **Use the Details tab, not the Processes tab.** The Processes tab shows both `python.exe` and `pythonw.exe` as just "Python", so it can't tell them apart. Only Details shows the real file names.

| Shugo's admin setting | Setup to use |
|---|---|
| **Off** (Elevated = No) | **[Setup 1: normal user](#setup-1-normal-user).** Simplest and safest. The script and the scheduled task run without admin rights. Shugo's overlays may not be able to hide in the game's menus, so they can cover parts of the game's interface. |
| **On** (Elevated = Yes) | **[Setup 2: elevated, in a protected folder](#setup-2-elevated-in-a-protected-folder).** A normal-rights script can't close an elevated Shugo, so the script has to run elevated too. That's only safe if the script and the Python that runs it live where a normal user can't edit them. Setup 2 builds exactly that. |

> **Never run an elevated task from a folder you can edit as a normal user** (Documents, Desktop, `AppData`, and so on). Any program running as you could change the script or Python, and the change would run as admin at your next login with no prompt. If you use Setup 2, follow its folder layout exactly.

> **Don't want a script at all?** Shugo has its own **Start with Windows** option, which keeps it in the tray with the overlays showing over the game. This script's only advantage is that Shugo isn't running when you aren't playing.

### PowerShell vs Command Prompt

Several steps ask you to type commands. Windows Terminal opens **PowerShell** by default, and its prompt starts with `PS`, like `PS C:\Users\you>`. Command Prompt's prompt has no `PS`. The two behave differently in one important way:

- In **PowerShell**, a command that starts with a path in quotes needs an `&` and a space in front of it, for example `& "C:\Program Files\...\python.exe" --version`. Without it, you get "Unexpected token" errors.
- In **Command Prompt**, you type the same command without the `&`.

Where it matters, this tutorial shows both.

### Task Scheduler's three boxes

Task Scheduler's **Action** window has three separate boxes, and each holds only its own piece:

| Box | What goes in it | Quotes? |
|---|---|---|
| **Program/script** | The path to `pythonw.exe` and nothing else | **Yes**, put quotes around it |
| **Add arguments (optional)** | The path to `ShugoGG_Watcher.py` and nothing else | **Yes**, put quotes around it |
| **Start in (optional)** | The folder that contains the script | **No quotes** |

If you forget the quotes in **Program/script**, Task Scheduler shows a pop-up saying *"It appears as though arguments have been included in the Program text box."* Click **No**, add the quotes, and try again. And if you put quotes in **Start in**, the task fails with error `0x8007010B` ("The directory name is invalid").

---

## Setup 1: normal user

Use this when Shugo's **Run as administrator** setting is **off**.

### Step 1: Make sure Python is installed

Open **Command Prompt** (press the Windows key, type `cmd`, press Enter) and run:

```
python --version
```

You should see something like `Python 3.12.4`. If you get "python is not recognized," or the Microsoft Store opens, install Python:

1. Download Python 3 from <https://www.python.org/downloads/>.
2. Run the installer and **tick "Add python.exe to PATH"** if you see that option.
3. Finish, then open a **new** Command Prompt and run `python --version` again.

### Step 2: Put the script in a permanent folder

The scheduled task points at the script's exact location, so choose a folder you won't move or delete.

1. In File Explorer, open **Documents** and create a new folder named `Scripts`. You'll have `C:\Users\YOURNAME\Documents\Scripts`, where `YOURNAME` is your Windows username.
2. Copy `ShugoGG_Watcher.py` into it.
3. Write down the full path of the script. Tip: right-click the file and choose **Copy as path**. It will be like `C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py`.

### Step 3: Check the settings

Open `ShugoGG_Watcher.py` in Notepad and read the `SETTINGS` block near the top. Most people don't need to change anything, but check these two:

- `GAME_EXE` should match the game's process name. For Aion 2 it's `"AION2.exe"`. To confirm, start the game, open Task Manager > Details, and look for it.
- `LAUNCH_DELAY` is how many seconds Shugo waits before opening after the game is detected. The default is **60**. See [Changing the launch delay](#changing-the-launch-delay).

The [settings reference](#settings-reference) explains the rest.

### Step 4: Test it by hand

Test before you create the scheduled task, because once it runs in the background you can't see errors.

1. Open a **normal** terminal (not an admin one). Press the Windows key, type `cmd`, and press Enter.
2. Go to the script's folder (use your own path):
   ```
   cd "C:\Users\YOURNAME\Documents\Scripts"
   ```
3. Run the script:
   ```
   python ShugoGG_Watcher.py
   ```
4. You should see two lines: `Using Shugo exe: C:\Program Files\Shugo.GG App\...` and `Watching for AION2.exe. Shugo will open 60 seconds after the game is detected.` Then nothing happens, which is normal. Leave the window open.
5. Make sure Shugo is closed, then launch Aion 2.
6. Wait. About **60 seconds** after the game appears, Shugo should open. (Don't want to wait while testing? See the tip in [Changing the launch delay](#changing-the-launch-delay).)
7. Close Aion 2. About 10 seconds later Shugo should close, and the terminal prints `taskkill exit code: 0`.
8. Press `Ctrl+C` in the terminal to stop the script.

If `taskkill` prints `Access is denied`, Shugo is running at a higher level than your terminal, which means its admin setting is on and you need [Setup 2](#setup-2-elevated-in-a-protected-folder).

### Step 5: Find your pythonw.exe path

The scheduled task uses `pythonw.exe`, which is `python.exe` without the black console window. In Command Prompt, run:

```
python -c "import sys; print(sys.executable)"
```

It prints something like:

```
C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\python.exe
```

Change the end from `python.exe` to `pythonw.exe` to get the path you need:

```
C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\pythonw.exe
```

To check it, paste the folder part into File Explorer's address bar and press Enter. You should see `pythonw.exe` in the list.

### Step 6: Create the scheduled task

1. Press the Windows key, type `Task Scheduler`, and open it.
2. In the right-hand **Actions** panel, click **Create Task...** (not "Create Basic Task").

**General tab**
- **Name:** `Shugo Watcher`
- Leave **Run with highest privileges UNTICKED.**
- Leave "Run only when user is logged on" selected.

**Triggers tab:** click **New...**
- **Begin the task:** At log on
- Under Settings, choose **Specific user** and make sure it shows your account.
- Make sure **Enabled** is ticked at the bottom, then click **OK**.

**Actions tab:** click **New...**
- **Action:** Start a program
- **Program/script:** your `pythonw.exe` path **in quotes**
  ```
  "C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\pythonw.exe"
  ```
- **Add arguments (optional):** the script path **in quotes**
  ```
  "C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py"
  ```
- **Start in (optional):** the script's folder, **no quotes**
  ```
  C:\Users\YOURNAME\Documents\Scripts
  ```
- Click **OK**.

**Conditions tab**
- Untick **Start the task only if the computer is on AC power** (it matters on laptops).

**Settings tab**
- Untick **Stop the task if it runs longer than 3 days**.

Click **OK** to save. If Windows asks for your password, enter it.

You should now see **Shugo Watcher** in the **Task Scheduler Library** list.

### Step 7: Test the scheduled task

1. In **Task Scheduler Library**, right-click **Shugo Watcher** and choose **Run**. Press `F5` to refresh.
2. Open Task Manager > **Details** and look for `pythonw.exe`. If it's there, the watcher is running.
3. Launch Aion 2 and confirm Shugo opens after the delay. Close the game and confirm Shugo closes after about 10 seconds.
4. If `pythonw.exe` isn't in the list, widen the task list until you can see the **Last Run Result** column. See the codes below.
5. Once it works, **restart your PC** and check that `pythonw.exe` is running again after you log in.

| Last Run Result | Meaning |
|---|---|
| `0x0` | Started fine |
| `0x41301` | Currently running (normal while the watcher is active) |
| `0x2` | File not found: a path in Step 6 is wrong |
| `0x1` | Python started but the script errored: run it by hand (Step 4) to see the message |
| `0x8007010B` | "Start in" is invalid: remove any quotes or a trailing backslash |

### Step 8: Verify

In Task Manager > Details, with the **Elevated** column showing:
- `pythonw.exe` and Shugo should both say **No**.
- There should be only **one** `pythonw.exe`. If you see two, end the extra one (right-click > End task).
- Add the **Command line** column (right-click a header > Select columns). The `pythonw.exe` row should show `ShugoGG_Watcher.py` in its command line.

---

## Setup 2: elevated, in a protected folder

Use this when Shugo's **Run as administrator** setting is **on**. The script has to run as administrator to close an elevated Shugo, so every file it uses must sit where normal programs can't change them. You'll build a folder under `Program Files` that holds the script and its own copy of Python. You don't use the Python installed in your user folder (`AppData`), because normal programs can edit that.

**Before you start:** Shugo is installed, **Run as administrator** is on, and Task Manager shows Shugo's Elevated column as **Yes**. You'll need about 20 minutes.

### Step 1: Get the files

1. Download `ShugoGG_Watcher.py` from this repo and keep it somewhere easy to find (Downloads is fine).
2. Go to <https://www.python.org/downloads/windows/>. Open the page for the Python 3 version you want (this was tested with 3.15.1) and scroll to the file list. Download **Windows embeddable package (64-bit)**. It's a `.zip` file. Don't download an installer (`.exe`).

### Step 2: Create the protected folder

1. Open File Explorer and go to **This PC > Local Disk (C:) > Program Files**.
2. Right-click an empty space and choose **New > Folder**. Windows shows "You'll need to provide administrator permission to create a folder here." Click **Continue**.
3. Name the folder exactly `ShugoAutoLauncher` and press Enter.
4. Open `ShugoAutoLauncher`, and create another folder inside it named `python` (click **Continue** again if asked).

**Check:** you now have `C:\Program Files\ShugoAutoLauncher\python\`, and it's empty.

### Step 3: Put Python inside it

1. Right-click the embeddable `.zip` you downloaded and choose **Extract All...**.
2. The window shows a destination path. **Delete it and type this instead**, exactly:
   ```
   C:\Program Files\ShugoAutoLauncher\python
   ```
3. Click **Extract**. Click **Continue** if Windows asks for admin permission.

**Check:** open `C:\Program Files\ShugoAutoLauncher\python`. You should see `python.exe` and `pythonw.exe` **directly in this folder**, with many other files. If you see only a single folder, open it, select everything inside, and move it up into `python`.

### Step 4: Put the script next to it

1. Copy `ShugoGG_Watcher.py`.
2. Open `C:\Program Files\ShugoAutoLauncher` and paste it there, next to the `python` folder. Click **Continue** if asked.

**Check:** `C:\Program Files\ShugoAutoLauncher` contains exactly two items: the `python` folder and `ShugoGG_Watcher.py`.

### Step 5: Check that the folder is protected

This is the security step, so don't skip it.

1. Go up one level to `C:\Program Files`. Right-click the `ShugoAutoLauncher` folder and choose **Properties**.
2. Open the **Security** tab.
3. In the top box ("Group or user names"), click **Users**. It may be labeled like `Users (YOURPC\Users)`. Don't click Edit.
4. In the lower box ("Permissions for Users"), look at the **Allow** column.

**Check:** **Read & execute**, **List folder contents**, and **Read** are ticked, and **Modify** and **Write** are **not** ticked. If Modify or Write is ticked, stop. Anyone could change the script, which defeats the purpose of this setup.

### Step 6: Check that Python runs

1. Right-click the **Start** button and choose **Terminal (Admin)**. Click **Yes**.
2. Run this. In **PowerShell** (the prompt starts with `PS`), include the `&`:
   ```
   & "C:\Program Files\ShugoAutoLauncher\python\python.exe" --version
   ```
   In **Command Prompt**, leave off the `&`:
   ```
   "C:\Program Files\ShugoAutoLauncher\python\python.exe" --version
   ```

**Check:** it prints `Python 3.15.1` (or the version you downloaded). If you get "Unexpected token," you left out the `&` in PowerShell. If it can't find the path, go back to Step 3's check.

### Step 7: Test the script by hand

Keep that admin terminal open.

1. Close Shugo completely: right-click its icon in the system tray and choose **Quit**. Then open Task Manager > **Details** and confirm `shugogg-companion.exe` isn't listed.
2. In the admin terminal, run the script. PowerShell:
   ```
   & "C:\Program Files\ShugoAutoLauncher\python\python.exe" "C:\Program Files\ShugoAutoLauncher\ShugoGG_Watcher.py"
   ```
   Command Prompt (no `&`):
   ```
   "C:\Program Files\ShugoAutoLauncher\python\python.exe" "C:\Program Files\ShugoAutoLauncher\ShugoGG_Watcher.py"
   ```
   (Typing only the `.py` path just opens it in your editor and runs nothing.)
3. **Check:** it prints `Using Shugo exe: C:\Program Files\Shugo.GG App\shugogg-companion.exe` and `Watching for AION2.exe. Shugo will open 60 seconds after the game is detected.` Then it does nothing. Leave it running.
4. Launch Aion 2. The timer starts as soon as `AION2.exe` appears in Task Manager. About **60 seconds** later, Shugo should open on its own. (Because the script is in a protected folder, you can't change the delay for a quick test without copying the file out and back. See [Changing the launch delay](#changing-the-launch-delay). Simply waiting is easier for this first test.)
5. Close the game. About 10 seconds later the terminal should print `taskkill exit code: 0` and a line saying the process was terminated, and Shugo should disappear.
6. Press `Ctrl+C` in the terminal to stop the script.

| What you see | What it means |
|---|---|
| A path error before any output | A path in step 2 is wrong. Check the quotes and spelling |
| `Could not find the Shugo.GG App` | Shugo isn't in one of the usual folders. See the settings reference for `SHUGO_DIR` |
| Shugo never opens | Wait the full 60 seconds after `AION2.exe` shows in Task Manager, then read what the terminal printed |
| `Access is denied` when closing | The terminal isn't an admin one. Close it and reopen it as in Step 6 |

### Step 8: Create the scheduled task

1. Press the Windows key, type `Task Scheduler`, and open it.
2. In the right-hand **Actions** panel, click **Create Task...** (not "Create Basic Task").

**General tab**
- **Name:** `Shugo Watcher`
- **Tick Run with highest privileges** (near the bottom).
- Leave "Run only when user is logged on" selected.

**Triggers tab:** click **New...**
- **Begin the task:** At log on
- Under Settings, choose **Specific user** and make sure it shows your account.
- Make sure **Enabled** is ticked at the bottom, then click **OK**.

**Actions tab:** click **New...**
- **Action:** Start a program
- **Program/script:** the Python path **in quotes**
  ```
  "C:\Program Files\ShugoAutoLauncher\python\pythonw.exe"
  ```
- **Add arguments (optional):** the script path **in quotes**
  ```
  "C:\Program Files\ShugoAutoLauncher\ShugoGG_Watcher.py"
  ```
- **Start in (optional):** the folder, **no quotes**
  ```
  C:\Program Files\ShugoAutoLauncher
  ```
- Click **OK**. If a pop-up says *"arguments have been included in the Program text box,"* click **No** and check that Program/script holds only the quoted `pythonw.exe` path.

**Conditions tab**
- Untick **Start the task only if the computer is on AC power** (it matters on laptops).

**Settings tab**
- Untick **Stop the task if it runs longer than 3 days**.

Click **OK** to save. If Windows asks for your password, enter it.

> **Leave Shugo's own task alone.** When Shugo's "Run as administrator" setting is on, Shugo creates its own scheduled task named "Shugo.GG App". Don't delete or edit it. Shugo removes it itself when you turn that setting off.

**Check:** **Shugo Watcher** appears in the **Task Scheduler Library** list.

### Step 9: Test the task

1. Close the admin terminal from Step 7, so the hand-run copy isn't still running.
2. In **Task Scheduler Library**, right-click **Shugo Watcher** and choose **Run**. Press `F5` to refresh.
3. Open Task Manager > **Details**. Look for `pythonw.exe`, then right-click a column header > **Select columns** and tick **Elevated** and **Command line**. The row should say **Elevated: Yes** and show `ShugoGG_Watcher.py` in its command line.
4. Launch Aion 2, wait about a minute, and confirm Shugo opens. Close the game and confirm Shugo closes after about 10 seconds.
5. If `pythonw.exe` isn't in the list, widen the task list and read **Last Run Result**:

| Last Run Result | Meaning |
|---|---|
| `0x0` | Started fine |
| `0x41301` | Currently running (normal while the watcher is active) |
| `0x2` | File not found: a path in Step 8 is wrong |
| `0x1` | Python started but the script errored: run it by hand (Step 7) to see the message |
| `0x8007010B` | "Start in" is invalid: remove any quotes or a trailing backslash |

### Step 10: Restart and verify

1. **Restart your PC.** Log in and wait a minute.
2. In Task Manager > Details, confirm `pythonw.exe` is running without you having done anything, and that there's only one.
3. Do a normal play session. Shugo should open after the delay and close after the game does.

If something misbehaves, see [Troubleshooting](#troubleshooting).

---

## Settings reference

Open `ShugoGG_Watcher.py` in Notepad or VS Code and look at the `SETTINGS` block near the top. After you change anything, [restart the script](#changing-the-launch-delay).

- **`GAME_EXE`** (default `"AION2.exe"`): the game's process name. For Aion 2 on Steam it's `AION2.exe`. To check, start the game, open Task Manager > **Details**, and look for it. The name must match exactly, including `.exe`.
- **`SHUGO_DIR`** (default `None`): leave as `None` to auto-detect. The script looks in `C:\Program Files\Shugo.GG App`, `C:\Program Files (x86)\Shugo.GG App`, `%LOCALAPPDATA%\Programs\Shugo.GG App`, and `%LOCALAPPDATA%\Shugo.GG App`. If Shugo is installed elsewhere, set it, for example `SHUGO_DIR = r"D:\Apps\Shugo.GG App"`.
- **`SHUGO_EXE`** (default `None`): only needed if auto-detect picks the wrong `.exe`. Set the full path to Shugo's main program.
- **`SHUGO_SHORTCUT`** (default `None`): optional. Set it to a Shugo shortcut (`.lnk`) to open that instead of the `.exe`. To get a path, hold **Shift**, right-click the shortcut, choose **Copy as path**, and paste it with the quotes removed: `SHUGO_SHORTCUT = r"C:\...\Shugo.GG App.lnk"`. Most people can leave it alone.
- **`LAUNCH_DELAY`** (default `60`): seconds to wait after the game is detected before Shugo opens. See below.
- **`POLL_SECONDS`** (default `5`): how often, in seconds, to check whether the game is running.
- **`CLOSE_DELAY`** (default `10`): how many seconds the game must be gone before Shugo closes, so a crash and relaunch doesn't make Shugo flicker.

## Changing the launch delay

**The default delay is 60 seconds.** The timer starts when the script first sees `AION2.exe` running, so Shugo opens about a minute after you launch the game, not when you press Play in Steam. The delay keeps Shugo from appearing the moment the game is detected, while the game is still starting up.

**If 60 seconds feels too long**, lower the number, for example `30`, or `0` to open Shugo as soon as the game is detected. **If Shugo opens before you're loaded in**, raise it, for example `90` or `120`. A good way to pick the number: time how long your game takes to get from launch to being in the world, then use about that.

**How to change it in Setup 1:**
1. Open `ShugoGG_Watcher.py` in Notepad.
2. Find the line `LAUNCH_DELAY = 60` and change the number. Save the file.
3. Open Task Manager > **Details**, right-click `pythonw.exe` and choose **End task**.
4. In Task Scheduler, right-click **Shugo Watcher** and choose **Run**.

**How to change it in Setup 2:** the script is in a protected folder, so you can't save changes to it directly.
1. Copy `C:\Program Files\ShugoAutoLauncher\ShugoGG_Watcher.py` to your Documents folder.
2. Edit the copy in Notepad: change the number on the `LAUNCH_DELAY = 60` line and save.
3. Copy the edited file back over the one in `C:\Program Files\ShugoAutoLauncher\`. Click **Continue** on the admin prompt and choose to replace the file.
4. End `pythonw.exe` in Task Manager > Details, then run **Shugo Watcher** again from Task Scheduler.
5. Delete the copy in Documents so you don't mix them up later.

Good to know:
- Changes don't apply until the script restarts.
- If you close the game during the wait, Shugo never opens.
- If the script starts while the game is already running (for example, you end and rerun the task mid-session), the wait counts from when the script started.
- To skip the wait while testing in Setup 1, set `LAUNCH_DELAY = 0`, test, then set it back.

## Using it for a different game

Change `GAME_EXE` to the other game's process name from Task Manager > Details, for example `GAME_EXE = "OtherGame.exe"`. Then restart the script as described above.

## Updating, stopping, or removing it

- **Edited the script?** The running copy won't pick up changes. End `pythonw.exe` in Task Manager > Details, then right-click the task in Task Scheduler and choose **Run**.
- **Stop it now:** end `pythonw.exe` in Task Manager > Details. It starts again at your next login.
- **Stop it starting at login:** right-click the task in Task Scheduler and choose **Disable**.
- **Remove it completely:** right-click the task and choose **Delete**, then delete the script. In Setup 2, also delete the `C:\Program Files\ShugoAutoLauncher` folder.
- **Moved the script or changed Python?** Edit the task (right-click > **Properties** > **Actions** > **Edit**) and update the paths.

## Troubleshooting

**"python is not recognized"**
Python isn't on your PATH. Reinstall it with "Add python.exe to PATH" ticked, then open a **new** terminal.

**"Unexpected token" when running a quoted path in PowerShell**
PowerShell needs `&` in front of a quoted path. Use `& "C:\...\python.exe" ...`, or use Command Prompt instead (see [PowerShell vs Command Prompt](#powershell-vs-command-prompt)).

**Typing the script's path just opens an editor**
That runs nothing. Put the Python path first and the script path after it, as in the test steps.

**Task Scheduler says "arguments have been included in the Program text box"**
Click **No**. Program/script must hold only the path to `pythonw.exe`, in quotes. The script's path goes in the separate **Add arguments** box.

**The task fails with error `0x8007010B`**
"Start in" is invalid. It must have no quotes and no trailing backslash.

**The task does nothing at all**
Check the **Last Run Result** column in Task Scheduler (the codes are in the setup steps). Usually a path is wrong or the quotes are misplaced. Run the script by hand to see real error messages, since the scheduled version hides them.

**I only see "Python" in Task Manager, not `pythonw.exe`**
You're on the Processes tab. Open the **Details** tab, which shows real file names.

**"Could not find the Shugo.GG App"**
Shugo is installed somewhere non-standard. Set `SHUGO_DIR` or `SHUGO_EXE`.

**"SHUGO_SHORTCUT not found"**
The path you set doesn't exist. Copy it again with **Copy as path**, or set it back to `None`.

**Shugo doesn't open when the game starts**
- Remember the launch delay: by default Shugo opens 60 seconds after the game is detected.
- `GAME_EXE` must match the process name in Task Manager > Details exactly, including `.exe`.
- Confirm `pythonw.exe` is running.
- Run the script by hand and read what it prints.

**Shugo opens but never closes, or its window goes blank**
- Run the script by hand and read the `taskkill` output.
  - `Access is denied`: Shugo is running at a higher level than the script. If Shugo's admin setting is on, use Setup 2, or turn that setting off and use Setup 1.
  - `process not found`: the wrong `.exe` was picked. Set `SHUGO_EXE`.
- To clear a stuck blank window now, end the Shugo processes in Task Manager.

**A Discord (or other app) hotkey toggles when Shugo starts**
This isn't caused by this script. On the author's PC, Discord's mute keybind was a single modifier key (Right Alt on its own), and it toggled every time an elevated Shugo started, even with this script completely removed and Shugo started by hand. Binding mute to a combination (Right Alt + Right Ctrl) stopped it. The exact cause wasn't found. Turning off Discord's hardware acceleration, and changing Shugo's own shortcuts and options, did not help.
- If you have a keybind that is a single modifier key (Alt, Ctrl, or Shift on its own), try a combination of keys or a non-modifier key instead.
- If your keybinds overlap (for example one on Right Ctrl and another on Right Alt + Right Ctrl), check that pressing the combination doesn't also fire the shorter one.
- If you think Shugo itself is misbehaving, report it to the Shugo.GG team, since it's reproducible without any script.

**I opened Shugo myself and it didn't close**
By design: the script only closes Shugo if it opened it.

**I closed Shugo and it didn't come back**
By design: the script opens Shugo once per game session. It opens again the next time the game starts.

**Two copies are running**
End the extra `pythonw.exe` in Task Manager > Details, then run the task once.

## How it works

- Every `POLL_SECONDS`, the script runs Windows' built-in `tasklist` to check whether the game process exists.
- Once the game has been running for `LAUNCH_DELAY` seconds, and Shugo isn't already running, the script starts Shugo through `explorer.exe`, which starts it at normal permissions like a double-click. If Shugo's own admin setting is on, Shugo elevates itself.
- When the game has been gone for `CLOSE_DELAY` seconds, and the script opened Shugo, it runs the built-in `taskkill` on Shugo, including its child processes.
- It calls Windows' tools by full path (under `%SystemRoot%`) so a look-alike `.exe` in another folder can't be run by mistake.
- It doesn't read game memory, inject anything, send keystrokes, or otherwise interact with the game, and it doesn't modify Shugo.
- Standard library only: nothing is downloaded or installed.
- Use at your own risk. It's a personal-use script and may not suit every setup.
