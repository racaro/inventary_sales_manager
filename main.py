# Stock Manager - Aplicación de gestión de ventas y stock
# Copyright (c) 2025 Raúl Carrasco Romero
# Licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).
# See https://creativecommons.org/licenses/by-nc/4.0/

import sys
import logging
from PySide6.QtWidgets import QApplication
from src.gui.stock_manager import StockManager

# Configure logging
logging.basicConfig(
    filename="stock_manager.log", 
    level=logging.ERROR, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SOFTWARE_VERSION = "v1.0.0"

def main():
    app = QApplication(sys.argv)
    window = StockManager(SOFTWARE_VERSION)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

# To run this application:
# 1. Open your command prompt or terminal
# 2. Navigate to the project directory:
#    cd c:\Users\Usuario\Documents\racaro\inventary_sales_manager
# 3. Run the application:
#    python main.py
#
# To create an executable:
# 1. Install pyinstaller: pip install pyinstaller
# 2. Run: pyinstaller --onefile --windowed --icon=app_icon.ico main.py
# 3. The executable will be created in the 'dist' folder
