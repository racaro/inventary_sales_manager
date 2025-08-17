# Sembra 2023 - Wine Sales Manager

Wine Sales Manager is a specialized desktop application designed for managing wine sales and inventory for Sembra 2023 wines. The application helps track sales, monitor stock levels, and analyze profit margins specifically tailored for wine distribution business.

## Features

- Track wine sales with detailed information (wine type, quantity, price, client type, payment method)
- Monitor remaining wine stock levels
- View sales analytics by client and wine product
- Track business expenses and calculate profit margins
- Visualize sales data with interactive charts
- Specialized for wine distribution channels (Horeca, Distribution, Public sales, etc.)

## Project Structure
```
inventary_sales_manager/
├── main.py                  # Main entry point
├── requirements.txt         # Project dependencies
├── CHANGELOG.md             # changelog version file
├── README.md                # This file
├── Dockerfile               # Docker file
├── docker-compose.yml       # Docker compose
├── .dockerignore            # Docker ignore file
├── .gitattributes           # Git attributes
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── src/
│   ├── gui/                 # GUI components
│   │   ├── __init__.py
│   │   ├── stock_manager.py # Main application window
│   │   └── tabs/            # UI tabs
│   │       ├── __init__.py
│   │       ├── sales_tab.py     # Wine sales data display tab
│   │       ├── new_sale_tab.py  # New wine sale input tab
│   │       └── summary_tab.py   # Wine sales summary and charts tab
│   └── utils/               # Utility modules
│       ├── __init__.py
│       ├── data_handler.py  # Excel data handling
│       └── config_manager.py # Configuration management
└── scripts/                 # Build and deployment scripts
    ├── run_app.bat         # Windows run script
    ├── run_app.sh          # Linux/Mac run script
    ├── build_exe.bat       # Windows executable build script
    └── docker-start.bat    # Docker startup script
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Git (optional, for development)

### Installation

1. Clone or download this repository:
   ```
   git clone https://github.com/racaro/inventary_sales_manager.git
   cd inventary_sales_manager
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Wine Sales Data Management

The application uses an Excel file to store wine sales data:
- By default, it looks for a file called `sales_data.xlsx` in the `data` directory
- If the file doesn't exist, it will automatically create a new one with the wine sales structure
- No need to manually create any template file - the application handles this for you
- All wine sales modifications are automatically backed up in a `backups` folder
  - Each backup file is named with a timestamp (e.g., `sales_data_backup_20240601_153045.xlsx`)
  - This provides data recovery options in case of accidental changes or data corruption

### Running the Wine Sales Manager

### Method 1: Direct Python Execution
1. Open your command prompt or terminal
2. Navigate to the project directory
3. Run the wine sales application:
   ```
   python main.py
   ```

### Method 2: Using Run Scripts
1. For Windows users:
   ```
   cd scripts
   run_app.bat
   ```

   For macOS/Linux users:
   ```
   cd scripts
   chmod +x run_app.sh  # Make the script executable (only needed once)
   ./run_app.sh
   ```

### Method 3: Creating an Executable for Wine Business

#### Prerequisites for Executable Creation
1. Make sure PyInstaller is installed:
   ```
   pip install pyinstaller
   ```

#### Build Commands

**Option 1: Complete Build (Recommended for Distribution)**
```bash
pyinstaller --onefile --windowed --name "Sembra2023-SalesManager" --add-data "data;data" --add-data "backups;backups" --hidden-import=openpyxl --hidden-import=matplotlib --hidden-import=pandas --hidden-import=PySide6 main.py
```

**Option 2: Simple Build (Basic executable)**
```bash
pyinstaller --onefile --windowed --name "Sembra2023-SalesManager" main.py
```

**Option 3: Optimized Build (Smaller file size)**
```bash
pyinstaller --onefile --windowed --name "Sembra2023-SalesManager" --exclude-module tkinter --exclude-module PIL --hidden-import=openpyxl --hidden-import=matplotlib --hidden-import=pandas main.py
```

