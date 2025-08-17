import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QTabWidget, QMenu
)
from PySide6.QtGui import QAction

from src.utils.data_handler import ExcelHandler
from src.gui.tabs.sales_tab import SalesTableTab
from src.gui.tabs.new_sale_tab import NewSaleTab
from src.gui.tabs.summary_tab import SummaryTab

class StockManager(QMainWindow):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("Stock Manager")
        self.resize(1200, 700)
        self.version = version

        # Determine base path
        if getattr(sys, 'frozen', False):
            # Running as .exe
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Initialize data handler
        self.handler = ExcelHandler(base_path)
        self.file_path = self.handler.file_path

        # Load data
        self.data = self.handler.load_data()

        # Initialize expense history
        self.expense_history = []
        self.load_expense_history()

        # Set up the tabs
        self.setup_ui()

        # Setup menu bar
        self.setup_menu_bar()

        # Setup status bar
        self.setup_status_bar()

    def setup_ui(self):
        """Set up the main UI components"""
        self.tabs = QTabWidget()

        # Create tabs
        self.sales_tab = SalesTableTab(self.data, self.handler, self.update_summary_tab)
        self.new_sale_tab = NewSaleTab(self.data, self.handler, self.update_summary_tab)
        self.summary_tab = SummaryTab(
            self.data,
            self.expense_history,
            self.save_expense_history,
            self.file_path
        )

        # Add tabs to the tab widget
        self.tabs.addTab(self.sales_tab, "Ventas")
        self.tabs.addTab(self.new_sale_tab, "Nueva venta")
        self.tabs.addTab(self.summary_tab, "Resumen")

        # Set as central widget
        self.setCentralWidget(self.tabs)

    def setup_status_bar(self):
        """Set up the status bar with copyright information"""
        self.statusBar().showMessage(
            f"© 2025 Raúl Carrasco Romero | For support: raulcarrasco9797@gmail.com | Version: {self.version} | CC BY-NC 4.0"
        )

    def setup_menu_bar(self):
        """Set up the menu bar with Help menu"""
        menubar = self.menuBar()
        help_menu = QMenu("Ayuda", self)
        about_action = QAction("Acerca de...", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        menubar.addMenu(help_menu)

    def update_summary_tab(self):
        """Update the summary tab with the latest data"""
        self.summary_tab.update_summary_tab()

    def load_expense_history(self):
        """Load expense history from Excel file"""
        try:
            import pandas as pd
            expense_df = pd.read_excel(self.file_path, sheet_name="Gastos")
            self.expense_history = list(expense_df.itertuples(index=False, name=None))
        except Exception:
            self.expense_history = []

    def save_expense_history(self):
        """Save expense history to Excel file"""
        import pandas as pd
        expense_df = pd.DataFrame(self.expense_history, columns=["Tipo", "Importe"])
        with pd.ExcelWriter(self.file_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            expense_df.to_excel(writer, sheet_name="Gastos", index=False)

    def show_about(self):
        """Show about information dialog"""
        QMessageBox.information(
            self,
            "About",
            "Stock Manager - Gestión de ventas y stock\n"
            "© 2025 Raúl Carrasco Romero\n"
            "Licensed under Creative Commons BY-NC 4.0\n"
            "https://creativecommons.org/licenses/by-nc/4.0/\n"
            "For support: raulcarrasco9797@gmail.com"
        )
