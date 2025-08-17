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
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        form_layout.addRow("Fecha de venta:", self.fecha_input)

        # Action input
        self.accion_input = QComboBox()
        self.accion_input.addItems(["Seleccione", "Venta", "Otro"])
        form_layout.addRow("Acción:", self.accion_input)

        # Product input
        self.producto_input = QComboBox()
        self.producto_input.addItems(["Seleccione", "Sembra 2023", "Otro"])
        form_layout.addRow("Producto:", self.producto_input)

        # Quantity input
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setMinimum(1)
        form_layout.addRow("Cantidad:", self.cantidad_input)

        # Bottle price input
        self.precio_botella_input = QDoubleSpinBox()
        self.precio_botella_input.setMinimum(0.0)
        self.precio_botella_input.setSingleStep(0.1)
        self.precio_botella_input.setDecimals(2)
        form_layout.addRow("Precio botella:", self.precio_botella_input)

        # Client input
        self.cliente_input = QComboBox()
        self.cliente_input.addItems(["Seleccione", "Muestra", "Distribución", "Horeca", "Amigos/Familia", "Público", "Otro"])
        form_layout.addRow("Tipo de cliente:", self.cliente_input)

        # Payment method input
        self.metodo_pago_input = QComboBox()
        self.metodo_pago_input.addItems(["Seleccione", "Bizum", "Efectivo", "Factura", "Otro"])
        form_layout.addRow("Método de pago:", self.metodo_pago_input)

        # Observations input
        self.observaciones_input = QTextEdit()
        form_layout.addRow("Observaciones:", self.observaciones_input)

        # Add sale button
        self.btn_agregar_venta = QPushButton("Añadir Venta")
        self.btn_agregar_venta.clicked.connect(self.agregar_venta)
        form_layout.addRow(self.btn_agregar_venta)

    def agregar_venta(self):
        """Add a new sale to the data and update the table and summary tab"""
        try:
            # Validate required fields
            if self.accion_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona una Acción.")
                return
            if self.cliente_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona un Cliente.")
                return
            if self.metodo_pago_input.currentText() == "Seleccione":
                QMessageBox.warning(self, "Campos obligatorios", "Por favor selecciona un Método de pago.")
                return
            if self.cantidad_input.value() <= 0:
                QMessageBox.warning(self, "Campos obligatorios", "La cantidad de botellas vendidas debe ser mayor que cero.")
                return
            if self.precio_botella_input.value() <= 0:
                if self.cliente_input.currentText() != "Muestra":
                    QMessageBox.warning(self, "Campos obligatorios", "El precio de la botella debe ser mayor que cero, salvo para muestras.")
                    return

            cantidad = self.cantidad_input.value()
            precio_botella = self.precio_botella_input.value()
            precio_total = round(cantidad * precio_botella, 2)

            nueva_fila = {
                "Fecha de venta": self.fecha_input.date().toString("yyyy-MM-dd"),
                "Accion": self.accion_input.currentText(),
                "Producto": self.producto_input.currentText(),
                "Botellas vendidas": cantidad,
                "Precio total venta": precio_total,
                "Precio botella": precio_botella,
                "Cliente": self.cliente_input.currentText(),
                "Observaciones": self.observaciones_input.toPlainText(),
                "Metodo de pago": self.metodo_pago_input.currentText()
            }

            # Ensure self.data has the same columns as nueva_fila
            for col in nueva_fila:
                if col not in self.data.columns:
                    self.data[col] = pd.NA

            # Concatenate without warning
            self.data = pd.concat([self.data, pd.DataFrame([nueva_fila])], ignore_index=True)
            self.handler.save_data(self.data)

            # Reset form fields
            self.accion_input.setCurrentIndex(0)
            self.producto_input.setCurrentIndex(0)
            self.cantidad_input.setValue(1)
            self.precio_botella_input.setValue(0.0)
            self.cliente_input.setCurrentIndex(0)
            self.metodo_pago_input.setCurrentIndex(0)
            self.observaciones_input.clear()

            # Update the table and summary
            self.update_callback()

            QMessageBox.information(self, "Venta añadida", "La venta se ha registrado correctamente.")

        except Exception as e:
            logging.error(f"Error al añadir venta: {e}")
            QMessageBox.critical(self, "Error inesperado", str(e))
