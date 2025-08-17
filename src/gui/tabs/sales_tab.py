import pandas as pd
import numpy as np
import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QComboBox, QDateEdit
)
from PySide6.QtCore import Qt, QDate

class SalesTableTab(QWidget):
    def __init__(self, data, handler, update_callback):
        super().__init__()
        self.data = data
        self.handler = handler
        self.update_callback = update_callback
        self.init_ui()

    def init_ui(self):
        """Initialize the sales table UI"""
        layout = QVBoxLayout(self)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.handler.columns))
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(self.handler.columns)

        # Detect changes in the table
        self.table.itemChanged.connect(self.on_table_edit)

        # Load data into table
        self.load_table_data()

        # Add buttons
        btn_update_charts = QPushButton("Actualizar gráficos")
        btn_update_charts.clicked.connect(self.update_charts_and_save)

        btn_delete_sale = QPushButton("Eliminar venta seleccionada")
        btn_delete_sale.clicked.connect(self.delete_selected_sale)

        # Add widgets to layout
        layout.addWidget(self.table)
        layout.addWidget(btn_update_charts)
        layout.addWidget(btn_delete_sale)

    def load_table_data(self):
        """Load data from DataFrame into the table with dropdown menus in specific columns"""
        try:
            self.table.setRowCount(0)
            if self.data.empty:
                return

            for row_idx, row_data in self.data.iterrows():
                self.table.insertRow(row_idx)
                for col_idx, col_name in enumerate(self.handler.columns):
                    value = row_data[col_name]
                    if pd.isna(value):
                        value = ""

                    if col_name == "Producto":
                        combo = QComboBox()
                        combo.addItems(["Sembra 2023", "Otro"])
                        combo.setCurrentText(value)
                        combo.currentIndexChanged.connect(
                            lambda _, r=row_idx, c=col_name: self.on_combo_change(r, c, combo))
                        self.table.setCellWidget(row_idx, col_idx, combo)
                    elif col_name == "Cliente":
                        combo = QComboBox()
                        combo.addItems(["Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])
                        combo.setCurrentText(value)
                        combo.currentIndexChanged.connect(
                            lambda _, r=row_idx, c=col_name: self.on_combo_change(r, c, combo))
                        self.table.setCellWidget(row_idx, col_idx, combo)
                    elif col_name == "Metodo de pago":
                        combo = QComboBox()
                        combo.addItems(["Bizum", "Efectivo", "Factura", "Otro"])
                        combo.setCurrentText(value)
                        combo.currentIndexChanged.connect(
                            lambda _, r=row_idx, c=col_name: self.on_combo_change(r, c, combo))
                        self.table.setCellWidget(row_idx, col_idx, combo)
                    elif col_name == "Accion":
                        combo = QComboBox()
                        combo.addItems(["Venta", "Otro"])
                        combo.setCurrentText(value)
                        combo.currentIndexChanged.connect(
                            lambda _, r=row_idx, c=col_name: self.on_combo_change(r, c, combo))
                        self.table.setCellWidget(row_idx, col_idx, combo)
                    elif col_name == "Fecha de venta":
                        try:
                            if isinstance(value, str) and value.strip():
                                date = QDate.fromString(value, "yyyy-MM-dd")
                            else:
                                date = QDate.currentDate()  # Use current date as default

                            date_edit = QDateEdit()
                            date_edit.setCalendarPopup(True)
                            date_edit.setDate(date)
                            date_edit.dateChanged.connect(
                                lambda _, r=row_idx, c=col_name: self.on_date_change(r, c, date_edit))
                            self.table.setCellWidget(row_idx, col_idx, date_edit)
                        except Exception as e:
                            logging.error(f"Error processing date: {e}")
                            QMessageBox.critical(self, "Error", f"Error processing date: {e}")
                    else:
                        item = QTableWidgetItem(str(value))
                        item.setFlags(item.flags() | Qt.ItemIsEditable)
                        self.table.setItem(row_idx, col_idx, item)

        except Exception as e:
            logging.error(f"Error loading data into table: {e}")
            QMessageBox.critical(self, "Error", f"Error loading data into table: {e}")

    def on_table_edit(self, item):
        """Update data and graphs when a cell is edited in the table"""
        try:
            self.table.blockSignals(True)

            row = item.row()
            col = item.column()
            new_value = item.text()
            column_name = self.handler.columns[col]

            if column_name in ["Botellas vendidas", "Precio total venta", "Precio botella"]:
                new_value = pd.to_numeric(new_value, errors="coerce")

                if column_name == "Botellas vendidas":
                    bottle_price = pd.to_numeric(self.data.at[row, "Precio botella"], errors="coerce")
                    if not pd.isna(bottle_price):
                        total_price = new_value * bottle_price
                        self.data.at[row, "Precio total venta"] = round(total_price, 2)

                        total_col_idx = self.handler.columns.index("Precio total venta")
                        item = self.table.item(row, total_col_idx)
                        if item is None:
                            item = QTableWidgetItem(str(round(total_price, 2)))
                            self.table.setItem(row, total_col_idx, item)
                        else:
                            item.setText(str(round(total_price, 2)))

                elif column_name == "Precio botella":
                    bottles_sold = pd.to_numeric(self.data.at[row, "Botellas vendidas"], errors="coerce")
                    if not pd.isna(bottles_sold):
                        total_price = new_value * bottles_sold
                        self.data.at[row, "Precio total venta"] = round(total_price, 2)

                        total_col_idx = self.handler.columns.index("Precio total venta")
                        item = self.table.item(row, total_col_idx)
                        if item is None:
                            item = QTableWidgetItem(str(round(total_price, 2)))
                            self.table.setItem(row, total_col_idx, item)
                        else:
                            item.setText(str(round(total_price, 2)))

            elif column_name == "Producto":
                new_value = new_value if new_value == "Sembra 2023" else "Otro"
            else:
                new_value = str(new_value)

            # Update DataFrame with new value
            self.data.at[row, column_name] = new_value

            # Save updated data to Excel file
            self.handler.save_data(self.data)

            # Refresh summary graphs
            self.update_callback()

        except Exception as e:
            logging.error(f"Error updating data: {e}")
            QMessageBox.critical(self, "Error", f"Error updating data: {e}")

        finally:
            # Reconnect itemChanged event
            self.table.blockSignals(False)

    def on_combo_change(self, row, column_name, combo):
        """Update DataFrame when a value is selected in a QComboBox"""
        try:
            new_value = combo.currentText()

            if column_name == "Cliente":
                valid_clients = [
                    "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"
                ]
                if new_value not in valid_clients:
                    new_value = "Otro"

            if column_name == "Producto":
                new_value = new_value if new_value == "Sembra 2023" else "Otro"

            # Update DataFrame
            self.data.at[row, column_name] = new_value

            # Save updated data to Excel file
            self.handler.save_data(self.data)

            # Refresh summary graphs
            self.update_callback()

        except Exception as e:
            logging.error(f"Error updating dropdown value: {e}")
            QMessageBox.critical(self, "Error", f"Error updating dropdown value: {e}")

    def on_date_change(self, row, column_name, date_edit):
        """Update DataFrame when a new date is selected in a QDateEdit"""
        try:
            new_value = date_edit.date().toString("yyyy-MM-dd")
            self.data.at[row, column_name] = new_value
            self.handler.save_data(self.data)
            self.update_callback()
        except Exception as e:
            logging.error(f"Error updating date: {e}")
            QMessageBox.critical(self, "Error", f"Error updating date: {e}")

    def sync_table_to_dataframe(self):
        """Sync visible data in table with internal DataFrame"""
        float_columns = ["Precio total venta", "Precio botella"]
        int_columns = ["Botellas vendidas"]
        for row in range(self.table.rowCount()):
            for col, col_name in enumerate(self.handler.columns):
                widget = self.table.cellWidget(row, col)
                if isinstance(widget, QComboBox):
                    value = widget.currentText()
                elif isinstance(widget, QDateEdit):
                    value = widget.date().toString("yyyy-MM-dd")
                else:
                    item = self.table.item(row, col)
                    value = item.text() if item else ""

                if col_name in float_columns:
                    if value == "":
                        value = np.nan
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = np.nan
                elif col_name in int_columns:
                    if value == "":
                        value = 0
                    else:
                        try:
                            value = int(float(value))
                        except ValueError:
                            value = 0
                self.data.at[row, col_name] = value

    def update_charts_and_save(self):
        """Sync table, save data, and update summary graphs"""
        try:
            self.sync_table_to_dataframe()
            self.handler.save_data(self.data)
            self.update_callback()
        except Exception as e:
            logging.error(f"Error saving and updating graphs: {e}")
            QMessageBox.critical(self, "Error", f"Error saving and updating graphs: {e}")

    def delete_selected_sale(self):
        """Delete selected sale in table and update DataFrame and graphs"""
        try:
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Invalid selection", "Please select a row to delete.")
                return
            response = QMessageBox.question(
                self, "Confirm deletion", "Are you sure you want to delete this sale?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response != QMessageBox.Yes:
                return
            self.data = self.data.drop(index=selected_row).reset_index(drop=True)
            self.handler.save_data(self.data)
            self.load_table_data()
            self.update_callback()
            QMessageBox.information(self, "Sale deleted", "The sale has been successfully deleted.")
        except Exception as e:
            logging.error(f"Error deleting sale: {e}")
            QMessageBox.critical(self, "Error", f"Error deleting sale: {e}")
