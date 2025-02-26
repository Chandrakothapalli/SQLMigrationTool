```# SQL Server Migration Tool

A Python-based desktop application that facilitates the migration of tables between SQL Server databases with a user-friendly graphical interface.

![SQL Migration Tool]

## Features

- 🔄 Migrate tables between SQL Server databases
- 🎯 Selective table migration with multi-select capability
- 📊 Preserves table schema and data types
- 🚀 Batch processing for efficient data transfer
- 📝 Real-time migration logging
- 🔒 Secure password input
- 🧵 Multi-threaded operation for responsive UI

## Prerequisites

- Python 3.6 or higher
- SQL Server installed on source and target machines
- SQL Server ODBC Driver

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Chandrakothapalli/SQLMigrationTool

```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

Create a `requirements.txt` file with the following packages:
```
pyodbc>=4.0.30
tkinter  # Usually comes with Python
```

## Usage

1. Run the application:
```bash
python sql_migration_tool.py
```

2. Enter connection details for both source and target databases:
   - Server name/IP
   - Database name
   - Username
   - Password

3. Click "Connect & Load Tables" to fetch available tables from the source database

4. Select the tables you want to migrate using the multi-select listbox

5. Click "Migrate Selected Tables" to start the migration process

6. Monitor the progress in the Migration Log section

## Features in Detail

### Connection Management
- Supports SQL Server authentication
- Separate connection settings for source and target databases
- Secure password input fields

### Table Selection
- Multi-select interface for table selection
- Scrollable table list
- Displays all user tables from the source database

### Migration Process
- Automatic schema creation in target database
- Preserves column data types and properties
- Batch processing for large datasets
- Transaction management for data integrity
- Real-time progress logging

### Error Handling
- Comprehensive error reporting
- Connection error management
- Data type compatibility checking
- Transaction rollback on failure

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python's tkinter library
- Uses Microsoft SQL Server ODBC Driver
- Inspired by the need for simple database migration tools

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Roadmap

- [ ] Add support for custom SQL queries
- [ ] Implement data transformation capabilities
- [ ] Add support for other database systems
- [ ] Include progress bars for large table migrations
- [ ] Add configuration file support```
