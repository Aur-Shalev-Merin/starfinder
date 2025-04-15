# Sky Observer Setup Instructions

## Requirements

- Python 3.6 or higher
- Internet connection (for automatic location detection and ISS data)
- Basic familiarity with command line/terminal

## Setup Instructions

### 1. Install Python (if not already installed)

#### Windows:
1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH" during installation
3. Click "Install Now"
4. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

#### macOS:
1. Install Homebrew (if not already installed):
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```
   brew install python
   ```

#### Linux:
```
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Create a Project Directory

```
mkdir sky_observer
cd sky_observer
```

### 3. Create a Virtual Environment (Optional but Recommended)

#### Windows:
```
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Required Dependencies

```
pip install requests pyephem
```

### 5. Create the Script File

1. Create a new file named `sky_observer.py`
2. Copy the entire script code into this file
3. Save the file

### 6. Run the Script

```
python sky_observer.py
```

## Usage Instructions

1. When prompted, choose whether to detect your location automatically or enter it manually
2. If choosing manual entry, enter your latitude (-90 to 90) and longitude (-180 to 180)
3. The script will display information about:
   - Upcoming ISS passes
   - Visible planets
   - Moon position and phase
   - Sun position

## Troubleshooting

### "ModuleNotFoundError: No module named 'ephem'"
- Ensure you've installed the dependencies correctly:
  ```
  pip install pyephem
  ```
  Not just `ephem`

### Automatic Location Detection Fails
- Your IP address might be masked by a VPN or proxy
- The geolocation service might be temporarily unavailable
- Use the manual input option instead

### ISS Data Not Available
- Check your internet connection
- The API service might be temporarily unavailable
- Try running the script again later

### Permission Errors During Installation
- On Linux/macOS, try adding `sudo` before commands
- On Windows, run Command Prompt as Administrator

## Making the Script Executable (Linux/macOS)

```bash
chmod +x sky_observer.py
```

Then you can run it with:
```bash
./sky_observer.py
```

## Created By
Aur-Shalev-Merin  
Last Updated: 2025-04-15