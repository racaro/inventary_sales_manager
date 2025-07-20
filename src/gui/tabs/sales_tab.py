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
        btn_actualizar_graficos = QPushButton("Actualizar gráficos")
        btn_actualizar_graficos.clicked.connect(self.actualizar_graficos_y_guardar)

        btn_eliminar_venta = QPushButton("Eliminar venta seleccionada")
        btn_eliminar_venta.clicked.connect(self.eliminar_venta_seleccionada)

        # Add widgets to layout
        layout.addWidget(self.table)
        layout.addWidget(btn_actualizar_graficos)
        layout.addWidget(btn_eliminar_venta)

    def load_table_data(self):
        """Load data from DataFrame into the table with dropdown menus in specific columns"""
        try:
            self.table.setRowCount(0)
            if self.data.empty:
                return
                
            # Iterate through DataFrame rows and add them to table
            for row_idx, row_data in self.data.iterrows():
                self.table.insertRow(row_idx)
                for col_idx, col_name in enumerate(self.handler.columns):
                    value = row_data[col_name]
                    if pd.isna(value):
                        value = ""  # Handle NaN values

                    # Add dropdowns in specific columns
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
                            # Make sure value is a valid string
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
            # Temporarily disconnect itemChanged event to avoid recursion
            self.table.blockSignals(True)

            row = item.row()
            col = item.column()
            new_value = item.text()

            # Get column name
            column_name = self.handler.columns[col]

            # Convert value to expected data type
            if column_name in ["Botellas vendidas", "Precio total venta", "Precio botella"]:
                new_value = pd.to_numeric(new_value, errors="coerce")  # Convert to numeric

                # If "Botellas vendidas" is modified, update "Precio total venta"
                if column_name == "Botellas vendidas":
                    precio_botella = pd.to_numeric(self.data.at[row, "Precio botella"], errors="coerce")
                    if not pd.isna(precio_botella):
                        precio_total = new_value * precio_botella
                        self.data.at[row, "Precio total venta"] = round(precio_total, 2)

                        # Update "Precio total venta" cell in table
                        total_col_idx = self.handler.columns.index("Precio total venta")
                        item = self.table.item(row, total_col_idx)
                        if item is None:
                            item = QTableWidgetItem(str(round(precio_total, 2)))
                            self.table.setItem(row, total_col_idx, item)
                        else:
                            item.setText(str(round(precio_total, 2)))

                # If "Precio botella" is modified, update "Precio total venta"
                elif column_name == "Precio botella":
                    botellas_vendidas = pd.to_numeric(self.data.at[row, "Botellas vendidas"], errors="coerce")
                    if not pd.isna(botellas_vendidas):
                        precio_total = new_value * botellas_vendidas
                        self.data.at[row, "Precio total venta"] = round(precio_total, 2)

                        # Update "Precio total venta" cell in table
                        total_col_idx = self.handler.columns.index("Precio total venta")
                        item = self.table.item(row, total_col_idx)
                        if item is None:
                            item = QTableWidgetItem(str(round(precio_total, 2)))
                            self.table.setItem(row, total_col_idx, item)
                        else:
                            item.setText(str(round(precio_total, 2)))

            elif column_name == "Producto":
                # Classify products that are not "Sembra 2023" as "Otro"
                new_value = new_value if new_value == "Sembra 2023" else "Otro"
            else:
                new_value = str(new_value)  # For other columns, use string

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

            # Normalize client value to always be one of the valid ones
            if column_name == "Cliente":
                clientes_validos = [
                    "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"
                ]
                if new_value not in clientes_validos:
                    new_value = "Otro"

            # Classify products that are not "Sembra 2023" as "Otro"
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

                # Type conversion based on column
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

    def actualizar_graficos_y_guardar(self):
        """Sync table, save data, and update summary graphs"""
        try:
            self.sync_table_to_dataframe()
            self.handler.save_data(self.data)
            self.update_callback()
        except Exception as e:
            logging.error(f"Error saving and updating graphs: {e}")
            QMessageBox.critical(self, "Error", f"Error saving and updating graphs: {e}")

    def eliminar_venta_seleccionada(self):
        """Delete selected sale in table and update DataFrame and graphs"""
        try:
            fila_seleccionada = self.table.currentRow()
            if fila_seleccionada < 0:
                QMessageBox.warning(self, "Invalid selection", "Please select a row to delete.")
                return
            respuesta = QMessageBox.question(
                self, "Confirm deletion", "Are you sure you want to delete this sale?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta != QMessageBox.Yes:
                return
            self.data = self.data.drop(index=fila_seleccionada).reset_index(drop=True)
            self.handler.save_data(self.data)
            self.load_table_data()
            self.update_callback()
            QMessageBox.information(self, "Sale deleted", "The sale has been successfully deleted.")
        except Exception as e:
            logging.error(f"Error deleting sale: {e}")
            QMessageBox.critical(self, "Error", f"Error deleting sale: {e}")