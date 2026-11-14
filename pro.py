import datetime
import json       
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from abc import ABC, abstractmethod
import threading

# ==============================================
# Base Classes with Encapsulation
# ==============================================

class Part:
    def __init__(self, part_id, name, price, quantity, category):
        self._part_id = part_id
        self._name = name
        self._price = price
        self._quantity = quantity
        self._category = category
    
    # Getters
    @property
    def part_id(self):
        return self._part_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def quantity(self):
        return self._quantity
    
    @property
    def category(self):
        return self._category
    
    # Setters (with validation)
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    
    @quantity.setter
    def quantity(self, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value
    
    @category.setter
    def category(self, value):
        if not value or not value.strip():
            raise ValueError("Category cannot be empty")
        self._category = value.strip()
    
    def to_dict(self):
        """Convert part to dictionary for serialization"""
        return {
            'part_id': self._part_id,
            'name': self._name,
            'price': self._price,
            'quantity': self._quantity,
            'category': self._category
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create part from dictionary"""
        return cls(
            data['part_id'],
            data['name'],
            data['price'],
            data['quantity'],
            data['category']
        )

class Customer:
    def __init__(self, customer_id, name, phone, email=""):
        self._customer_id = customer_id
        self._name = name
        self._phone = phone
        self._email = email
        self._purchases = []
    
    # Getters
    @property
    def customer_id(self):
        return self._customer_id
    
    @property
    def name(self):
        return self._name
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def email(self):
        return self._email
    
    @property
    def purchases(self):
        return self._purchases.copy()
    
    # Setters
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @phone.setter
    def phone(self, value):
        if not value or not value.strip():
            raise ValueError("Phone cannot be empty")
        self._phone = value.strip()
    
    @email.setter
    def email(self, value):
        self._email = value.strip()
    
    def add_purchase(self, purchase_data):
        """Add a purchase to customer history"""
        self._purchases.append(purchase_data)
    
    def get_purchase_history(self):
        """Get customer's purchase history"""
        return self._purchases.copy()
    
    def to_dict(self):
        """Convert customer to dictionary"""
        return {
            'customer_id': self._customer_id,
            'name': self._name,
            'phone': self._phone,
            'email': self._email,
            'purchases': self._purchases
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create customer from dictionary"""
        customer = cls(
            data['customer_id'],
            data['name'],
            data['phone'],
            data.get('email', '')
        )
        customer._purchases = data.get('purchases', [])
        return customer

# ==============================================
# User Management Classes
# ==============================================

class User(ABC):
    def __init__(self, username, password, role):
        self._username = username
        self._password = password
        self._role = role
    
    @property
    def username(self):
        return self._username
    
    @property
    def role(self):
        return self._role
    
    def verify_password(self, password):
        return self._password == password
    
    @abstractmethod
    def get_permissions(self):
        pass
    
    def to_dict(self):
        return {
            'username': self._username,
            'password': self._password,
            'role': self._role
        }

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, "admin")
    
    def get_permissions(self):
        return {
            'manage_parts': True,
            'manage_customers': True,
            'manage_sales': True,
            'manage_users': True,
            'view_reports': True,
            'process_sales': True
        }

class Staff(User):
    def __init__(self, username, password):
        super().__init__(username, password, "staff")
    
    def get_permissions(self):
        return {
            'manage_parts': False,
            'manage_customers': True,
            'manage_sales': True,
            'manage_users': False,
            'view_reports': True,
            'process_sales': True
        }

# ==============================================
# Store Management Class
# ==============================================

class AutoPartsStore:
    def __init__(self):
        self._parts = []
        self._customers = []
        self._sales_history = []
        self._users = []
        self._current_user = None
        self._initialize_default_users()
        self._load_sample_data()
    
    def _initialize_default_users(self):
        """Initialize default admin user"""
        default_admin = Admin("admin", "admin123")
        default_staff = Staff("staff", "staff123")
        self._users = [default_admin, default_staff]
    
    def _load_sample_data(self):
        """Load sample data for testing"""
        # Sample parts
        sample_parts = [
            Part("P001", "Engine Piston", 850, 25, "Engine"),
            Part("P002", "Oil Filter", 120, 100, "Filters"),
            Part("P003", "Car Battery", 1800, 15, "Electrical"),
            Part("P004", "Brake Cylinder", 320, 40, "Brakes"),
            Part("P005", "15-inch Tire", 650, 30, "Tires"),
            Part("P006", "Spark Plug", 45, 200, "Engine"),
            Part("P007", "Headlight", 350, 50, "Electrical"),
            Part("P008", "Steering Wheel", 450, 20, "Interior"),
        ]
        self._parts = sample_parts
        
        # Sample customers
        sample_customers = [
            Customer("C001", "mahmoud saleh", "01001234567", "mahmoud@example.com"),
            Customer("C002", "mazen EL SAWY", "01009876543", "mazen@example.com"),
            Customer("C003", "MOHAMED SAMEH", "01005556677", "mohamed@example.com"),
        ]
        self._customers = sample_customers
    
    # Authentication Methods
    def login(self, username, password):
        """Login user"""
        for user in self._users:
            if user.username == username and user.verify_password(password):
                self._current_user = user
                return True, user.role
        return False, None
    
    def logout(self):
        """Logout current user"""
        self._current_user = None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self._current_user
    
    def check_permission(self, permission):
        """Check if current user has specific permission"""
        if not self._current_user:
            return False
        permissions = self._current_user.get_permissions()
        return permissions.get(permission, False)
    
    # Getter methods for GUI
    def get_all_parts(self):
        return self._parts.copy()
    
    def get_all_customers(self):
        return self._customers.copy()
    
    def get_all_sales(self):
        return self._sales_history.copy()
    
    def get_all_users(self):
        return self._users.copy()
    
    def get_part_by_id(self, part_id):
        for part in self._parts:
            if part.part_id == part_id:
                return part
        return None
    
    def get_customer_by_id(self, customer_id):
        for customer in self._customers:
            if customer.customer_id == customer_id:
                return customer
        return None
    
    # Data manipulation methods
    def add_part(self, part_data):
        """Add new part"""
        try:
            part = Part(**part_data)
            self._parts.append(part)
            return True, "Part added successfully!"
        except ValueError as e:
            return False, str(e)
    
    def update_part(self, part_id, update_data):
        """Update existing part"""
        part = self.get_part_by_id(part_id)
        if not part:
            return False, "Part not found!"
        
        try:
            for key, value in update_data.items():
                if hasattr(part, key):
                    setattr(part, key, value)
            return True, "Part updated successfully!"
        except ValueError as e:
            return False, str(e)
    
    def add_customer(self, customer_data):
        """Add new customer"""
        try:
            customer = Customer(**customer_data)
            self._customers.append(customer)
            return True, "Customer added successfully!"
        except ValueError as e:
            return False, str(e)
    
    def update_customer(self, customer_id, update_data):
        """Update existing customer"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False, "Customer not found!"
        
        try:
            for key, value in update_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            return True, "Customer updated successfully!"
        except ValueError as e:
            return False, str(e)
    
    def process_sale(self, sale_data):
        """Process a new sale"""
        if not self.check_permission('process_sales'):
            return False, "Permission denied!"
        
        customer = self.get_customer_by_id(sale_data['customer_id'])
        if not customer:
            return False, "Customer not found!"
        
        sale_items = sale_data['items']
        total_amount = 0
        
        # Check stock and update inventory
        for item in sale_items:
            part = self.get_part_by_id(item['part_id'])
            if not part:
                return False, f"Part {item['part_id']} not found!"
            
            if part.quantity < item['quantity']:
                return False, f"Insufficient stock for {part.name}. Available: {part.quantity}"
            
            part.quantity -= item['quantity']
            total_amount += item['total']
        
        # Record sale
        sale_record = {
            'sale_id': f"S{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'customer_id': customer.customer_id,
            'customer_name': customer.name,
            'items': sale_items,
            'total_amount': total_amount,
            'processed_by': self._current_user.username if self._current_user else "Unknown"
        }
        self._sales_history.append(sale_record)
        
        # Add to customer purchases
        for item in sale_items:
            customer.add_purchase({
                'date': datetime.datetime.now().strftime('%Y-%m-%d'),
                'item': item['name'],
                'quantity': item['quantity'],
                'total': item['total']
            })
        
        return True, f"Sale completed successfully! Total: ${total_amount:.2f}"
    
    # Data persistence
    def save_data(self):
        """Save data to files"""
        try:
            # Save parts
            parts_data = [part.to_dict() for part in self._parts]
            with open('parts.json', 'w') as f:
                json.dump(parts_data, f, indent=2)
            
            # Save customers
            customers_data = [customer.to_dict() for customer in self._customers]
            with open('customers.json', 'w') as f:
                json.dump(customers_data, f, indent=2)
            
            # Save users
            users_data = [user.to_dict() for user in self._users]
            with open('users.json', 'w') as f:
                json.dump(users_data, f, indent=2)
            
            # Save sales
            with open('sales.json', 'w') as f:
                json.dump(self._sales_history, f, indent=2)
            
            return True, "All data saved successfully!"
            
        except Exception as e:
            return False, f"Error saving data: {e}"
    
    def load_data(self):
        """Load data from files"""
        try:
            # Load parts
            try:
                with open('parts.json', 'r') as f:
                    parts_data = json.load(f)
                self._parts = [Part.from_dict(data) for data in parts_data]
            except FileNotFoundError:
                pass
            
            # Load customers
            try:
                with open('customers.json', 'r') as f:
                    customers_data = json.load(f)
                self._customers = [Customer.from_dict(data) for data in customers_data]
            except FileNotFoundError:
                pass
            
            # Load users
            try:
                with open('users.json', 'r') as f:
                    users_data = json.load(f)
                self._users = []
                for data in users_data:
                    if data['role'] == 'admin':
                        user = Admin(data['username'], data['password'])
                    else:
                        user = Staff(data['username'], data['password'])
                    self._users.append(user)
            except FileNotFoundError:
                pass
            
            # Load sales
            try:
                with open('sales.json', 'r') as f:
                    self._sales_history = json.load(f)
            except FileNotFoundError:
                pass
            
            return True, "Data loaded successfully!"
            
        except Exception as e:
            return False, f"Error loading data: {e}"

# ==============================================
# GUI Application
# ==============================================

class AutoPartsStoreGUI:
    def __init__(self):
        self.store = AutoPartsStore()
        self.root = tk.Tk()
        self.root.title("🚗 el3anqody Auto Parts Store")
        self.root.geometry("1200x700")
        
        # Style configuration
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Current user info
        self.current_user_label = ttk.Label(self.main_container, text="Not logged in", font=('Arial', 10, 'italic'))
        self.current_user_label.pack(anchor=tk.NE)
        
        # Show login screen initially
        self.show_login_screen()
        
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        
        # Button styles
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'), padding=5)
        style.configure('Secondary.TButton', font=('Arial', 9), padding=3)
        
        # Treeview styles
        style.configure('Treeview', font=('Arial', 9))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def clear_screen(self):
        """Clear all widgets from main container"""
        for widget in self.main_container.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        """Display login screen"""
        self.clear_screen()
        
        # Title
        title_label = ttk.Label(self.main_container, text="🚗 AUTO PARTS STORE MANAGEMENT", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Login frame
        login_frame = ttk.Frame(self.main_container)
        login_frame.pack(pady=50)
        
        # Username
        ttk.Label(login_frame, text="Username:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.username_entry = ttk.Entry(login_frame, width=30, font=('Arial', 11))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.username_entry.focus()
        
        # Password
        ttk.Label(login_frame, text="Password:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.password_entry = ttk.Entry(login_frame, width=30, show="*", font=('Arial', 11))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", command=self.handle_login, style='Primary.TButton')
        login_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.handle_login())
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        success, role = self.store.login(username, password)
        if success:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.current_user_label.config(text=f"User: {username} ({role})")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
    
    def show_main_menu(self):
        """Display main menu based on user role"""
        self.clear_screen()
        
        user = self.store.get_current_user()
        if not user:
            self.show_login_screen()
            return
        
        # Title
        title_label = ttk.Label(self.main_container, text=f"🏠 Main Menu - {user.role.upper()} Panel", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Button frame
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(pady=20)
        
        # Common buttons for all users
        buttons = [
            ("📦 View Parts", self.show_parts_screen),
            ("👥 View Customers", self.show_customers_screen),
            ("💰 New Sale", self.show_new_sale_screen),
            ("📊 View Sales", self.show_sales_screen),
            ("📈 Inventory Report", self.show_inventory_report),
            ("🔍 Search Parts", self.show_search_screen),
        ]
        
        # Add admin-only buttons
        if user.role == "admin":
            buttons.extend([
                ("➕ Add Part", self.show_add_part_screen),
                ("✏️ Edit Part", self.show_edit_part_screen),
                ("➕ Add Customer", self.show_add_customer_screen),
                ("✏️ Edit Customer", self.show_edit_customer_screen),
                ("👤 Manage Users", self.show_user_management_screen),
            ])
        
        buttons.append(("💾 Save Data", self.save_data))
        buttons.append(("📂 Load Data", self.load_data))
        buttons.append(("🚪 Logout", self.logout))
        
        # Create buttons in grid
        row, col = 0, 0
        for text, command in buttons:
            btn = ttk.Button(button_frame, text=text, command=command, width=20, style='Primary.TButton')
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def show_parts_screen(self):
        """Display all parts"""
        self.clear_screen()
        
        # Title
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, pady=10)
        ttk.Label(title_frame, text="📦 Inventory Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        ttk.Button(title_frame, text="← Back", command=self.show_main_menu, style='Secondary.TButton').pack(side=tk.RIGHT)
        
        # Create treeview for parts
        tree_frame = ttk.Frame(self.main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Create treeview
        self.parts_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Price", "Quantity", "Category", "Status"), 
                                      yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.parts_tree.yview)
        hsb.config(command=self.parts_tree.xview)
        
        # Define columns
        self.parts_tree.heading("#0", text="")
        self.parts_tree.heading("ID", text="Part ID")
        self.parts_tree.heading("Name", text="Part Name")
        self.parts_tree.heading("Price", text="Price ($)")
        self.parts_tree.heading("Quantity", text="Quantity")
        self.parts_tree.heading("Category", text="Category")
        self.parts_tree.heading("Status", text="Status")
        
        self.parts_tree.column("#0", width=0, stretch=tk.NO)
        self.parts_tree.column("ID", width=100, anchor=tk.W)
        self.parts_tree.column("Name", width=200, anchor=tk.W)
        self.parts_tree.column("Price", width=100, anchor=tk.E)
        self.parts_tree.column("Quantity", width=80, anchor=tk.E)
        self.parts_tree.column("Category", width=120, anchor=tk.W)
        self.parts_tree.column("Status", width=100, anchor=tk.W)
        
        # Add to frame
        self.parts_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load data
        self.load_parts_data()
        
        # Statistics frame
        stats_frame = ttk.Frame(self.main_container)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        parts = self.store.get_all_parts()
        total_parts = len(parts)
        total_value = sum(p.price * p.quantity for p in parts)
        low_stock = len([p for p in parts if p.quantity <= 5])
        
        ttk.Label(stats_frame, text=f"Total Parts: {total_parts}").pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text=f"Total Value: ${total_value:,.2f}").pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text=f"Low Stock Items: {low_stock}", foreground='red' if low_stock > 0 else 'black').pack(side=tk.LEFT, padx=20)
    
    def load_parts_data(self):
        """Load parts data into treeview"""
        # Clear existing items
        for item in self.parts_tree.get_children():
            self.parts_tree.delete(item)
        
        # Add parts
        parts = self.store.get_all_parts()
        for part in parts:
            status = "✅ In Stock" if part.quantity > 0 else "❌ Out of Stock"
            self.parts_tree.insert("", tk.END, values=(
                part.part_id,
                part.name,
                f"${part.price:,.2f}",
                part.quantity,
                part.category,
                status
            ))
    
    def show_customers_screen(self):
        """Display all customers"""
        self.clear_screen()
        
        # Title
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, pady=10)
        ttk.Label(title_frame, text="👥 Customer Management", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        ttk.Button(title_frame, text="← Back", command=self.show_main_menu, style='Secondary.TButton').pack(side=tk.RIGHT)
        
        # Create treeview for customers
        tree_frame = ttk.Frame(self.main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        self.customers_tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Phone", "Email", "Purchases"), 
                                          yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.customers_tree.yview)
        hsb.config(command=self.customers_tree.xview)
        
        # Define columns
        self.customers_tree.heading("#0", text="")
        self.customers_tree.heading("ID", text="Customer ID")
        self.customers_tree.heading("Name", text="Name")
        self.customers_tree.heading("Phone", text="Phone")
        self.customers_tree.heading("Email", text="Email")
        self.customers_tree.heading("Purchases", text="Total Purchases")
        
        self.customers_tree.column("#0", width=0, stretch=tk.NO)
        self.customers_tree.column("ID", width=100, anchor=tk.W)
        self.customers_tree.column("Name", width=150, anchor=tk.W)
        self.customers_tree.column("Phone", width=120, anchor=tk.W)
        self.customers_tree.column("Email", width=200, anchor=tk.W)
        self.customers_tree.column("Purchases", width=120, anchor=tk.E)
        
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load data
        customers = self.store.get_all_customers()
        for customer in customers:
            total_purchases = len(customer.purchases)
            self.customers_tree.insert("", tk.END, values=(
                customer.customer_id,
                customer.name,
                customer.phone,
                customer.email,
                total_purchases
            ))
    
    def show_new_sale_screen(self):
        """Display new sale screen"""
        self.clear_screen()
        
        # Title
        title_frame = ttk.Frame(self.main_container)
        title_frame.pack(fill=tk.X, pady=10)
        ttk.Label(title_frame, text="💰 Process New Sale", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Back button
        ttk.Button(title_frame, text="← Back", command=self.show_main_menu, style='Secondary.TButton').pack(side=tk.RIGHT)
        
        # Main content frame
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame - Customer selection
        left_frame = ttk.LabelFrame(content_frame, text="Customer Information", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        ttk.Label(left_frame, text="Customer ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sale_customer_id = ttk.Entry(left_frame, width=20)
        self.sale_customer_id.grid(row=0, column=1, pady=5)
        
        ttk.Button(left_frame, text="Find Customer", command=self.find_customer_for_sale, style='Secondary.TButton').grid(row=1, column=0, columnspan=2, pady=5)
        
        self.customer_info_label = ttk.Label(left_frame, text="No customer selected", font=('Arial', 10, 'italic'))
        self.customer_info_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Right frame - Parts selection
        right_frame = ttk.LabelFrame(content_frame, text="Add Items", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Part selection
        ttk.Label(right_frame, text="Part ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sale_part_id = ttk.Entry(right_frame, width=20)
        self.sale_part_id.grid(row=0, column=1, pady=5)
        
        ttk.Label(right_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sale_quantity = ttk.Spinbox(right_frame, from_=1, to=1000, width=18)
        self.sale_quantity.grid(row=1, column=1, pady=5)
        self.sale_quantity.set(1)
        
        ttk.Button(right_frame, text="Find Part", command=self.find_part_for_sale, style='Secondary.TButton').grid(row=2, column=0, columnspan=2, pady=5)
        
        self.part_info_label = ttk.Label(right_frame, text="No part selected", font=('Arial', 10, 'italic'))
        self.part_info_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(right_frame, text="Add to Cart", command=self.add_to_cart, style='Primary.TButton').grid(row=4, column=0, columnspan=2, pady=10)
        
        # Cart frame
        cart_frame = ttk.LabelFrame(content_frame, text="Shopping Cart", padding=10)
        cart_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Cart treeview
        self.cart_tree = ttk.Treeview(cart_frame, columns=("Part", "Quantity", "Price", "Total"), height=8)
        self.cart_tree.heading("#0", text="")
        self.cart_tree.heading("Part", text="Part Name")
        self.cart_tree.heading("Quantity", text="Qty")
        self.cart_tree.heading("Price", text="Price ($)")
        self.cart_tree.heading("Total", text="Total ($)")
        
        self.cart_tree.column("#0", width=0, stretch=tk.NO)
        self.cart_tree.column("Part", width=200)
        self.cart_tree.column("Quantity", width=80, anchor=tk.E)
        self.cart_tree.column("Price", width=100, anchor=tk.E)
        self.cart_tree.column("Total", width=100, anchor=tk.E)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Cart buttons
        cart_buttons_frame = ttk.Frame(cart_frame)
        cart_buttons_frame.pack(pady=10)
        
        ttk.Button(cart_buttons_frame, text="Remove Selected", command=self.remove_from_cart, style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(cart_buttons_frame, text="Clear Cart", command=self.clear_cart, style='Secondary.TButton').pack(side=tk.LEFT, padx=5)
        
        # Total and process button
        bottom_frame = ttk.Frame(content_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        self.total_label = ttk.Label(bottom_frame, text="Total: $0.00", font=('Arial', 12, 'bold'))
        self.total_label.pack(side=tk.LEFT)
        
        ttk.Button(bottom_frame, text="Process Sale", command=self.process_sale, style='Primary.TButton').pack(side=tk.RIGHT)
        
        # Initialize cart
        self.cart_items = []
        self.current_customer = None
        self.current_part = None
    
    def find_customer_for_sale(self):
        """Find customer by ID for sale"""
        customer_id = self.sale_customer_id.get().strip()
        if not customer_id:
            messagebox.showwarning("Warning", "Please enter a customer ID!")
            return
        
        customer = self.store.get_customer_by_id(customer_id)
        if customer:
            self.current_customer = customer
            self.customer_info_label.config(text=f"Customer: {customer.name}\nPhone: {customer.phone}")
        else:
            messagebox.showerror("Error", "Customer not found!")
    
    def find_part_for_sale(self):
        """Find part by ID for sale"""
        part_id = self.sale_part_id.get().strip()
        if not part_id:
            messagebox.showwarning("Warning", "Please enter a part ID!")
            return
        
        part = self.store.get_part_by_id(part_id)
        if part:
            self.current_part = part
            status = "In Stock" if part.quantity > 0 else "Out of Stock"
            self.part_info_label.config(text=f"Part: {part.name}\nPrice: ${part.price:.2f}\nAvailable: {part.quantity}\nStatus: {status}")
        else:
            messagebox.showerror("Error", "Part not found!")
    
    def add_to_cart(self):
        """Add current part to cart"""
        if not self.current_part:
            messagebox.showwarning("Warning", "Please select a part first!")
            return
        
        try:
            quantity = int(self.sale_quantity.get())
            if quantity <= 0:
                messagebox.showwarning("Warning", "Quantity must be positive!")
                return
            
            if quantity > self.current_part.quantity:
                messagebox.showwarning("Warning", f"Only {self.current_part.quantity} available in stock!")
                return
            
            # Add to cart
            item_total = self.current_part.price * quantity
            cart_item = {
                'part_id': self.current_part.part_id,
                'name': self.current_part.name,
                'price': self.current_part.price,
                'quantity': quantity,
                'total': item_total
            }
            
            self.cart_items.append(cart_item)
            
            # Add to treeview
            self.cart_tree.insert("", tk.END, values=(
                self.current_part.name,
                quantity,
                f"${self.current_part.price:.2f}",
                f"${item_total:.2f}"
            ))
            
            # Update total
            self.update_cart_total()
            
            # Reset part selection
            self.current_part = None
            self.sale_part_id.delete(0, tk.END)
            self.part_info_label.config(text="No part selected")
            self.sale_quantity.set(1)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")


