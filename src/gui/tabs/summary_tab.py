import pandas as pd
import logging
from PySide6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QMessageBox
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SummaryTab(QWidget):
    def __init__(self, data, gastos_historial, save_gastos_callback, file_path):
        super().__init__()
        self.data = data
        self.gastos_historial = gastos_historial
        self.save_gastos_callback = save_gastos_callback
        self.file_path = file_path
        self.init_ui()

    def init_ui(self):
        """Initialize the summary tab UI with separate tabs for each type of graph"""
        layout = QVBoxLayout(self)

        # Create tab widget for different summary views
        self.summary_tabs = QTabWidget()

        # Stock tab
        self.stock_container = QWidget()
        self.stock_layout = QVBoxLayout(self.stock_container)

        # Add stock initial input to stock tab
        stock_inicial_layout = QHBoxLayout()
        stock_inicial_label = QLabel("Stock inicial Sembra 2023:")
        self.stock_inicial_input = QSpinBox()
        self.stock_inicial_input.setMinimum(0)
        self.stock_inicial_input.setMaximum(10000)
        self.stock_inicial_input.setValue(1850)
        self.stock_inicial_input.valueChanged.connect(self.update_summary_tab)
        stock_inicial_layout.addWidget(stock_inicial_label)
        stock_inicial_layout.addWidget(self.stock_inicial_input)
        self.stock_layout.addLayout(stock_inicial_layout)

        self.summary_tabs.addTab(self.stock_container, "Stock Restante")

        # Client tab
        self.client_container = QWidget()
        self.client_layout = QVBoxLayout(self.client_container)
        self.summary_tabs.addTab(self.client_container, "Ventas por Cliente")

        # Product tab
        self.product_container = QWidget()
        self.product_layout = QVBoxLayout(self.product_container)
        self.summary_tabs.addTab(self.product_container, "Ventas por Producto")

        # Gains tab
        self.gains_container = QWidget()
        self.gains_layout = QVBoxLayout(self.gains_container)

        # Add expense inputs
        gastos_layout = QHBoxLayout()
        gastos_label = QLabel("Introduce los gastos:")
        self.gastos_input = QLineEdit()
        self.gastos_input.setPlaceholderText("Introduce los gastos (€)")
        self.gastos_input.textChanged.connect(self.update_summary_tab)
        self.tipo_gasto_input = QLineEdit()
        self.tipo_gasto_input.setPlaceholderText("Tipo de gasto (opcional)")

        # Add expense buttons
        self.btn_agregar_gasto = QPushButton("Añadir gasto")
        self.btn_agregar_gasto.clicked.connect(self.agregar_gasto)
        self.btn_resetear_gastos = QPushButton("Resetear gastos")
        self.btn_resetear_gastos.clicked.connect(self.resetear_gastos)

        # Add all widgets to expense layout
        gastos_layout.addWidget(gastos_label)
        gastos_layout.addWidget(self.gastos_input)
        gastos_layout.addWidget(self.tipo_gasto_input)
        gastos_layout.addWidget(self.btn_agregar_gasto)
        gastos_layout.addWidget(self.btn_resetear_gastos)

        self.gains_layout.addLayout(gastos_layout)
        self.summary_tabs.addTab(self.gains_container, "Ganancias")

        # Add summary tabs to main layout
        layout.addWidget(self.summary_tabs)

        # Update the summary tab with initial data
        self.update_summary_tab()

    def update_summary_tab(self):
        """Update the summary tabs with the latest data"""
        try:
            if self.data.empty:
                return

            # Clear current content of all tabs
            self._clear_layout(self.stock_layout, preserve_first=1)  # Preserve stock initial input
            self._clear_layout(self.client_layout)
            self._clear_layout(self.product_layout)
            self._clear_layout(self.gains_layout, preserve_first=1)  # Preserve expense inputs

            # Ensure columns are numeric
            self.data["Botellas vendidas"] = pd.to_numeric(self.data["Botellas vendidas"], errors="coerce").fillna(0)
            self.data["Precio total venta"] = pd.to_numeric(self.data["Precio total venta"], errors="coerce").fillna(0)

            # Classify products that aren't "Sembra 2023" as "Otro"
            self.data["Producto"] = self.data["Producto"].apply(lambda x: x if x == "Sembra 2023" else "Otro")

            # --- Stock Remaining ---
            self._update_stock_tab()

            # --- Sales by Client ---
            self._update_client_tab()

            # --- Sales by Product ---
            self._update_product_tab()

            # --- Total Gains ---
            self._update_gains_tab()

        except Exception as e:
            logging.error(f"Error updating summary tabs: {e}")
            QMessageBox.critical(self, "Error", f"Error updating summary tabs: {e}")

    def _clear_layout(self, layout, preserve_first=0):
        """Clear all widgets from a layout except for the first n items if specified"""
        if layout is None:
            return

        # Get all items that need to be removed
        items_to_remove = []
        for i in range(preserve_first, layout.count()):
            items_to_remove.append(layout.itemAt(i))

        # Remove items from the layout
        for item in items_to_remove:
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
            layout.removeItem(item)

    def _update_stock_tab(self):
        """Update the stock tab with remaining stock information"""
        # Initial stock values
        stock_inicial = {"Sembra 2023": self.stock_inicial_input.value(), "Otro": 0}

        # Sales by product
        ventas_por_producto = self.data.groupby("Producto")["Botellas vendidas"].sum()

        # Calculate remaining stock for both products
        stock_restante = {}
        for producto in stock_inicial:
            vendido = ventas_por_producto.get(producto, 0)
            stock_restante[producto] = stock_inicial[producto] - vendido

        # Ensure both products are present and in order
        for prod in ["Sembra 2023", "Otro"]:
            if prod not in stock_restante:
                stock_restante[prod] = stock_inicial.get(prod, 0)
        stock_restante_series = pd.Series(stock_restante)[["Sembra 2023", "Otro"]]

        # Draw the chart
        figure_stock = Figure()
        canvas_stock = FigureCanvas(figure_stock)
        ax_stock = figure_stock.add_subplot(111)
        stock_restante_series.plot(kind="bar", ax=ax_stock, color="green")
        ax_stock.set_title("Stock Restante por Producto")
        ax_stock.set_ylabel("Cantidad Disponible")
        ax_stock.set_xlabel("Producto")
        figure_stock.tight_layout()
        self.stock_layout.addWidget(canvas_stock)

        # Show remaining stock as text below the chart
        stock_text = "\n".join([f"{prod}: {cant}" for prod, cant in stock_restante.items()])
        stock_label = QLabel(f"Stock restante:\n{stock_text}")
        self.stock_layout.addWidget(stock_label)

    def _update_client_tab(self):
        """Update the client tab with sales by client information"""
        # List of valid clients
        clientes_validos = {
            "Muestra": "Muestra",
            "Distribución": "Distribución",
            "Horeca": "Horeca",
            "Amigos/Fam": "Amigos/Familia",
            "Amigos/Familia": "Amigos/Familia",
            "Público": "Público",
            "Otro": "Otro"
        }

        # Normalize the values in the "Cliente" column
        self.data["Cliente"] = self.data["Cliente"].map(clientes_validos).fillna("Otro")

        # Filter data to include only valid clients
        clientes_filtrados = self.data[self.data["Cliente"].isin(clientes_validos.values())]
        ventas_por_cliente = clientes_filtrados.groupby("Cliente")["Botellas vendidas"].sum()

        # Draw the chart
        figure_client = Figure()
        canvas_client = FigureCanvas(figure_client)
        ax_client = figure_client.add_subplot(111)
        ventas_por_cliente.plot(kind="bar", ax=ax_client, color="blue")
        ax_client.set_title("Ventas por Cliente")
        ax_client.set_ylabel("Cantidad Vendida")
        ax_client.set_xlabel("Cliente")
        figure_client.tight_layout()
        self.client_layout.addWidget(canvas_client)

    def _update_product_tab(self):
        """Update the product tab with sales by product information"""
        # Sales by product
        ventas_por_producto = self.data.groupby("Producto")["Botellas vendidas"].sum()

        # Ensure both products are present in the index
        for prod in ["Sembra 2023", "Otro"]:
            if prod not in ventas_por_producto.index:
                ventas_por_producto[prod] = 0

        # Sort the index so they always appear the same
        ventas_por_producto = ventas_por_producto[["Sembra 2023", "Otro"]]

        # Draw the chart
        figure_producto = Figure()
        canvas_producto = FigureCanvas(figure_producto)
        ax_producto = figure_producto.add_subplot(111)
        ventas_por_producto.plot(kind="bar", ax=ax_producto, color="orange")
        ax_producto.set_title("Ventas por Producto")
        ax_producto.set_ylabel("Cantidad Vendida")
        ax_producto.set_xlabel("Producto")
        figure_producto.tight_layout()
        self.product_layout.addWidget(canvas_producto)

    def _update_gains_tab(self):
        """Update the gains tab with total gains information"""
        # Calculate total gain, expenses, and net gain
        ganancia_total = self.data["Precio total venta"].sum()
        gastos = sum(importe for _, importe in self.gastos_historial)
        ganancia_neta = ganancia_total - gastos

        # Calculate average selling price
        precio_medio = self.data["Precio botella"].mean()

        # Display gains information
        ganancias_text = (
            f"Ganancia total: {ganancia_total:.2f} €\n"
            f"Gastos: {gastos:.2f} €\n"
            f"Ganancia neta: {ganancia_neta:.2f} €\n"
            f"Precio medio: {precio_medio:.2f} €"
        )
        ganancias_label = QLabel(ganancias_text)
        ganancias_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.gains_layout.addWidget(ganancias_label)

        # Display total profit by payment method
        beneficio_por_metodo = self.data.groupby("Metodo de pago")["Precio total venta"].sum()
        beneficio_text = "Beneficio total por método de pago:\n"
        for metodo, total in beneficio_por_metodo.items():
            beneficio_text += f"{metodo}: {total:.2f} €\n"
        beneficio_label = QLabel(beneficio_text)
        self.gains_layout.addWidget(beneficio_label)

        # Display expense history
        historial_text = "Historial de gastos:\n"
        if self.gastos_historial:
            for idx, (tipo, importe) in enumerate(self.gastos_historial, 1):
                historial_text += f"{idx}. {tipo}: {importe:.2f} €\n"
        else:
            historial_text += "Sin gastos registrados."
        gastos_historial_label = QLabel(historial_text)
        self.gains_layout.addWidget(gastos_historial_label)

    def agregar_gasto(self):
        """Add a new expense to the history and update the summary"""
        try:
            tipo = self.tipo_gasto_input.text().strip()
            try:
                importe = float(self.gastos_input.text().replace(",", "."))
            except ValueError:
                importe = 0.0

            if importe <= 0:
                QMessageBox.warning(self, "Gasto inválido", "Introduce un importe mayor que cero.")
                return

            self.gastos_historial.append((tipo, importe))
            self.tipo_gasto_input.clear()
            self.gastos_input.clear()
            self.save_gastos_callback()
            self.update_summary_tab()
        except Exception:
            QMessageBox.warning(self, "Gasto inválido", "Introduce un valor numérico para el gasto.")

    def resetear_gastos(self):
        """Reset the expense history and update the gains tab"""
        try:
            respuesta = QMessageBox.question(
                self,
                "Confirmar reseteo",
                "¿Seguro que quieres borrar todos los gastos?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.gastos_historial.clear()
                self.save_gastos_callback()
                self.update_summary_tab()
        except Exception as e:
            logging.error(f"Error resetting expenses: {e}")
            QMessageBox.critical(self, "Error", f"Error resetting expenses: {e}")
