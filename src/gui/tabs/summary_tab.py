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
    def __init__(self, data, expense_history, save_expenses_callback, file_path):
        super().__init__()
        self.data = data
        self.expense_history = expense_history
        self.save_expenses_callback = save_expenses_callback
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
        initial_stock_layout = QHBoxLayout()
        QLabel("Stock inicial:")

        # Stock inputs for each product
        self.initial_stock_inputs = {}
        products = ["Producto1", "Producto2", "Producto3"]

        for product in products:
            product_layout = QVBoxLayout()
            product_label = QLabel(f"{product}:")
            product_input = QSpinBox()
            product_input.setMinimum(0)
            product_input.setMaximum(10000)
            product_input.setValue(0)  # Default value
            product_input.valueChanged.connect(self.update_summary_tab)

            product_layout.addWidget(product_label)
            product_layout.addWidget(product_input)

            self.initial_stock_inputs[product] = product_input
            initial_stock_layout.addLayout(product_layout)

        self.stock_layout.addLayout(initial_stock_layout)
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
        expense_layout = QHBoxLayout()
        expense_label = QLabel("Introduce los gastos:")
        self.expense_input = QLineEdit()
        self.expense_input.setPlaceholderText("Introduce los gastos (€)")
        self.expense_input.textChanged.connect(self.update_summary_tab)
        self.expense_type_input = QLineEdit()
        self.expense_type_input.setPlaceholderText("Tipo de gasto (opcional)")

        # Add expense buttons
        self.btn_add_expense = QPushButton("Añadir gasto")
        self.btn_add_expense.clicked.connect(self.add_expense)
        self.btn_reset_expenses = QPushButton("Resetear gastos")
        self.btn_reset_expenses.clicked.connect(self.reset_expenses)

        # Add all widgets to expense layout
        expense_layout.addWidget(expense_label)
        expense_layout.addWidget(self.expense_input)
        expense_layout.addWidget(self.expense_type_input)
        expense_layout.addWidget(self.btn_add_expense)
        expense_layout.addWidget(self.btn_reset_expenses)

        self.gains_layout.addLayout(expense_layout)
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
            self._clear_layout(self.stock_layout, preserve_first=1)
            self._clear_layout(self.client_layout)
            self._clear_layout(self.product_layout)
            self._clear_layout(self.gains_layout, preserve_first=1)

            # Ensure columns are numeric
            self.data["Cantidad vendida"] = pd.to_numeric(self.data["Cantidad vendida"], errors="coerce").fillna(0)
            self.data["Precio total venta"] = pd.to_numeric(self.data["Precio total venta"], errors="coerce").fillna(0)

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
        # Get initial stock values from inputs
        initial_stock = {}
        for product, input_widget in self.initial_stock_inputs.items():
            initial_stock[product] = input_widget.value()

        # Sales by product
        sales_by_product = self.data.groupby("Producto")["Cantidad vendida"].sum()

        # Calculate remaining stock for all products
        remaining_stock = {}
        all_products = ["Producto1", "Producto2", "Producto3", "Otro"]

        for product in all_products:
            initial = initial_stock.get(product, 0)
            sold = sales_by_product.get(product, 0)
            remaining_stock[product] = initial - sold

        # Create series with all products
        remaining_stock_series = pd.Series(remaining_stock)[all_products]

        # Draw the chart
        figure_stock = Figure()
        canvas_stock = FigureCanvas(figure_stock)
        ax_stock = figure_stock.add_subplot(111)
        remaining_stock_series.plot(kind="bar", ax=ax_stock, color="green")
        ax_stock.set_title("Stock Restante por Producto")
        ax_stock.set_ylabel("Cantidad Disponible")
        ax_stock.set_xlabel("Producto")
        figure_stock.tight_layout()
        self.stock_layout.addWidget(canvas_stock)

        # Show remaining stock as text below the chart
        stock_text = "\n".join([f"{prod}: {cant}" for prod, cant in remaining_stock.items()])
        stock_label = QLabel(f"Stock restante:\n{stock_text}")
        self.stock_layout.addWidget(stock_label)

    def _update_client_tab(self):
        """Update the client tab with sales by client information"""
        # List of valid clients
        valid_clients = {
            "Muestra": "Muestra",
            "Distribución": "Distribución",
            "Horeca": "Horeca",
            "Amigos/Fam": "Amigos/Familia",
            "Amigos/Familia": "Amigos/Familia",
            "Público": "Público",
            "Otro": "Otro"
        }

        # Normalize the values in the "Cliente" column
        self.data["Cliente"] = self.data["Cliente"].map(valid_clients).fillna("Otro")

        # Filter data to include only valid clients
        filtered_clients = self.data[self.data["Cliente"].isin(valid_clients.values())]
        sales_by_client = filtered_clients.groupby("Cliente")["Cantidad vendida"].sum()

        # Draw the chart
        figure_client = Figure()
        canvas_client = FigureCanvas(figure_client)
        ax_client = figure_client.add_subplot(111)
        sales_by_client.plot(kind="bar", ax=ax_client, color="blue")
        ax_client.set_title("Ventas por Cliente")
        ax_client.set_ylabel("Cantidad Vendida")
        ax_client.set_xlabel("Cliente")
        figure_client.tight_layout()
        self.client_layout.addWidget(canvas_client)

    def _update_product_tab(self):
        """Update the product tab with sales by product information"""
        # Sales by product
        sales_by_product = self.data.groupby("Producto")["Cantidad vendida"].sum()

        # Ensure all products are present in the index
        all_products = ["Producto1", "Producto2", "Producto3", "Otro"]
        for prod in all_products:
            if prod not in sales_by_product.index:
                sales_by_product[prod] = 0

        # Sort the index so they always appear the same
        sales_by_product = sales_by_product[all_products]

        # Draw the chart
        figure_product = Figure()
        canvas_product = FigureCanvas(figure_product)
        ax_product = figure_product.add_subplot(111)
        sales_by_product.plot(kind="bar", ax=ax_product, color="orange")
        ax_product.set_title("Ventas por Producto")
        ax_product.set_ylabel("Cantidad Vendida")
        ax_product.set_xlabel("Producto")
        figure_product.tight_layout()
        self.product_layout.addWidget(canvas_product)

    def _update_gains_tab(self):
        """Update the gains tab with total gains information"""
        # Calculate total gain, expenses, and net gain
        total_gain = self.data["Precio total venta"].sum()
        expenses = sum(amount for _, amount in self.expense_history)
        net_gain = total_gain - expenses

        # Calculate average selling price
        average_price = self.data["Precio unitario"].mean()

        # Display gains information
        gains_text = (
            f"Ganancia total: {total_gain:.2f} €\n"
            f"Gastos: {expenses:.2f} €\n"
            f"Ganancia neta: {net_gain:.2f} €\n"
            f"Precio medio: {average_price:.2f} €"
        )
        gains_label = QLabel(gains_text)
        gains_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.gains_layout.addWidget(gains_label)

        # Display total profit by payment method
        profit_by_method = self.data.groupby("Metodo de pago")["Precio total venta"].sum()
        profit_text = "Beneficio total por método de pago:\n"
        for method, total in profit_by_method.items():
            profit_text += f"{method}: {total:.2f} €\n"
        profit_label = QLabel(profit_text)
        self.gains_layout.addWidget(profit_label)

        # Display expense history
        history_text = "Historial de gastos:\n"
        if self.expense_history:
            for idx, (expense_type, amount) in enumerate(self.expense_history, 1):
                history_text += f"{idx}. {expense_type}: {amount:.2f} €\n"
        else:
            history_text += "Sin gastos registrados."
        expense_history_label = QLabel(history_text)
        self.gains_layout.addWidget(expense_history_label)

    def add_expense(self):
        """Add a new expense to the history and update the summary"""
        try:
            expense_type = self.expense_type_input.text().strip()
            try:
                amount = float(self.expense_input.text().replace(",", "."))
            except ValueError:
                amount = 0.0

            if amount <= 0:
                QMessageBox.warning(self, "Gasto inválido", "Introduce un importe mayor que cero.")
                return

            self.expense_history.append((expense_type, amount))
            self.expense_type_input.clear()
            self.expense_input.clear()
            self.save_expenses_callback()
            self.update_summary_tab()
        except Exception:
            QMessageBox.warning(self, "Gasto inválido", "Introduce un valor numérico para el gasto.")

    def reset_expenses(self):
        """Reset the expense history and update the gains tab"""
        try:
            response = QMessageBox.question(
                self,
                "Confirmar reseteo",
                "¿Seguro que quieres borrar todos los gastos?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.Yes:
                self.expense_history.clear()
                self.save_expenses_callback()
                self.update_summary_tab()
        except Exception as e:
            logging.error(f"Error resetting expenses: {e}")
            QMessageBox.critical(self, "Error", f"Error resetting expenses: {e}")
