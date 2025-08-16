# Changelog

All notable changes to Stock Manager will be documented in this file.

## [1.1.0] - 2025-08-16

### Added
- Docker Support: Complete containerization with VNC access
- Cross-platform deployment (Windows, macOS, Linux)
- Automated startup scripts (`docker-start.bat`, `docker-start.sh`)
- Volume mounting for data persistence
- Comprehensive Docker documentation

### Changed
- Enhanced README with Docker installation instructions
- Updated project structure for containerization

## [1.0.0] - 2025-08-16

### Added
- Core Application: Complete sales and inventory management system
- Multi-tab Interface:
  - Sales table view
  - New sale form
  - Analytics dashboard
- Data Management:
  - Excel-based storage
  - Automatic backups
  - Data validation
- Analytics:
  - Stock tracking
  - Sales charts by client/product
  - Profit/expense tracking
- Technical:
  - PySide6 GUI framework
  - Pandas data handling
  - Matplotlib visualizations

### Technical Details
- **Platform**: Python 3.11+
- **Framework**: PySide6 (Qt)
- **Data**: Excel files with pandas
- **Charts**: Matplotlib integration
- **License**: CC BY-NC 4.0

---

## Version Summary

| Version | Release Date | Key Features |
|---------|-------------|--------------|
| **1.1.0** | 2025-08-16 | Docker deployment, VNC access, cross-platform |
| **1.0.0** | 2025-08-16 | Initial release, core features, GUI application |

## Deployment Options

- **Direct Python**: `python main.py`
- **Docker**: `docker-compose up -d` + VNC client
- **Executable**: PyInstaller build
