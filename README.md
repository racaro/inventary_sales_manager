# Stock Manager

Stock Manager is a desktop application for managing sales and inventory. The application helps track sales, monitor stock levels, and analyze profit margins.

## Features

- Track sales with detailed information (product, quantity, price, client type, payment method)
- Monitor remaining stock levels
- View sales analytics by client and product
- Track expenses and calculate profit margins
- Visualize data with interactive charts

## Project Structure
```
inventary_sales_manager/
├── main.py                  # Main entry point
├── requirements.txt         # Project dependencies
├── README.md                # This file
├── Template.xlsx            # Data storage template
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── gui/                     # GUI components
│   ├── __init__.py
│   ├── stock_manager.py     # Main application window
│   └── tabs/                # UI tabs
│       ├── __init__.py
│       ├── sales_tab.py     # Sales data display tab
│       ├── new_sale_tab.py  # New sale input tab
│       └── summary_tab.py   # Data summary and charts tab
└── utils/                   # Utility modules
    ├── __init__.py
    └── data_handler.py      # Excel data handling
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

### Data File Information

The application uses an Excel file to store data:
- By default, it looks for a file called `sales_data.xlsx` in the application directory
- If the file doesn't exist, it will automatically create a new one with the required structure
- No need to manually create any template file - the application handles this for you
- All data modifications are automatically backed up in a `backups` folder (created in the application directory)
  - Each backup file is named with a timestamp (e.g., `sales_data_backup_20240601_153045.xlsx`)
  - This provides data recovery options in case of accidental changes or data corruption

### Running the Application

### Method 1: Direct Python Execution
1. Open your command prompt or terminal
2. Run the application directly with Python:
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

   These scripts automatically handle the Python execution with the correct environment.

### Method 3: Creating an Executable
1. Make sure PyInstaller is installed:
   ```
   pip install pyinstaller
   ```
2. Create the executable:
   ```
   # For Windows
   pyinstaller --onefile --windowed --icon=resources/app_icon.ico main.py

   # For macOS
   pyinstaller --onefile --windowed --icon=resources/app_icon.icns main.py

   # For Linux
   pyinstaller --onefile --windowed main.py
   ```
3. Find the executable in the 'dist' folder
4. Double-click the executable to run the application

### Method 4: Running with Docker

Docker provides a containerized environment that ensures the application runs consistently across different systems.

#### Prerequisites
- Docker Desktop installed on your system
- VNC viewer software (RealVNC Viewer, TightVNC, or UltraVNC)

#### Quick Start with Docker
1. For Windows users, run the automated script:
   ```cmd
   docker-start.bat
   ```

   For macOS/Linux users:
   ```bash
   chmod +x docker-start.sh
   ./docker-start.sh
   ```

#### Manual Docker Commands
```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f stock-manager

# Stop the container
docker-compose down

# Rebuild the image (if you made changes)
docker-compose build --no-cache
```

#### Accessing the GUI with Docker
1. Install a VNC viewer:
   - **RealVNC Viewer** (recommended): https://www.realvnc.com/en/connect/download/viewer/
   - **TightVNC Viewer**: https://www.tightvnc.com/download.php
   - **UltraVNC**: https://uvnc.com/downloads/

2. Connect to the application:
   - Open your VNC viewer
   - Connect to `localhost:5901`
   - No password required
   - The Stock Manager application will appear in the VNC window

#### Docker Benefits
- **Portability**: Runs identically on any system with Docker
- **Isolation**: No need to install Python or dependencies on your host system
- **Consistency**: Same environment for development and distribution
- **Easy Distribution**: Users only need Docker and a VNC viewer

#### Data Persistence with Docker
- Your sales data is automatically saved to `./data/sales_data.xlsx` on your host system
- Backups are stored in `./backups/` directory
- Data persists even when the container is stopped or recreated

## Testing the Application

When first launched, the application will:
1. Create a new sales_data.xlsx file if it doesn't exist
2. Display an empty sales table
3. Allow you to add new sales data through the "Nueva venta" tab

To test the application functionality:
1. Go to the "Nueva venta" tab
2. Fill in the required fields:
   - Select a date
   - Choose "Venta" as the action type
   - Select a product (e.g., "Sembra 2023")
   - Enter the quantity sold
   - Enter the price per bottle
   - Select a client type
   - Select a payment method
   - Add any observations (optional)
3. Click "Añadir Venta" to add the sale
4. Go to the "Ventas" tab to see the sale in the table
5. Go to the "Resumen" tab to see charts and statistics

The application automatically creates backups before saving any changes to your data file.

## Development Setup

### Code Quality Tools

This project uses pre-commit hooks to maintain code quality. To set up:

1. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks:
   ```
   pre-commit install
   ```

3. The hooks will run automatically when you commit changes.

### Manual Code Linting

You can run Ruff manually to check code quality:

```
ruff check .
```

Or to auto-fix issues:

```
ruff check --fix .
```

## License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
See https://creativecommons.org/licenses/by-nc/4.0/ for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

If you encounter any issues or have questions about this project, please open an issue on the GitHub repository or contact the maintainers.

## Docker Troubleshooting

### Common Issues
- **Port already in use**: If port 5901 is busy, change it in `docker-compose.yml`
- **VNC connection fails**: Ensure Docker container is running with `docker-compose ps`
- **Application doesn't start**: Check logs with `docker-compose logs -f stock-manager`

### Useful Docker Commands
```bash
# Check container status
docker-compose ps

# View real-time logs
docker-compose logs -f stock-manager

# Restart the application
docker-compose restart

# Clean rebuild (if having issues)
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```
