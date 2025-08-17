import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QTabWidget, QMenu
)
from PySide6.QtGui import QAction
from PySide6.QtCore import QTimer

from src.utils.data_handler import ExcelHandler
from src.utils.config_manager import ConfigManager
from src.gui.tabs.sales_tab import SalesTableTab
from src.gui.tabs.new_sale_tab import NewSaleTab
from src.gui.tabs.summary_tab import SummaryTab

class StockManager(QMainWindow):
    def __init__(self, version):
        super().__init__()
        self.setWindowTitle("Stock Manager")
        self.resize(1200, 700)
        self.version = version

        # Initialize flags for backup control
        self.session_backup_created = False
        self.data_modified_this_session = False
        self.data_modified = False

        # Initialize tab references to None first
        self.sales_tab = None
        self.new_sale_tab = None
        self.summary_tab = None

        # Determine base path
        if getattr(sys, 'frozen', False):
            # Running as .exe
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as script
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Initialize config manager
        self.config_manager = ConfigManager(base_path)

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

        # Setup auto-save timer
        self.setup_auto_save()

    def setup_auto_save(self):
        """Setup auto-save timer to save data periodically"""
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.auto_save_data)
        self.auto_save_timer.start(30000)  # 30 seconds

    def auto_save_data(self):
        """Auto-save data if it has been modified"""
        if self.data_modified:
            try:
                self.handler.save_data_no_backup(self.data)
                print("Auto-saved data (no backup)")
                self.data_modified = False
            except Exception as e:
                print(f"Auto-save failed: {e}")

    def save_sale_data(self, data):
        """Save sale data with controlled backup creation"""
        try:
            # Update data reference in all components FIRST
            self.data = data
            self._update_all_tab_references(data)

            # Create backup only once per session
            if not self.session_backup_created:
                print("Creating session backup...")
                self.handler.save_data(data, create_backup=True)
                self.session_backup_created = True
            else:
                print("Saving without backup (session backup already exists)")
                self.handler.save_data_no_backup(data)

            # Mark data as modified
            self.data_modified_this_session = True
            self.data_modified = True

        except Exception as e:
            print(f"Error saving sale data: {e}")
            raise

    def _update_all_tab_references(self, new_data):
        """Update data references in all tabs without reloading from file"""
        if self.sales_tab:
            self.sales_tab.data = new_data

        if self.new_sale_tab:
            self.new_sale_tab.data = new_data

        if self.summary_tab:
            self.summary_tab.data = new_data

    def setup_ui(self):
        """Set up the main UI components"""
        self.tabs = QTabWidget()

        # Create tabs with config manager
        self.sales_tab = SalesTableTab(self.data, self.handler, self.safe_update_summary, self)
        self.new_sale_tab = NewSaleTab(self.data, self.handler, self.safe_update_all, self)
        self.summary_tab = SummaryTab(
            self.data,
            self.expense_history,
            self.save_expense_history,
            self.file_path,
            self.config_manager
        )

        # Add tabs to the tab widget
        self.tabs.addTab(self.sales_tab, "Ventas")
        self.tabs.addTab(self.new_sale_tab, "Nueva venta")
        self.tabs.addTab(self.summary_tab, "Resumen")

        # Set as central widget
        self.setCentralWidget(self.tabs)

    def safe_update_summary(self):
        """Safely update summary tab (checks if tab exists)"""
        if hasattr(self, 'summary_tab') and self.summary_tab is not None:
            try:
                self.update_summary_tab()
            except Exception as e:
                print(f"Error updating summary tab: {e}")

    def safe_update_all(self):
        """Safely update all tabs (checks if tabs exist)"""
        if hasattr(self, 'sales_tab') and self.sales_tab is not None:
            try:
                self.update_all_data()
            except Exception as e:
                print(f"Error updating all data: {e}")

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
        """Update only the summary tab with the current data in memory"""
        try:
            # DON'T reload from file - use current data in memory
            if self.summary_tab:
                self.summary_tab.data = self.data
                self.summary_tab.update_summary_tab()

        except Exception as e:
            print(f"Error updating summary tab: {e}")

    def update_all_data(self):
        """Update all tabs with current data in memory (NOT from file)"""
        try:
            # DON'T reload from file - use current data references

            # Update sales table display
            if self.sales_tab:
                self.sales_tab.load_table_data()

            # Update summary tab
            if self.summary_tab:
                self.summary_tab.update_summary_tab()

        except Exception as e:
            print(f"Error updating all data: {e}")

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
        try:
            import pandas as pd
            expense_df = pd.DataFrame(self.expense_history, columns=["Tipo", "Importe"])
            with pd.ExcelWriter(self.file_path, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
                expense_df.to_excel(writer, sheet_name="Gastos", index=False)
        except Exception as e:
            print(f"Error saving expense history: {e}")

    def closeEvent(self, event):
        """Handle application close event"""
        try:
            # If no session backup was created but data was modified, create one
            if self.data_modified_this_session and not self.session_backup_created:
                print("Creating backup on close...")
                self.handler.save_data(self.data, create_backup=True)
            elif self.data_modified:
                # Save any pending changes
                print("Saving final changes...")
                self.handler.save_data_no_backup(self.data)

            # Stop the auto-save timer
            if hasattr(self, 'auto_save_timer'):
                self.auto_save_timer.stop()

        except Exception as e:
            print(f"Error during close: {e}")

        event.accept()

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
