import pandas as pd
import os
from datetime import datetime
import logging
import shutil

class ExcelHandler:
    def __init__(self, base_path):
        """
        Initialize the Excel handler with the base path for data files.

        Args:
            base_path (str): Base directory path
        """
        self.base_path = base_path
        self.data_dir = os.path.join(base_path, "data")
        self.backup_dir = os.path.join(base_path, "backups")

        # Create directories if they don't exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)

        self.file_path = os.path.join(self.data_dir, "sales_data.xlsx")

        self.columns = [
            "Fecha de venta", "Accion", "Producto", "Botellas vendidas",
            "Precio total venta", "Precio botella", "Cliente",
            "Observaciones", "Metodo de pago"
        ]

    def load_data(self):
        """
        Load data from the Excel file.

        Returns:
            pandas.DataFrame: The loaded data
        """
        try:
            if os.path.exists(self.file_path):
                data = pd.read_excel(self.file_path)
                print(f"Data loaded successfully. Rows: {len(data)}")
                return data
            else:
                print("Excel file not found. Creating new empty DataFrame.")
                return pd.DataFrame(columns=self.columns)
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            print(f"Error loading data: {e}")
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=self.columns)

    def save_data(self, data, create_backup=True):
        """
        Save data to the Excel file.

        Args:
            data (pandas.DataFrame): The data to save
        """
        try:
            # Create backup only if requested
            if create_backup:
                self.create_backup()

            # Save data to Excel
            data.to_excel(self.file_path, index=False)
            print(f"Data saved successfully. Rows: {len(data)} | Backup: {create_backup}")

        except Exception as e:
            logging.error(f"Error saving data: {e}")
            print(f"Error saving data: {e}")
            raise

    def save_data_no_backup(self, data):
        """Save data without creating backup (for internal updates)"""
        self.save_data(data, create_backup=False)

    def create_backup(self):
        """Create a backup of the current Excel file"""
        try:
            if os.path.exists(self.file_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"sales_data_backup_{timestamp}.xlsx"
                backup_path = os.path.join(self.backup_dir, backup_filename)

                shutil.copy2(self.file_path, backup_path)
                print(f"Backup created: {backup_filename}")

        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            print(f"Error creating backup: {e}")