#### Using the Build Script (Windows)
For convenience, you can use the automated build script:
```batch
scripts\build_exe.bat
```

#### After Building
1. The executable will be created in the `dist/` folder
2. The file will be named `Sembra2023-SalesManager.exe` (Windows)
3. You can distribute this single file to wine business users
4. Users don't need Python installed - just double-click to run

### Method 4: Running with Docker (Build from Source)

Docker provides a professional containerized environment for consistent wine sales management across different systems.

#### Prerequisites
- Docker Desktop installed on your system
- VNC viewer software (RealVNC Viewer, TightVNC, or UltraVNC)

#### Quick Start with Docker
1. For Windows users, run the automated script:
```cmd
scripts\docker-start.bat
```

   For macOS/Linux users:
   ```bash
   chmod +x scripts/docker-start.sh
   ./scripts/docker-start.sh
   ```

#### Manual Docker Commands
```bash
# Build and start the wine sales manager container
docker-compose up -d

# View application logs
docker-compose logs -f sembra-sales-manager

# Stop the container
docker-compose down

# Rebuild the image (if you made changes)
docker-compose build --no-cache
```

### Method 5: Using Pre-built Docker Image (Recommended)

The easiest way to run Sembra 2023 Wine Sales Manager is using our pre-built Docker image from Docker Hub.

#### Quick Start with Pre-built Image

```bash
# Pull the latest version
docker pull racaro/sembra2023-sales-manager:v1.0.0-Sembra2023

# Run the wine sales manager
docker run -d \
  --name sembra-sales \
  -p 5901:5901 \
  -v ./data:/app/data \
  -v ./backups:/app/backups \
  racaro/sembra2023-sales-manager:v1.0.0-Sembra2023

# Connect with VNC viewer to localhost:5901
```

#### Docker Compose with Pre-built Image

Create a `docker-compose-prebuilt.yml` file:

```yaml
version: '3.8'

services:
  sembra-sales:
    image: racaro/sembra2023-sales-manager:v1.0.0-Sembra2023
    container_name: sembra2023-sales-manager
    ports:
      - "5901:5901"  # VNC port
    volumes:
      - ./data:/app/data
      - ./backups:/app/backups
      - ./config:/app/config
    environment:
      - DISPLAY=:1
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "pgrep", "-f", "python3 main.py"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Then run:
```bash
docker-compose -f docker-compose-prebuilt.yml up -d
```

#### Alternative Tags Available

```bash
# Latest version (same as v1.0.0-Sembra2023)
docker pull racaro/sembra2023-sales-manager:latest

