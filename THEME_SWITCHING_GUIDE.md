# Theme Switching Guide - Fishtest Worker GUI

## Overview
The Fishtest Worker GUI now supports dynamic theme switching between Light and Dark modes. This feature provides a modern, customizable user experience that adapts to user preferences and different lighting conditions.

## 🎨 Available Themes

### Light Theme
- **Background**: Clean white and light gray tones
- **Text**: Dark text for excellent readability
- **Accents**: Professional blue highlights
- **Best for**: Bright environments, daytime use

### Dark Theme  
- **Background**: Dark gray and charcoal tones
- **Text**: Light text for comfortable viewing
- **Accents**: Same professional blue highlights
- **Best for**: Low-light environments, nighttime use, reduced eye strain

## 🔄 How to Switch Themes

### Method 1: Settings Panel
1. Open the Fishtest Worker GUI
2. Click on the **"⚙️ Settings"** tab
3. In the **Theme** section, use the dropdown menu
4. Select either **"Light"** or **"Dark"**
5. The theme will change immediately with visual feedback

### Method 2: Keyboard Shortcut
- Press **`Ctrl+T`** to instantly toggle between themes
- This works from any tab in the application
- Provides quick switching without navigating to settings

### Method 3: Automatic Loading
- Your theme preference is automatically saved
- The GUI will remember your choice and load it on startup
- No need to reconfigure each time you open the application

## 🔧 Technical Implementation

### Theme Persistence
- Theme preference is saved in your configuration file
- Located at: `~/.fishtest_worker_config.json`
- Automatically loaded when the application starts

### Real-time Updates
- All UI components update immediately when theme changes
- No restart required
- Smooth transition between themes

### Visual Feedback
- Toast notification confirms theme change
- Log entry records the theme switch
- Settings dropdown reflects current selection

## 🎯 Features

### Comprehensive Coverage
- **All UI Elements**: Buttons, text fields, labels, frames
- **Log Display**: Syntax highlighting adapts to theme
- **Status Indicators**: Colors remain consistent and readable
- **Tooltips**: Automatically adjust to theme colors

### Smart Color Management
- **High Contrast**: Ensures excellent readability in both themes
- **Consistent Branding**: Accent colors maintain brand identity
- **Accessibility**: Meets contrast ratio standards

### Performance Optimized
- **Instant Switching**: No lag or delay when changing themes
- **Memory Efficient**: Minimal overhead for theme management
- **Smooth Transitions**: Clean visual updates

## 🚀 Usage Tips

### Best Practices
1. **Try Both Themes**: Test both to see which you prefer
2. **Environment Matching**: Use Light for bright rooms, Dark for dim lighting
3. **Eye Comfort**: Dark theme can reduce eye strain during long sessions
4. **Keyboard Shortcut**: Use `Ctrl+T` for quick switching

### Customization
- Theme preference is per-user
- Settings are preserved across application updates
- Easy to reset by deleting the config file

## 🔍 Troubleshooting

### Theme Not Changing
1. **Check Settings Tab**: Ensure you're in the Settings tab
2. **Dropdown Selection**: Make sure to select from the dropdown
3. **Restart Application**: Close and reopen if issues persist

### Visual Issues
1. **Force Refresh**: Press `F5` to refresh the display
2. **Toggle Theme**: Use `Ctrl+T` to toggle back and forth
3. **Check Logs**: Look in the Logs & Stats tab for error messages

### Configuration Issues
1. **Reset Config**: Delete `~/.fishtest_worker_config.json` to reset
2. **Manual Edit**: Edit the config file to set `"theme": "light"` or `"theme": "dark"`
3. **Permissions**: Ensure the config file is writable

## 📋 Keyboard Shortcuts Summary

| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | Toggle theme (Light ↔ Dark) |
| `Ctrl+Q` | Quit application |
| `Ctrl+L` | Focus login field |
| `Ctrl+S` | Start/Stop worker |
| `F5` | Refresh status |

## 🎨 Color Schemes

### Light Theme Colors
```
Primary Background:   #ffffff (White)
Secondary Background: #f8f9fa (Light Gray)
Accent Background:    #e9ecef (Lighter Gray)
Primary Text:         #212529 (Dark Gray)
Secondary Text:       #6c757d (Medium Gray)
Accent Color:         #0d6efd (Blue)
Success Color:        #198754 (Green)
Warning Color:        #fd7e14 (Orange)
Error Color:          #dc3545 (Red)
```

### Dark Theme Colors
```
Primary Background:   #212529 (Dark Gray)
Secondary Background: #343a40 (Medium Dark)
Accent Background:    #495057 (Lighter Dark)
Primary Text:         #f8f9fa (Light Gray)
Secondary Text:       #adb5bd (Medium Light)
Accent Color:         #0d6efd (Blue)
Success Color:        #198754 (Green)
Warning Color:        #fd7e14 (Orange)
Error Color:          #dc3545 (Red)
```

## 🔮 Future Enhancements

### Planned Features
- **Custom Themes**: User-defined color schemes
- **Auto Theme**: Automatic switching based on system time
- **High Contrast**: Enhanced accessibility themes
- **Theme Import/Export**: Share custom themes

### Advanced Options
- **Accent Color Customization**: Choose your preferred accent color
- **Font Size Scaling**: Adjust text size with themes
- **Animation Effects**: Smooth theme transition animations

## 📝 Notes

- Theme switching is instant and requires no restart
- All preferences are automatically saved
- The feature is fully backward compatible
- Works on all supported operating systems (Windows, macOS, Linux)

## 🆘 Support

If you encounter any issues with theme switching:

1. **Check the Logs**: Look in the "📊 Logs & Stats" tab for error messages
2. **Reset Settings**: Delete the config file to restore defaults
3. **Report Issues**: Document any problems with steps to reproduce

The theme switching feature enhances the user experience by providing visual customization options that adapt to different environments and user preferences.
