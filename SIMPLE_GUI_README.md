# Simple Fishtest Worker GUI

A streamlined GUI for the fishtest worker with the essential features you requested:

## Features

✅ **Login to Fishtest** - Enter username and password  
✅ **Choose CPU Cores** - Select how many cores to use  
✅ **Remember Password** - Automatically saves and loads your credentials  
✅ **Background Process** - Runs continuously until you click stop  

## Files

- `fishtest_gui.py` - Main GUI application
- `config_manager.py` - Handles saving/loading settings and password memory
- `worker_controller.py` - Controls the fishtest worker process
- `gui_components.py` - UI components (login, status, controls)
- `run_fishtest_gui.py` - Simple launcher script

## How to Use

### 1. Start the GUI
```bash
python3 fishtest_gui.py
```
or
```bash
python3 run_fishtest_gui.py
```

### 2. Login Setup
- Enter your fishtest username and password
- Choose how many CPU cores to use (1 to max available)
- Click "Login to Fishtest" button (located right under the password field)

### 3. Start Working
- After successful login, click "Start Worker" to begin
- The worker runs in the background continuously
- Monitor progress in the status log
- Click "Stop Worker" when you want to stop

## Key Features

### Password Memory
- Your password is automatically saved (encoded for basic security)
- Settings are stored in `~/.fishtest_worker_config.json`
- Next time you open the GUI, your credentials are pre-filled

### Background Operation
- Once started, the worker runs continuously in the background
- You can minimize the GUI window and it keeps working
- The worker only stops when you click "Stop Worker" or close the GUI

### Simple Interface
- Clean, focused interface with only essential controls
- Real-time status updates and logging
- Color-coded status indicator (red=stopped, green=running)
- Clear login flow with dedicated login button

### Core Selection
- Easy spinbox to select CPU cores (1 to maximum available)
- Shows available core count for reference
- Automatically limits to valid range

## Status Indicators

- **Red dot**: Worker stopped
- **Green dot**: Worker running
- **Login button**: Located under password field, shows "Login to Fishtest" or "✓ Logged In"
- **Start Worker button**: Located in Controls section, disabled until logged in
- **Status text**: Current operation (Ready, Logging in, Starting worker, etc.)
- **Log area**: Real-time messages from the worker

## Requirements

- Python 3.6+
- tkinter (included with Python)
- fishtest worker files in `worker/` directory

## Troubleshooting

### "Worker script not found"
Make sure the `worker/` directory exists with `worker.py` inside it.

### "Import error"
Ensure you're running from the fishtest root directory with the worker subdirectory.

### Login fails
- Check username and password are correct
- Verify internet connection
- Make sure you have a valid fishtest account

### Worker won't start
- Make sure you're logged in first (click "Login to Fishtest")
- Test login credentials first
- Check that no other worker is already running
- Look at the log messages for specific errors

This simplified GUI focuses on your core requirements while keeping the interface clean and easy to use.
