=====================================================================
 SHUGO.GG AUTO-MANAGER  -  FULL SETUP TUTORIAL
 Opens the Shugo.GG companion app when Aion 2 starts and closes it
 when Aion 2 closes. Windows only.
=====================================================================

TABLE OF CONTENTS
  1. What this does
  2. What you need
  3. What is in this folder
  4. Step 1  - Install Python
  5. Step 2  - Put the script somewhere permanent
  6. Step 3  - Check the settings in the script
  7. Step 4  - Test it by hand
  8. Step 5  - Find your pythonw.exe path
  9. Step 6  - Make it start automatically (Task Scheduler)
 10. Step 7  - Test the scheduled task
 11. Step 8  - Verify everything is working
 12. Using it for a different game
 13. Updating, stopping, or removing it
 14. Troubleshooting
 15. How it works / safety notes


Just DM me if something breaks or if you need better clarification/help!

---------------------------------------------------------------------
1. WHAT THIS DOES
---------------------------------------------------------------------
A small Python script runs quietly in the background and checks every 5
seconds whether the game (AION2.exe) is running.

  * Game starts            ->  the script opens the Shugo.GG App
  * Game closes            ->  about 10 seconds later, the script
                               closes the Shugo.GG App

Shugo is only closed if the script was the one that opened it. If you
open Shugo yourself, the script will not kill it when you are not
gaming.


---------------------------------------------------------------------
2. WHAT YOU NEED
---------------------------------------------------------------------
  * Windows 10 or 11
  * Aion 2 (written for the Steam version, process name AION2.exe)
  * The Shugo.GG companion app installed
  * Python 3 (Step 1)
  * Nothing else. No pip installs, no extra libraries.


---------------------------------------------------------------------
3. WHAT IS IN THIS FOLDER
---------------------------------------------------------------------
  ShugoGG_Watcher.py   the script
  README.txt           this tutorial


---------------------------------------------------------------------
STEP 1 - INSTALL PYTHON
---------------------------------------------------------------------
Skip this step if Python is already installed. To check, open the Start
menu, type "cmd", open Command Prompt, and run:

    python --version

If you see a version number (for example "Python 3.12.4"), you are
set. If you get "python is not recognized" or the Microsoft Store
opens, install Python:

  1. Go to https://www.python.org/downloads/ and download the latest
     Python 3 for Windows.
  2. Run the installer.
  3. On the first screen, TICK "Add python.exe to PATH" (if shown).
  4. Click Install, then close the installer when it finishes.
  5. Open a NEW Command Prompt and run  python --version  again.


---------------------------------------------------------------------
STEP 2 - PUT THE SCRIPT SOMEWHERE PERMANENT
---------------------------------------------------------------------
The scheduled task will point at the script's exact location, so pick a
folder you will not move or delete later.

  1. Create a folder, for example:
         C:\Users\YOURNAME\Documents\Scripts
     (Replace YOURNAME with your Windows username.)
  2. Copy ShugoGG_Watcher.py into that folder.

Write down the full path to the script. You will need it in Step 6.
Example:
         C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py

TIP: To copy a file's path in Windows 11, right-click it and choose
"Copy as path".


---------------------------------------------------------------------
STEP 3 - CHECK THE SETTINGS IN THE SCRIPT
---------------------------------------------------------------------
Open ShugoGG_Watcher.py in Notepad or Visual Studio Code (VS Code). Near the top is a
SETTINGS block:

  GAME_EXE       The game's process name. For Aion 2 on Steam this is
                 "AION2.exe". To verify: start the game, press
                 Ctrl+Shift+Esc to open Task Manager, click the
                 "Details" tab, and look for AION2.exe. If yours
                 differs, change this value (keep the quotes).

  SHUGO_DIR      Leave as None to auto-detect. The script checks:
                   C:\Program Files\Shugo.GG App
                   C:\Program Files (x86)\Shugo.GG App
                   %LOCALAPPDATA%\Programs\Shugo.GG App
                   %LOCALAPPDATA%\Shugo.GG App
                 If Shugo is installed somewhere else, set it, e.g.
                   SHUGO_DIR = r"D:\Apps\Shugo.GG App"

  SHUGO_EXE      Optional. Only needed if auto-detect picks the wrong
                 .exe file. Set the full path to Shugo's main .exe, e.g.
                   SHUGO_EXE = r"C:\Program Files\Shugo.GG App\Shugo.GG App.exe"
                 To find it: right-click your Shugo shortcut > "Open
                 file location".

  POLL_SECONDS   How often (seconds) it checks for the game. Default 5.

  CLOSE_DELAY    How long (seconds) the game must be gone before Shugo
                 is closed. Default 10. This prevents flicker if the
                 game crashes and you relaunch it right away.

