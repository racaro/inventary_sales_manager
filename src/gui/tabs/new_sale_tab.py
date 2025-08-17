import pandas as pd
import logging
from PySide6.QtWidgets import (
    QWidget, QFormLayout, QDateEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QTextEdit, QPushButton, QMessageBox
)
from PySide6.QtCore import QDate

class NewSaleTab(QWidget):
    def __init__(self, data, handler, update_callback):
        super().__init__()
        self.data = data
        self.handler = handler
        self.update_callback = update_callback
        self.init_ui()

    def init_ui(self):
        """Initialize the form for inputting new sales data"""
        form_layout = QFormLayout(self)

        # Date input
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Fecha de venta:", self.date_input)

        # Action input
        self.action_input = QComboBox()
        self.action_input.addItems(["Seleccione", "Venta", "Otro"])
        form_layout.addRow("Acción:", self.action_input)

        # Product input
        self.product_input = QComboBox()
        self.product_input.addItems(["Seleccione", "Sembra 2023", "Otro"])
        form_layout.addRow("Producto:", self.product_input)

        # Quantity input
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        form_layout.addRow("Cantidad:", self.quantity_input)

        # Bottle price input
        self.bottle_price_input = QDoubleSpinBox()
        self.bottle_price_input.setMinimum(0.0)
        self.bottle_price_input.setSingleStep(0.1)
        self.bottle_price_input.setDecimals(2)
        form_layout.addRow("Precio botella:", self.bottle_price_input)

        # Client input
        self.client_input = QComboBox()
        self.client_input.addItems(["Seleccione", "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])
        form_layout.addRow("Tipo de cliente:", self.client_input)

        # Payment method input
        self.payment_method_input = QComboBox()
        self.payment_method_input.addItems(["Seleccione", "Bizum", "Efectivo", "Factura", "Otro"])
        form_layout.addRow("Método de pago:", self.payment_method_input)

        # Observations input
        self.observations_input = QTextEdit()
        form_layout.addRow("Observaciones:", self.observations_input)

        # Add sale button
        self.btn_add_sale = QPushButton("Añadir Venta")
        self.btn_add_sale.clicked.connect(self.add_sale)
        form_layout.addRow(self.btn_add_sale)

    def add_sale(self):
        """Add a new sale to the data and update the table and summary tab"""
        try:
            # Validate required fields
            if self.action_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona una Acción.")
                return
            if self.client_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona un Cliente.")
                return
            if self.payment_method_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona un Método de pago.")
                return
            if self.quantity_input.value() <= 0:
                QMessageBox.warning(self, "Campos obligatorios", "La cantidad de botellas vendidas debe ser mayor que cero.")
                return
            if self.bottle_price_input.value() <= 0:
                if self.client_input.currentText() != "Muestra":
                    QMessageBox.warning(self, "Campos obligatorios", "El precio de la botella debe ser mayor que cero, salvo para muestras.")
                    return

            quantity = self.quantity_input.value()
            bottle_price = self.bottle_price_input.value()
            total_price = round(quantity * bottle_price, 2)

            new_row = {
                "Fecha de venta": self.date_input.date().toString("yyyy-MM-dd"),
                "Accion": self.action_input.currentText(),
                "Producto": self.product_input.currentText(),
                "Botellas vendidas": quantity,
                "Precio total venta": total_price,
                "Precio botella": bottle_price,
                "Cliente": self.client_input.currentText(),
                "Observaciones": self.observations_input.toPlainText(),
                "Metodo de pago": self.payment_method_input.currentText()
            }

            for col in new_row:
                if col not in self.data.columns:
                    self.data[col] = pd.NA

            # Concatenate without warning
            self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
            self.handler.save_data(self.data)

            # Reset form fields
            self.action_input.setCurrentIndex(0)
            self.product_input.setCurrentIndex(0)
            self.quantity_input.setValue(1)
            self.bottle_price_input.setValue(0.0)
            self.client_input.setCurrentIndex(0)
            self.payment_method_input.setCurrentIndex(0)
            self.observations_input.clear()

            # Update the table and summary
            self.update_callback()

            QMessageBox.information(self, "Venta añadida", "La venta se ha registrado correctamente.")

        except Exception as e:
            logging.error(f"Error al añadir venta: {e}")
            QMessageBox.critical(self, "Error inesperado", str(e))
