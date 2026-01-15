# Quick Start Guide

## Start the Application

1. Open Terminal and navigate to the keymap directory:
   ```bash
   cd keymap
   ```

2. Run the startup script:
   ```bash
   ./run.sh
   ```

3. The terminal will show:
   ```
   Starting Keymap daemon...
   Web UI will be available at http://localhost:8080
   ```

4. Open your browser and go to: **http://localhost:8080**

## First-Time Setup

### 1. Grant Accessibility Permissions

When you first run the app, you'll see a red banner saying "Accessibility Permissions Required".

1. Click the "Open System Preferences" button
2. macOS will open System Settings
3. Go to: **Privacy & Security → Accessibility**
4. Find "Terminal" (or whichever app you're running the script from) in the list
5. Toggle it ON
6. Go back to the browser and refresh - the banner should turn green!

### 2. Detect Your Mouse Buttons

1. In the web UI, find the "Button Detector" section
2. Click **"Start Detecting"**
3. Press a mouse button (e.g., button 4 on the side of your mouse)
4. You'll see a big number showing which button was detected
5. Remember this number! You'll use it to configure mappings

### 3. Configure a Button Mapping

1. In the "Button Mappings" section, click **"Detect Button"**
2. Press the mouse button you want to remap (e.g., button 4)
3. A new mapping will appear with:
   - **Action dropdown**: Choose "Mouse Click", "Keyboard Shortcut", or "Ignore"
   - **For Mouse Click**: Choose Left, Right, or Middle click
   - **For Keyboard Shortcut**:
     - Click the **"Detect"** button next to the input field
     - Press your desired key combination (e.g., press cmd and ] together)
     - The keys will be detected automatically!
     - Or type it manually: `cmd+[`, `ctrl+t`, etc.

4. Click **"Save Configuration"** when done

## Example Configurations

### Browser Navigation
Map button 4 and 5 to browser back/forward:
- **Button 4** → Keyboard Shortcut: `cmd+[`
- **Button 5** → Keyboard Shortcut: `cmd+]`

### Middle Click
Map button 4 to middle click (great for opening links in new tabs):
- **Button 4** → Mouse Click: Middle

### Per-App Context
Configure different mappings for Chrome vs Terminal:

1. Click **"Add New App Context"**
2. Enter `com.google.Chrome` (or click "Use Current App" while Chrome is open)
3. Configure buttons specifically for Chrome
4. Switch back to "Global (All Apps)" to set default mappings

The app will automatically use Chrome-specific mappings when Chrome is active!

## Common Bundle IDs

- **Chrome**: `com.google.Chrome`
- **Safari**: `com.apple.Safari`
- **Firefox**: `org.mozilla.firefox`
- **Terminal**: `com.apple.Terminal`
- **Visual Studio Code**: `com.microsoft.VSCode`
- **Finder**: `com.apple.finder`
- **Slack**: `com.tinyspeck.slackmacgap`

To find any app's bundle ID:
```bash
osascript -e 'id of app "App Name"'
```

## Stopping the Application

Press `Ctrl+C` in the terminal where you ran `./run.sh`

## Troubleshooting

**Problem**: Red banner won't go away after granting permissions
- **Solution**: Quit Terminal completely and restart it, then run `./run.sh` again

**Problem**: Button presses aren't being remapped
- **Solution**: Check the Status section in the web UI - make sure "Event Tap: Running" shows green

**Problem**: "Failed to create event tap"
- **Solution**: You need to grant accessibility permissions (see step 1 above)

## What's Next?

- Try creating per-app contexts for your most-used applications
- Experiment with keyboard shortcuts to boost productivity
- Check out the full README.md for advanced features

Enjoy your custom button mappings! 🖱️⌨️