For most people, no changes are needed. Save the file if you edited it.


---------------------------------------------------------------------
STEP 4 - TEST IT BY HAND
---------------------------------------------------------------------
Always test manually before setting up the scheduled task. That way you
can see error messages, which are hidden later.

  1. Right-click the Start button and choose "Terminal (Admin)" or
     "Windows PowerShell (Admin)". Click Yes on the prompt.
  2. Go to the script's folder:
         cd "C:\Users\YOURNAME\Documents\Scripts"
  3. Run:
         python ShugoGG_Watcher.py
  4. You should see a line like:
         Using Shugo exe: C:\Program Files\Shugo.GG App\Shugo.GG App.exe
     After that the window will look idle. That is normal; it is
     waiting for the game.
  5. Launch Aion 2 from Steam. Within about 5 seconds, Shugo should
     open.
  6. Close Aion 2. About 10 seconds later, Shugo should close, and the
     terminal prints a line starting with "taskkill exit code: 0".
  7. Press Ctrl+C in the terminal to stop the script.

If something fails here, see the Troubleshooting section before moving
on.

Why Admin? In testing, the script needed admin rights to reliably close
Shugo. The script still starts Shugo at NORMAL (non-admin) permissions
on purpose (see "How it works").


---------------------------------------------------------------------
STEP 5 - FIND YOUR pythonw.exe PATH
---------------------------------------------------------------------
The scheduled task must use "pythonw.exe", which is the same as
python.exe but runs with no black console window. You need its full
path.

In Command Prompt, run:

    python -c "import sys; print(sys.executable)"

It prints something like:

    C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\python.exe

Your pythonw.exe is the same path with "python.exe" replaced by
"pythonw.exe":

    C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\pythonw.exe

Copy that down. To confirm the file exists, paste the folder path into
File Explorer's address bar and look for pythonw.exe.


---------------------------------------------------------------------
STEP 6 - MAKE IT START AUTOMATICALLY (TASK SCHEDULER)
---------------------------------------------------------------------
  1. Press the Windows key, type "Task Scheduler", and open it.
  2. In the right-hand "Actions" panel, click "Create Task..."
     (NOT "Create Basic Task").

  --- General tab ---
  3. Name:  Shugo Watcher
  4. TICK "Run with highest privileges".
  5. Leave "Run only when user is logged on" selected.

  --- Triggers tab ---
  6. Click "New...".
  7. Begin the task:  At log on
  8. Select "Specific user" and make sure it is YOUR account.
  9. Make sure "Enabled" is ticked at the bottom, then click OK.

  --- Actions tab ---
 10. Click "New...".
 11. Action: Start a program
 12. Program/script:
         the full path to pythonw.exe from Step 5, e.g.
         C:\Users\YOURNAME\AppData\Local\Python\pythoncore-3.15-64\pythonw.exe
 13. Add arguments (optional):
         the full path to the script from Step 2, INSIDE QUOTES, e.g.
         "C:\Users\YOURNAME\Documents\Scripts\ShugoGG_Watcher.py"
 14. Start in (optional):
         the script's folder, with NO quotes, e.g.
         C:\Users\YOURNAME\Documents\Scripts
 15. Click OK.

  --- Conditions tab ---
 16. UNTICK "Start the task only if the computer is on AC power"
     (laptops: otherwise it will not run on battery).

  --- Settings tab ---
 17. UNTICK "Stop the task if it runs longer than 3 days"
     (otherwise Windows will kill the watcher after 3 days).

 18. Click OK. If asked, enter your Windows account password.

Common mistake: the quotes. "Add arguments" NEEDS quotes around the
path. "Start in" must NOT have quotes. Also double-check your username
and that the folder in the arguments matches where the script really
is. A wrong path makes the task fail silently.


---------------------------------------------------------------------
STEP 7 - TEST THE SCHEDULED TASK
---------------------------------------------------------------------
You do not need to reboot yet.

  1. In Task Scheduler, click "Task Scheduler Library" on the left.
  2. Right-click "Shugo Watcher" and choose "Run".
  3. Press Ctrl+Shift+Esc, go to the "Details" tab, and look for
     "pythonw.exe". If it is there, the watcher is running.
  4. Launch Aion 2. Shugo should open on its own.
  5. Close Aion 2. Shugo should close about 10 seconds later.

If pythonw.exe is not in the list, the task did not start. In Task
Scheduler, look at the "Last Run Result" column for your task:

    0x0       started fine
    0x41301   currently running (normal while the watcher is active)
    0x2       file not found - a path in Step 6 is wrong
    0x1       Python started but the script hit an error - run it by
              hand (Step 4) to see the message

Once it works, restart your PC once to confirm it starts by itself at
login.


