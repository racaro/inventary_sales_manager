import os
import pandas as pd
import logging
from datetime import datetime
import shutil

class ExcelHandler:
    def __init__(self, base_path):
        """
        Initialize the Excel handler with the base path for data files.
        
        Args:
            base_path (str): Base directory path
        """
        self.base_path = base_path
        self.file_path = os.path.join(base_path, "sales_data.xlsx")
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
            # Check if file exists, create if not
            if not os.path.exists(self.file_path):
                self._create_empty_excel()
                return pd.DataFrame(columns=self.columns)
                
            data = pd.read_excel(self.file_path)
            # Ensure all expected columns are present
            for col in self.columns:
                if col not in data.columns:
                    data[col] = pd.NA
            return data
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=self.columns)
    
    def _create_empty_excel(self):
        """Create an empty Excel file with required columns"""
        try:
            df = pd.DataFrame(columns=self.columns)
            df.to_excel(self.file_path, index=False)
            logging.info(f"Created new data file at {self.file_path}")
        except Exception as e:
            logging.error(f"Error creating empty Excel file: {e}")
            
    def save_data(self, data):
        """
        Save data to the Excel file.
        
        Args:
            data (pandas.DataFrame): The data to save
        """
        try:
            # Create backup before saving
            self._create_backup()
            
            # Save data to Excel
            data.to_excel(self.file_path, index=False)
            
        except Exception as e:
            logging.error(f"Error saving data: {e}")
            raise
            
    def _create_backup(self):
        """Create a backup of the Excel file before saving"""
        if not os.path.exists(self.file_path):
            return
            
        try:
            # Create backups directory if it doesn't exist
            backups_dir = os.path.join(self.base_path, "backups")
            if not os.path.exists(backups_dir):
                os.makedirs(backups_dir)
                
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backups_dir, f"sales_data_backup_{timestamp}.xlsx")
            
            # Copy the current file to backup
            shutil.copy2(self.file_path, backup_file)
            
        except Exception as e:
            logging.error(f"Error creating backup: {e}")
            # Continue without backup if it fails
