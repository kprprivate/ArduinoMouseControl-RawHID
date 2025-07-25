# 🎯 ArduinoMouseControl v1.0

A lightweight, low-latency Arduino HID mouse controller with automatic Python discovery via RawHID communication.

## ✨ Features

- **🔍 Auto-Discovery**: Python automatically finds and connects to Arduino via HID enumeration
- **⚡ Ultra-Low Latency**: Fire-and-forget commands with no response overhead
- **🎮 Complete Control**: Mouse movement, left clicks, and scroll wheel support
- **🔌 Plug & Play**: No complex setup - just upload and run
- **🛡️ Reliable**: Robust HID communication with proper error handling

## 🚀 Quick Start

1. **Hardware**: Arduino Leonardo/Micro/Pro Micro (32u4-based)
2. **Install Library**: HID-Project library in Arduino IDE
3. **Upload**: `arduino_mouse_controller.ino` to your Arduino
4. **Install**: `pip install hidapi` 
5. **Run**: `python mouse_controller.py`

## 📡 API

```python
mouse = ArduinoMouseController()
mouse.move(x, y)        # Relative movement
mouse.click()           # Single left click  
mouse.click_down()      # Press and hold
mouse.click_up()        # Release click
mouse.wheel(delta)      # Scroll wheel
```

Thanks Antrophic + Claude Code Sonnet 4