---------------------------------------------------------------------
STEP 8 - VERIFY EVERYTHING IS WORKING
---------------------------------------------------------------------
Optional but recommended checks:

  * Shugo should NOT be running as admin. In Task Manager > Details,
    right-click any column header > "Select columns" > tick
    "Elevated" > OK. Shugo's row should show "No". (The pythonw.exe
    row will show "Yes", which is expected.)

  * Only ONE pythonw.exe should be in the Details list. If you see
    two, end the extra one (right-click > End task).

  * Your other apps should behave normally when Shugo opens (see
    "Discord hotkey" in Troubleshooting).


---------------------------------------------------------------------
USING IT FOR A DIFFERENT GAME
---------------------------------------------------------------------
Open the script and change GAME_EXE to the other game's process name
from Task Manager > Details, for example:

    GAME_EXE = "OtherGame.exe"

Then end pythonw.exe in Task Manager and re-run the task so the change
takes effect.


---------------------------------------------------------------------
UPDATING, STOPPING, OR REMOVING IT
---------------------------------------------------------------------
Edited the script?
  The running copy does not pick up changes. Task Manager > Details >
  right-click pythonw.exe > End task, then in Task Scheduler
  right-click the task > Run.

Stop it right now (until next login):
  Task Manager > Details > right-click pythonw.exe > End task.

Stop it from starting at login:
  Task Scheduler > right-click "Shugo Watcher" > Disable.

Remove it completely:
  Task Scheduler > right-click "Shugo Watcher" > Delete, then delete
  the script from your Scripts folder.

Moved the script, or changed/reinstalled Python?
  Edit the task (right-click > Properties > Actions > Edit) and update
  the paths from Steps 5 and 6.


---------------------------------------------------------------------
TROUBLESHOOTING
---------------------------------------------------------------------

"python is not recognized" in the terminal
  Python is not on your PATH. Reinstall it and tick "Add python.exe to
  PATH" (Step 1), then open a NEW terminal.

Script exits with "Could not find the Shugo.GG App"
  Shugo is installed in a non-standard folder. Set SHUGO_DIR or
  SHUGO_EXE in the script (Step 3).

The task does nothing at all
  Check "Last Run Result" (Step 7). Most often a path is wrong, or the
  quotes are missing or misplaced. Run the script by hand (Step 4) to
  see real error messages, since pythonw hides them.

Shugo does not open when the game starts
  * GAME_EXE must match the process name in Task Manager > Details
    exactly (including .exe).
  * Confirm pythonw.exe is running.
  * Compare the "Using Shugo exe:" line (printed in a manual test) with
    the real Shugo program. If it picked the wrong file, set SHUGO_EXE.

Shugo opens but never closes, or its window goes blank
  * The script lacks permission to close it. Make sure the task has
    "Run with highest privileges" ticked (Step 6, item 4), and that you
    ran your manual test from an Admin terminal.
  * Or the wrong .exe was picked. Set SHUGO_EXE.
  * To clear a stuck blank window now: Task Manager > end the Shugo
    processes.

Discord (or another app) hotkey fires when Shugo opens
  In testing, Shugo running as admin interfered with a Discord global
  mute hotkey. The script avoids this by launching Shugo through
  explorer.exe, which starts it at normal permissions. If you still see
  it:
    1. Check Step 8 - Shugo should show Elevated = No.
    2. If it shows Yes, right-click Shugo's .exe > Properties >
       Compatibility, and untick "Run this program as an
       administrator" (if the box is greyed out, the app requires
       admin and this workaround cannot help).
    3. Make sure no OLD copy of the script is still running (more than
       one pythonw.exe in Task Manager). An old copy that launches
       Shugo directly would start it as admin.

Shugo opens on its own, but I opened it myself earlier and it did not
close
  By design. The script only closes Shugo if it opened it.

Two copies are running
  End the extra pythonw.exe in Task Manager > Details, then re-run the
  task once.


---------------------------------------------------------------------
HOW IT WORKS / SAFETY NOTES
---------------------------------------------------------------------
  * Every POLL_SECONDS the script runs Windows' built-in "tasklist" to
    see whether the game process exists.
  * When the game appears and Shugo is not already running, it starts
    Shugo through explorer.exe (so Shugo runs without admin rights).
  * When the game has been gone for CLOSE_DELAY seconds, and the script
    was the one that opened Shugo, it runs Windows' built-in "taskkill"
    on Shugo, including its child processes.
  * The script does not read game memory, inject anything, send
    keystrokes, or otherwise interact with the game. It only looks at
    the process list and starts/stops a separate app.
  * Standard library only: nothing is downloaded or installed.
  * Use at your own risk. It is a personal-use script and may not suit
    every setup. Check your game's and Shugo's own terms if you are
    unsure about running companion tools.

=====================================================================
