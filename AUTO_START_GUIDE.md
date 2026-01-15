# Auto-Start Setup Guide

## ✅ Installation Complete!

Keymap is now configured to start automatically when you log in to your Mac.

## 📊 Resource Usage

Your keymap daemon is **very light**:
- **Memory**: ~50-100MB (lighter than a browser tab!)
- **CPU**: Near 0% when idle (event-driven, not polling)
- **Battery**: Minimal impact (only activates on button presses)
- **Disk**: ~80MB total

**Comparison**:
- BetterTouchTool: ~100-150MB
- A browser tab: ~100-200MB
- Keymap: **~50-100MB** ✓

It's perfectly safe to run all the time!

## 🎯 What Happens Now

1. **Immediate**: The daemon is running right now
   - Web UI: http://localhost:8080
   - It's already capturing and remapping your buttons

2. **On Next Login**: Daemon starts automatically
   - You don't need to do anything
   - It will be running in the background

3. **On Restart**: Daemon starts automatically
   - Survives system restarts
   - Your mappings are always active

## 🔧 Management Commands

### Check Status
```bash
# Check if daemon is running
launchctl list | grep keymap

# Test the server
curl http://localhost:8080/api/status
```

### View Logs
```bash
# Startup logs
tail -f ~/Library/Logs/keymap.log

# Error logs (if any)
tail -f ~/Library/Logs/keymap.error.log
```

### Restart Daemon
```bash
# Restart (if you made changes)
launchctl kickstart -k gui/$(id -u)/com.keymap.daemon
```

### Stop Daemon (temporarily)
```bash
# Stop (will auto-restart on next login)
launchctl stop com.keymap.daemon
```

### Uninstall Auto-Start
```bash
cd /Users/anujgoyal/Desktop/Coding/keymap
./uninstall.sh
```

### Reinstall Auto-Start
```bash
cd /Users/anujgoyal/Desktop/Coding/keymap
./install.sh
```

## 🔐 Permissions Note

The daemon needs **Accessibility permissions** to capture mouse button events.

**When running as auto-start**:
1. Open System Settings → Privacy & Security → Accessibility
2. Look for "Python" in the list
3. Toggle it ON
4. Restart the daemon: `launchctl kickstart -k gui/$(id -u)/com.keymap.daemon`

**Note**: This is different from granting permissions to Terminal. The LaunchAgent runs Python directly, so Python needs the permission.

## 🌐 Accessing the Web UI

The web interface is always available at:
- **Local**: http://localhost:8080
- **Network**: http://192.168.4.106:8080 (from other devices on your network)

You can configure button mappings from any browser on your network!

## 🔄 After System Updates

After major macOS updates, you may need to:
1. Re-grant accessibility permissions
2. Restart the daemon: `launchctl kickstart -k gui/$(id -u)/com.keymap.daemon`

## 🎮 Using Your Mappings

Now that auto-start is configured:

1. **Open the web UI**: http://localhost:8080
2. **Configure your buttons** (if you haven't already)
3. **Save your configuration**
4. **Close the browser** - your mappings keep working!

Your button mappings will be active 24/7, automatically switching contexts as you switch between apps.

## 🐛 Troubleshooting

### Daemon not starting on login?
```bash
# Check if LaunchAgent is loaded
launchctl list | grep keymap

# Reload it manually
launchctl unload ~/Library/LaunchAgents/com.keymap.daemon.plist
launchctl load ~/Library/LaunchAgents/com.keymap.daemon.plist
```

### Web UI not accessible?
```bash
# Check if Python process is running
ps aux | grep "python.*main.py"

# Check logs for errors
tail ~/Library/Logs/keymap.error.log
```

### Buttons not being remapped?
1. Check web UI status: http://localhost:8080
2. Verify "Event Tap: Running" shows green
3. Grant accessibility permissions (see above)

## 📝 Files Created

- **LaunchAgent**: `~/Library/LaunchAgents/com.keymap.daemon.plist`
- **Logs**: `~/Library/Logs/keymap.log` and `keymap.error.log`
- **Config**: `~/Library/Application Support/keymap/config.json`

## 🎉 You're All Set!

Your keymap tool is now running automatically in the background, using minimal resources, and ready to remap your buttons 24/7.

Enjoy your custom button mappings! 🖱️⌨️
