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
