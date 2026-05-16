# Windows Optimizer Pro 🚀

Windows 10/11 performance optimization software developed in Python with PySide6.

## 📋 Features

- ✅ Automatic visual effects adjustment for better performance
- ✅ Disable hibernation to free up disk space
- ✅ Activate Ultimate Performance power plan
- ✅ Disable active tracking features
- ✅ Clean temporary files (%temp% and .tmp)
- ✅ Prioritize processor for running programs
- ✅ Automatic system restore point creation
- ✅ Modern and intuitive interface
- ✅ Detailed operation log

## 🎨 Interface

- Minimalist and modern design
- Custom colors (#E82A9C, #E84D2A, #E82A2A, #9D1FAE, #E86C2A, #EB5959)
- Real-time visual feedback
- Operation progress bar
- Color-formatted log area

## 🔧 Requirements

- Windows 10 or 11
- Python 3.12 or higher
- Administrator privileges

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/windows-optimizer-pro.git
cd windows-optimizer-pro
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run as administrator:**
```bash
python main.py
```

## 🚀 Usage

1. Launch the application with administrator privileges
2. Click "Start Optimization" to begin the process
3. Monitor progress through the visual feedback bar
4. Check the log area for detailed operation information
5. System will automatically create a restore point before making changes

## 📁 Project Structure

```
windows-optimizer-pro/
├── main.py              # Main application entry point
├── optimizer.py         # Core optimization logic
├── ui.py                # PySide6 interface
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

## 🛡️ Safety

- Creates automatic restore points before any system changes
- All operations are reversible
- Detailed logs for all actions performed
- Requires explicit administrator confirmation

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.