# Specific version for wine business
docker pull racaro/sembra2023-sales-manager:v1.0.0-Sembra2023
```

#### Wine Business Benefits of Pre-built Image
- **🚀 Instant Setup**: No build time required
- **📦 Professional Distribution**: Ready for wine business use
- **🔄 Automatic Updates**: Easy to pull new versions
- **🍷 Sembra 2023 Optimized**: Pre-configured for wine sales
- **💾 Smaller Download**: Optimized image size

#### Accessing the Wine Sales Manager GUI
1. Install a VNC viewer:
   - **RealVNC Viewer** (recommended): https://www.realvnc.com/en/connect/download/viewer/
   - **TightVNC Viewer**: https://www.tightvnc.com/download.php

2. Connect to the wine sales application:
   - Open your VNC viewer
   - Connect to `localhost:5901`
   - No password required
   - The Sembra 2023 Wine Sales Manager will appear in the VNC window

## Wine Sales Business Features

### Wine Product Management
The application is specifically designed for wine sales with support for:
- **Sembra 2023**: Main wine product for tracking
- **Otro**: Additional/custom wine products

### Client Type Categories for Wine Business
- **Muestra**: Wine tasting samples and promotional bottles
- **Distribución**: Wholesale distribution to retailers
- **Horeca**: Hotels, Restaurants, and Cafés
- **Amigos/Familia**: Friends and family sales
- **Público**: Direct public sales
- **Otro**: Special client categories

### Wine Sales Analytics
- **Stock Management**: Track remaining wine inventory (default: 1850 bottles)
- **Sales by Client**: Analyze which distribution channels perform best
- **Profit Analysis**: Calculate margins after expenses (production, marketing, distribution)
- **Payment Tracking**: Monitor cash flow with different payment methods

## Testing the Wine Sales Application

When first launched for your wine business:
1. The application creates a new wine sales database
2. Initial stock is set to 1850 bottles (configurable via JSON)
3. Add wine sales through the "Nueva venta" tab

### Adding Your First Wine Sale:
1. Go to the "Nueva venta" tab
2. Fill in the wine sale details:
   - **Fecha de venta**: Sale date
   - **Acción**: Select "Venta"
   - **Producto**: Choose "Sembra 2023" or "Otro"
   - **Cantidad**: Number of bottles sold
   - **Precio unitario**: Price per bottle
   - **Cliente**: Type of client (Horeca, Distribución, Público, etc.)
   - **Método de pago**: Payment method (Bizum, Efectivo, Factura)
   - **Observaciones**: Notes about the sale
3. Click "Añadir Venta" to record the wine sale
4. View all sales in the "Ventas" tab
5. Analyze wine business performance in the "Resumen" tab

### Wine Business Analytics Dashboard
The "Resumen" tab provides:
- **Stock Restante**: Real-time wine inventory levels
- **Ventas por Cliente**: Performance by distribution channel
- **Ventas por Producto**: Which wines sell best
- **Ganancias**: Profit analysis with expense tracking

## Wine Business Configuration

### Stock Management
Initial stock is managed via `data/config.json`:
```json
{
  "initial_stock": {
    "Sembra 2023": 1850,
    "Otro": 0
  }
}
```

## Development Setup

### Code Quality Tools for Wine Sales Application

1. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks:
   ```
   pre-commit install
   ```

3. Run code quality checks:
   ```
   ruff check .
   ```

## License

This wine sales management application is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
Perfect for wine business use. See https://creativecommons.org/licenses/by-nc/4.0/ for details.

## Support for Wine Business

For questions about using this wine sales manager for your Sembra 2023 business:
- Open an issue on the GitHub repository
- Contact: raulcarrasco9797@gmail.com
- Docker Hub: https://hub.docker.com/r/racaro/sembra2023-sales-manager
- Specialized support for wine distribution business needs

## Wine Business Docker Troubleshooting

### Common Issues for Wine Sales Management
- **Port conflicts**: Change port 5901 in docker-compose files if needed
- **VNC connection issues**: Ensure container is running with `docker ps`
- **Wine sales data not saving**: Check permissions on `data` and `backups` folders

### Wine Business Docker Commands
```bash
# Check wine sales manager status
docker ps | grep sembra

# View wine sales application logs
docker logs sembra2023-sales-manager

# Restart wine sales manager
docker restart sembra2023-sales-manager

# Update to latest version
docker pull racaro/sembra2023-sales-manager:latest
docker stop sembra2023-sales-manager
docker rm sembra2023-sales-manager
docker run -d --name sembra2023-sales-manager -p 5901:5901 -v ./data:/app/data racaro/sembra2023-sales-manager:latest
```

## Wine Business Data Backup

Your wine sales data is automatically protected:
- **Local backups**: Created before each significant change
- **Docker persistence**: Data survives container restarts
- **Excel format**: Easy to import/export for accounting software
- **Timestamp tracking**: Full audit trail of wine sales modifications

---

**🍷 Developed specifically for Sembra 2023 wine business management**

*Professional wine sales tracking and inventory management solution*

**📦 Docker Hub**: https://hub.docker.com/r/racaro/sembra2023-sales-manager
