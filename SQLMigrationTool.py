import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pyodbc
from typing import List, Optional
import threading

class SQLMigrationTool:
    def _init_(self, root):
        self.root = root
        self.root.title("SQL Server Migration Tool")
        self.root.geometry("800x600")
        
        # Create main frames
        self.connection_frame = ttk.LabelFrame(root, text="Connection Settings", padding="10")
        self.connection_frame.pack(fill="x", padx=10, pady=5)
        
        self.tables_frame = ttk.LabelFrame(root, text="Table Selection", padding="10")
        self.tables_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_frame = ttk.LabelFrame(root, text="Migration Log", padding="10")
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self._create_connection_widgets()
        self._create_table_selection_widgets()
        self._create_log_widgets()

    def _create_connection_widgets(self):
        # Source connection settings
        ttk.Label(self.connection_frame, text="Source Server:").grid(row=0, column=0, sticky="w")
        self.source_server = ttk.Entry(self.connection_frame, width=40)
        self.source_server.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Source Database:").grid(row=1, column=0, sticky="w")
        self.source_db = ttk.Entry(self.connection_frame, width=40)
        self.source_db.grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Source Username:").grid(row=2, column=0, sticky="w")
        self.source_user = ttk.Entry(self.connection_frame, width=40)
        self.source_user.grid(row=2, column=1, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Source Password:").grid(row=3, column=0, sticky="w")
        self.source_pass = ttk.Entry(self.connection_frame, width=40, show="*")
        self.source_pass.grid(row=3, column=1, padx=5, pady=2)
        
        # Target connection settings
        ttk.Label(self.connection_frame, text="Target Server:").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.target_server = ttk.Entry(self.connection_frame, width=40)
        self.target_server.grid(row=0, column=3, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Target Database:").grid(row=1, column=2, sticky="w", padx=(20,0))
        self.target_db = ttk.Entry(self.connection_frame, width=40)
        self.target_db.grid(row=1, column=3, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Target Username:").grid(row=2, column=2, sticky="w", padx=(20,0))
        self.target_user = ttk.Entry(self.connection_frame, width=40)
        self.target_user.grid(row=2, column=3, padx=5, pady=2)
        
        ttk.Label(self.connection_frame, text="Target Password:").grid(row=3, column=2, sticky="w", padx=(20,0))
        self.target_pass = ttk.Entry(self.connection_frame, width=40, show="*")
        self.target_pass.grid(row=3, column=3, padx=5, pady=2)
        
        # Connect button
        self.connect_btn = ttk.Button(self.connection_frame, text="Connect & Load Tables", command=self.load_tables)
        self.connect_btn.grid(row=4, column=0, columnspan=4, pady=10)

    def _create_table_selection_widgets(self):
        # Create table selection listbox with scrollbar
        self.tables_listbox = tk.Listbox(self.tables_frame, selectmode=tk.MULTIPLE, width=70, height=10)
        scrollbar = ttk.Scrollbar(self.tables_frame, orient="vertical", command=self.tables_listbox.yview)
        self.tables_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.tables_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Migration button
        self.migrate_btn = ttk.Button(self.tables_frame, text="Migrate Selected Tables", command=self.migrate_tables)
        self.migrate_btn.pack(pady=10)

    def _create_log_widgets(self):
        # Create log text widget with scrollbar
        self.log_text = scrolledtext.ScrolledText(self.log_frame, width=70, height=10)
        self.log_text.pack(fill="both", expand=True)

    def load_tables(self):
        try:
            # Clear existing items
            self.tables_listbox.delete(0, tk.END)
            
            # Connect to source database
            conn_str = f'DRIVER={{SQL Server}};SERVER={self.source_server.get()};DATABASE={self.source_db.get()};UID={self.source_user.get()};PWD={self.source_pass.get()}'
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Get all user tables
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE' 
                AND TABLE_SCHEMA = 'dbo'
                ORDER BY TABLE_NAME
            """)
            
            # Add tables to listbox
            for table in cursor.fetchall():
                self.tables_listbox.insert(tk.END, table[0])
            
            conn.close()
            self.log_text.insert(tk.END, "Tables loaded successfully!\n")
            self.log_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading tables: {str(e)}")
            self.log_text.insert(tk.END, f"Error loading tables: {str(e)}\n")
            self.log_text.see(tk.END)

    def migrate_tables(self):
        selected_indices = self.tables_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one table to migrate.")
            return
        
        selected_tables = [self.tables_listbox.get(idx) for idx in selected_indices]
        
        # Start migration in a separate thread to keep UI responsive
        thread = threading.Thread(target=self._migrate_tables_thread, args=(selected_tables,))
        thread.daemon = True
        thread.start()

    def _migrate_tables_thread(self, selected_tables: List[str]):
        for table_name in selected_tables:
            try:
                # Connect to source database
                source_conn_str = f'DRIVER={{SQL Server}};SERVER={self.source_server.get()};DATABASE={self.source_db.get()};UID={self.source_user.get()};PWD={self.source_pass.get()}'
                source_conn = pyodbc.connect(source_conn_str)
                source_cursor = source_conn.cursor()
                
                # Connect to target database
                target_conn_str = f'DRIVER={{SQL Server}};SERVER={self.target_server.get()};DATABASE={self.target_db.get()};UID={self.target_user.get()};PWD={self.target_pass.get()}'
                target_conn = pyodbc.connect(target_conn_str)
                target_cursor = target_conn.cursor()
                
                # Get table schema
                source_cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, 
                           NUMERIC_PRECISION, NUMERIC_SCALE
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = '{table_name}'
                    ORDER BY ORDINAL_POSITION
                """)
                
                columns = source_cursor.fetchall()
                
                # Create table in target
                create_table_sql = f"CREATE TABLE {table_name} (\n"
                for i, col in enumerate(columns):
                    col_name, data_type, char_max_len, num_precision, num_scale = col
                    
                    if data_type in ('varchar', 'nvarchar', 'char', 'nchar'):
                        if char_max_len == -1:
                            data_type = f"{data_type}(MAX)"
                        else:
                            data_type = f"{data_type}({char_max_len})"
                    elif data_type in ('decimal', 'numeric'):
                        data_type = f"{data_type}({num_precision},{num_scale})"
                    
                    create_table_sql += f"{col_name} {data_type}"
                    if i < len(columns) - 1:
                        create_table_sql += ",\n"
                
                create_table_sql += "\n)"
                
                target_cursor.execute(create_table_sql)
                target_conn.commit()
                
                # Copy data
                source_cursor.execute(f"SELECT * FROM {table_name}")
                rows = source_cursor.fetchall()
                
                if rows:
                    # Prepare insert statement
                    placeholders = ','.join(['?' for _ in columns])
                    insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                    
                    # Insert data in batches
                    batch_size = 1000
                    for i in range(0, len(rows), batch_size):
                        batch = rows[i:i + batch_size]
                        target_cursor.executemany(insert_sql, batch)
                        target_conn.commit()
                
                self.log_text.insert(tk.END, f"Successfully migrated table: {table_name}\n")
                self.log_text.see(tk.END)
                
                # Close connections
                source_conn.close()
                target_conn.close()
                
            except Exception as e:
                self.log_text.insert(tk.END, f"Error migrating table {table_name}: {str(e)}\n")
                self.log_text.see(tk.END)
                # Make sure connections are closed even if an error occurs
                try:
                    if 'source_conn' in locals():
                        source_conn.close()
                    if 'target_conn' in locals():
                        target_conn.close()
                except:
                    pass
                continue

if _name_ == "_main_":
    root = tk.Tk()
    app = SQLMigrationTool(root)
    root.mainloop()