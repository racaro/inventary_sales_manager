# Wine Sales Management System

## Overview
This project is a simple, local wine sales management system built using **Python**, **Streamlit**, and **Excel** for data storage. It provides a graphical interface to manage wine inventory, register sales, track customer transactions, and calculate profits.

---

## Features
- **User-Friendly Interface with Streamlit**: Easily navigate between registering sales, viewing inventory, and generating reports.
- **Excel-Based Database**: Store and manage data for wines, customers, and sales without requiring a cloud service or external database.
- **Real-Time Stock Updates**: Automatically update inventory levels when sales are registered.
- **Profit Tracking**: Monitor and calculate profits based on sales data.
- **Client Information Management**: Record and manage sales by customer type and name.

---

## Project Structure
```
inventary_sales_manager/
├── app.py                      # Main entry point for the application
├── requirements.txt            # Dependencies for the project
├── src/                        # Sources module
│   │── data/                   # Business logic modules
│   │   └── inventario.xlsx     # Excel file for data storage
│   │── utils/                  # Utility modules
│   │   └── __init__.py         # Module initializer
│   └── __init__.py             # Module initializer
└── tests/                      # Unit tests

```

---

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/racaro/inventary_sales_manager.git
   cd inventary_sales_manager
   ```

2. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Ensure you have an Excel file (`inventario.xlsx`) with the appropriate structure in the `src/data` folder.

4. Run the application:
   ```sh
   streamlit run app.py
   ```

---

## Usage
- **Registrar Venta**: Enter wine name, quantity, price, and customer details to record a sale.
- **Ver Inventario**: View a table of the current stock and prices.
- **Reporte de Ventas**: Analyze sales data with visualizations (coming soon).

---

## Dependencies
- Python 3.x
- Streamlit
- pandas
- openpyxl

---

## Future Enhancements
- Add **sales analytics and visualization**.
- Implement **user authentication**.
- Support **mobile-friendly layouts**.

---

## License
This project is licensed under the MIT License.


