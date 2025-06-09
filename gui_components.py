"""
GUI Components for Fishtest Worker GUI
Contains modern UI components for login, status, controls, and settings.
"""

import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
import webbrowser

class LoginFrame(ttk.LabelFrame):
    """Login and configuration frame"""

    def __init__(self, parent, config, login_callback=None):
        super().__init__(parent, text="Fishtest Login", padding="10")
        self.config = config
        self.login_callback = login_callback
        self.is_logged_in = False
        self.create_widgets()
        
    def create_widgets(self):
        """Create login widgets"""
        # Username
        ttk.Label(self, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.username_var = tk.StringVar(value=self.config.get('username', ''))
        self.username_entry = ttk.Entry(self, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # Password
        ttk.Label(self, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.password_var = tk.StringVar(value=self.config.get('password', ''))
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)
        
        # CPU Cores
        ttk.Label(self, text="CPU Cores:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.cores_var = tk.StringVar(value=self.config.get('cores', '1'))

        cores_frame = ttk.Frame(self)
        cores_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 0), pady=2)

        self.cores_spinbox = ttk.Spinbox(
            cores_frame,
            from_=1,
            to=os.cpu_count() or 8,
            textvariable=self.cores_var,
            width=10
        )
        self.cores_spinbox.pack(side=tk.LEFT)

        max_cores = os.cpu_count() or 8
        ttk.Label(cores_frame, text=f"(1-{max_cores} available)").pack(side=tk.LEFT, padx=(5, 0))

        # Login button
        if self.login_callback:
            self.login_button = ttk.Button(self, text="Login to Fishtest", command=self.login_callback)
            self.login_button.grid(row=3, column=1, sticky=tk.W, padx=(5, 0), pady=(10, 0))

        # Configure grid weights
        self.columnconfigure(1, weight=1)
        
    def get_username(self):
        """Get username value"""
        return self.username_var.get().strip()
        
    def get_password(self):
        """Get password value"""
        return self.password_var.get()
        
    def get_cores(self):
        """Get cores value"""
        try:
            cores = int(self.cores_var.get())
            max_cores = os.cpu_count() or 8
            return max(1, min(cores, max_cores))
        except ValueError:
            return 1

    def set_logged_in(self, logged_in):
        """Update login button state"""
        self.is_logged_in = logged_in
        if hasattr(self, 'login_button'):
            if logged_in:
                self.login_button.config(text="✓ Logged In", state=tk.DISABLED)
            else:
                self.login_button.config(text="Login to Fishtest", state=tk.NORMAL)

    def set_worker_running(self, running):
        """Update UI when worker is running"""
        if hasattr(self, 'login_button'):
            if running:
                self.login_button.config(state=tk.DISABLED)
            else:
                # Only enable if not logged in
                if not self.is_logged_in:
                    self.login_button.config(state=tk.NORMAL)

class StatusFrame(ttk.LabelFrame):
    """Status and logging frame"""
    
    def __init__(self, parent):
        super().__init__(parent, text="Status", padding="10")
        self.create_widgets()
        
    def create_widgets(self):
        """Create status widgets"""
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var, font=('TkDefaultFont', 10, 'bold'))
        self.status_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Log display
        log_frame = ttk.Frame(self)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        self.log_text = tk.Text(log_frame, height=8, width=60, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Make text read-only
        self.log_text.config(state=tk.DISABLED)
        
        # Clear button
        ttk.Button(self, text="Clear Log", command=self.clear_log).pack(pady=(5, 0))
        
    def set_status(self, status):
        """Set status message"""
        self.status_var.set(status)
        
    def add_log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        self.log_text.config(state=tk.DISABLED)
        
    def clear_log(self):
        """Clear the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

class ControlFrame(ttk.LabelFrame):
    """Control buttons frame"""

    def __init__(self, parent, start_stop_callback):
        super().__init__(parent, text="Controls", padding="10")
        self.start_stop_callback = start_stop_callback
        self.is_running = False
        self.is_logged_in = False
        self.create_widgets()

    def create_widgets(self):
        """Create control widgets"""
        # Start/Stop button
        self.start_stop_button = ttk.Button(self, text="Start Worker", command=self.start_stop_callback, state=tk.DISABLED)
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 10))

        # Status indicator
        self.status_indicator = ttk.Label(self, text="●", foreground="red", font=('TkDefaultFont', 16))
        self.status_indicator.pack(side=tk.RIGHT, padx=(10, 0))

        ttk.Label(self, text="Status:").pack(side=tk.RIGHT)

    def set_logged_in(self, logged_in):
        """Update UI based on login state"""
        self.is_logged_in = logged_in
        if logged_in:
            self.start_stop_button.config(state=tk.NORMAL)
        else:
            self.start_stop_button.config(state=tk.DISABLED)

    def set_worker_running(self, running):
        """Update UI based on worker running state"""
        self.is_running = running
        if running:
            self.start_stop_button.config(text="Stop Worker")
            self.status_indicator.config(foreground="green")
        else:
            self.start_stop_button.config(text="Start Worker")
            self.status_indicator.config(foreground="red")


# Modern Enhanced Components

class ModernLoginFrame(ttk.LabelFrame):
    """Modern login and configuration frame with enhanced UX"""

    def __init__(self, parent, config, login_callback=None, theme=None):
        super().__init__(parent, text="🔐 Fishtest Login", padding="15", style='Card.TLabelframe')
        self.config = config
        self.login_callback = login_callback
        self.theme = theme
        self.is_logged_in = False
        self.create_widgets()

    def create_widgets(self):
        """Create modern login widgets"""
        # Username section
        username_frame = ttk.Frame(self, style='Card.TFrame')
        username_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(username_frame, text="Username:", style='Heading.TLabel').pack(anchor=tk.W)
        self.username_var = tk.StringVar(value=self.config.get('username', ''))
        self.username_entry = ttk.Entry(username_frame, textvariable=self.username_var,
                                       width=35, style='Modern.TEntry', font=('Segoe UI', 10))
        self.username_entry.pack(fill=tk.X, pady=(5, 0))

        # Password section
        password_frame = ttk.Frame(self, style='Card.TFrame')
        password_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(password_frame, text="Password:", style='Heading.TLabel').pack(anchor=tk.W)
        self.password_var = tk.StringVar(value=self.config.get('password', ''))
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var,
                                       show="*", width=35, style='Modern.TEntry', font=('Segoe UI', 10))
        self.password_entry.pack(fill=tk.X, pady=(5, 0))

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_cb = ttk.Checkbutton(password_frame, text="Show password",
                                          variable=self.show_password_var,
                                          command=self.toggle_password_visibility)
        show_password_cb.pack(anchor=tk.W, pady=(5, 0))

        # CPU Cores section
        cores_frame = ttk.Frame(self, style='Card.TFrame')
        cores_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        cores_label_frame = ttk.Frame(cores_frame)
        cores_label_frame.pack(fill=tk.X)

        ttk.Label(cores_label_frame, text="CPU Cores:", style='Heading.TLabel').pack(side=tk.LEFT)
        max_cores = os.cpu_count() or 8
        ttk.Label(cores_label_frame, text=f"(Max: {max_cores})",
                 style='Secondary.TLabel').pack(side=tk.RIGHT)

        self.cores_var = tk.StringVar(value=self.config.get('cores', '1'))
        cores_input_frame = ttk.Frame(cores_frame)
        cores_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.cores_spinbox = ttk.Spinbox(
            cores_input_frame,
            from_=1,
            to=max_cores,
            textvariable=self.cores_var,
            width=10,
            font=('Segoe UI', 10)
        )
        self.cores_spinbox.pack(side=tk.LEFT)

        # Auto-detect button
        auto_cores_btn = ttk.Button(cores_input_frame, text="Auto",
                                   command=self.auto_detect_cores)
        auto_cores_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Login button section
        if self.login_callback:
            button_frame = ttk.Frame(self, style='Card.TFrame')
            button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))

            self.login_button = ttk.Button(button_frame, text="🔑 Login to Fishtest",
                                          command=self.login_callback, style='Primary.TButton')
            self.login_button.pack(side=tk.LEFT)

            # Test connection button
            self.test_button = ttk.Button(button_frame, text="🔗 Test Connection",
                                         command=self.test_connection)
            self.test_button.pack(side=tk.LEFT, padx=(10, 0))

        # Configure grid weights
        self.columnconfigure(0, weight=1)

        # Add tooltips
        if hasattr(self.theme, 'create_tooltip'):
            self.theme.create_tooltip(self.username_entry, "Enter your Fishtest username")
            self.theme.create_tooltip(self.password_entry, "Enter your Fishtest password")
            self.theme.create_tooltip(self.cores_spinbox, "Number of CPU cores to use for testing")

    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def auto_detect_cores(self):
        """Auto-detect optimal number of cores"""
        max_cores = os.cpu_count() or 8
        # Use all cores minus 1 for better system responsiveness
        optimal_cores = max(1, max_cores - 1)
        self.cores_var.set(str(optimal_cores))

    def test_connection(self):
        """Test connection to Fishtest server"""
        # This would be implemented to test connection without full login
        pass

    def get_username(self):
        """Get username value"""
        return self.username_var.get().strip()

    def get_password(self):
        """Get password value"""
        return self.password_var.get()

    def get_cores(self):
        """Get cores value"""
        try:
            cores = int(self.cores_var.get())
            max_cores = os.cpu_count() or 8
            return max(1, min(cores, max_cores))
        except ValueError:
            return 1

    def set_logged_in(self, logged_in):
        """Update login button state"""
        self.is_logged_in = logged_in
        if hasattr(self, 'login_button'):
            if logged_in:
                self.login_button.config(text="✅ Logged In", state=tk.DISABLED, style='Success.TButton')
            else:
                self.login_button.config(text="🔑 Login to Fishtest", state=tk.NORMAL, style='Primary.TButton')

    def set_worker_running(self, running):
        """Update UI when worker is running"""
        if hasattr(self, 'login_button'):
            if running:
                self.login_button.config(state=tk.DISABLED)
                if hasattr(self, 'test_button'):
                    self.test_button.config(state=tk.DISABLED)
            else:
                # Only enable if not logged in
                if not self.is_logged_in:
                    self.login_button.config(state=tk.NORMAL)
                if hasattr(self, 'test_button'):
                    self.test_button.config(state=tk.NORMAL)


class ModernStatusFrame(ttk.LabelFrame):
    """Modern status and logging frame with enhanced display"""

    def __init__(self, parent, theme=None):
        super().__init__(parent, text="📊 Status & Logs", padding="15", style='Card.TLabelframe')
        self.theme = theme
        self.create_widgets()

    def create_widgets(self):
        """Create modern status widgets"""
        # Status section
        status_header = ttk.Frame(self, style='Card.TFrame')
        status_header.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(status_header, text="Current Status:", style='Heading.TLabel').pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(status_header, textvariable=self.status_var,
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)

        # Statistics section
        stats_frame = ttk.Frame(self, style='Accent.TFrame', padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 10))

        # Create statistics display
        self.stats_vars = {
            'tests_completed': tk.StringVar(value="0"),
            'uptime': tk.StringVar(value="00:00:00"),
            'games_played': tk.StringVar(value="0")
        }

        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill=tk.X)

        # Tests completed
        ttk.Label(stats_grid, text="Tests Completed:", style='Secondary.TLabel').grid(row=0, column=0, sticky=tk.W)
        ttk.Label(stats_grid, textvariable=self.stats_vars['tests_completed'],
                 style='Heading.TLabel').grid(row=0, column=1, sticky=tk.E)

        # Uptime
        ttk.Label(stats_grid, text="Uptime:", style='Secondary.TLabel').grid(row=1, column=0, sticky=tk.W)
        ttk.Label(stats_grid, textvariable=self.stats_vars['uptime'],
                 style='Heading.TLabel').grid(row=1, column=1, sticky=tk.E)

        # Games played
        ttk.Label(stats_grid, text="Games Played:", style='Secondary.TLabel').grid(row=2, column=0, sticky=tk.W)
        ttk.Label(stats_grid, textvariable=self.stats_vars['games_played'],
                 style='Heading.TLabel').grid(row=2, column=1, sticky=tk.E)

        stats_grid.columnconfigure(1, weight=1)

        # Log section
        log_header = ttk.Frame(self, style='Card.TFrame')
        log_header.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(log_header, text="Activity Log:", style='Heading.TLabel').pack(side=tk.LEFT)

        # Log controls
        log_controls = ttk.Frame(log_header)
        log_controls.pack(side=tk.RIGHT)

        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(log_controls, text="Auto-scroll",
                       variable=self.auto_scroll_var).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(log_controls, text="Clear", command=self.clear_log).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(log_controls, text="Save", command=self.save_log).pack(side=tk.LEFT, padx=(5, 0))

        # Log display with enhanced styling
        log_frame = ttk.Frame(self, style='Card.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)

        # Create text widget with scrollbar
        self.log_text = tk.Text(log_frame, height=10, width=70, wrap=tk.WORD,
                               bg='#f8f9fa', fg='#212529',
                               font=('Consolas', 9), relief='flat',
                               selectbackground='#0d6efd', selectforeground='white')

        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure text tags for different message types
        self.log_text.tag_configure('info', foreground='#0d6efd')
        self.log_text.tag_configure('success', foreground='#198754')
        self.log_text.tag_configure('warning', foreground='#fd7e14')
        self.log_text.tag_configure('error', foreground='#dc3545')
        self.log_text.tag_configure('timestamp', foreground='#6c757d', font=('Consolas', 8))

        # Make text read-only
        self.log_text.config(state=tk.DISABLED)

    def set_status(self, status):
        """Set status message with color coding"""
        self.status_var.set(status)

        # Update status label color based on content
        if hasattr(self, 'status_label'):
            if 'error' in status.lower() or 'failed' in status.lower():
                self.status_label.config(foreground='#dc3545')
            elif 'success' in status.lower() or 'running' in status.lower():
                self.status_label.config(foreground='#198754')
            elif 'warning' in status.lower():
                self.status_label.config(foreground='#fd7e14')
            else:
                self.status_label.config(foreground='#0d6efd')

    def add_log_message(self, message, msg_type='info'):
        """Add message to log with type-based formatting"""
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.log_text.config(state=tk.NORMAL)

        # Insert timestamp
        self.log_text.insert(tk.END, f"[{timestamp}] ", 'timestamp')

        # Insert message with appropriate tag
        self.log_text.insert(tk.END, f"{message}\n", msg_type)

        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.log_text.see(tk.END)

        self.log_text.config(state=tk.DISABLED)

    def update_stats(self, stats_dict):
        """Update statistics display"""
        for key, value in stats_dict.items():
            if key in self.stats_vars:
                self.stats_vars[key].set(str(value))

    def clear_log(self):
        """Clear the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

    def save_log(self):
        """Save log to file"""
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Log File"
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                self.add_log_message(f"Log saved to {filename}", 'success')
            except Exception as e:
                self.add_log_message(f"Failed to save log: {e}", 'error')


class ModernControlFrame(ttk.LabelFrame):
    """Modern control buttons frame with enhanced functionality"""

    def __init__(self, parent, start_stop_callback, theme=None):
        super().__init__(parent, text="⚙️ Worker Controls", padding="15", style='Card.TLabelframe')
        self.start_stop_callback = start_stop_callback
        self.theme = theme
        self.is_running = False
        self.is_logged_in = False
        self.create_widgets()

    def create_widgets(self):
        """Create modern control widgets"""
        # Main control section
        control_section = ttk.Frame(self, style='Card.TFrame')
        control_section.pack(fill=tk.X, pady=(0, 10))

        # Start/Stop button with enhanced styling
        self.start_stop_button = ttk.Button(
            control_section,
            text="▶️ Start Worker",
            command=self.start_stop_callback,
            state=tk.DISABLED,
            style='Primary.TButton'
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 15))

        # Status indicator section
        status_section = ttk.Frame(control_section, style='Accent.TFrame', padding="10")
        status_section.pack(side=tk.RIGHT)

        ttk.Label(status_section, text="Worker Status:", style='Secondary.TLabel').pack(side=tk.LEFT, padx=(0, 5))

        self.status_indicator = ttk.Label(status_section, text="⭕", font=('Segoe UI', 16))
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 5))

        self.status_text = ttk.Label(status_section, text="Stopped", style='Secondary.TLabel')
        self.status_text.pack(side=tk.LEFT)

        # Additional controls section
        additional_controls = ttk.Frame(self, style='Card.TFrame')
        additional_controls.pack(fill=tk.X)

        # Pause/Resume button (for future implementation)
        self.pause_button = ttk.Button(additional_controls, text="⏸️ Pause", state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 10))

        # Priority control
        priority_frame = ttk.Frame(additional_controls)
        priority_frame.pack(side=tk.LEFT, padx=(10, 0))

        ttk.Label(priority_frame, text="Priority:", style='Secondary.TLabel').pack(side=tk.LEFT, padx=(0, 5))

        self.priority_var = tk.StringVar(value="Normal")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var,
                                     values=["Low", "Normal", "High"], state="readonly", width=8)
        priority_combo.pack(side=tk.LEFT)

        # Quick actions
        quick_actions = ttk.Frame(additional_controls)
        quick_actions.pack(side=tk.RIGHT)

        ttk.Button(quick_actions, text="📊 Stats", command=self.show_stats).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_actions, text="🌐 Web UI", command=self.open_web_ui).pack(side=tk.LEFT, padx=(0, 5))

    def set_logged_in(self, logged_in):
        """Update UI based on login state"""
        self.is_logged_in = logged_in
        if logged_in:
            self.start_stop_button.config(state=tk.NORMAL)
        else:
            self.start_stop_button.config(state=tk.DISABLED)

    def set_worker_running(self, running):
        """Update UI based on worker running state"""
        self.is_running = running
        if running:
            self.start_stop_button.config(text="⏹️ Stop Worker", style='Danger.TButton')
            self.status_indicator.config(text="🟢", foreground="green")
            self.status_text.config(text="Running")
            self.pause_button.config(state=tk.NORMAL)
        else:
            self.start_stop_button.config(text="▶️ Start Worker", style='Primary.TButton')
            self.status_indicator.config(text="🔴", foreground="red")
            self.status_text.config(text="Stopped")
            self.pause_button.config(state=tk.DISABLED)

    def show_stats(self):
        """Show detailed statistics window"""
        # This would open a detailed stats window
        pass

    def open_web_ui(self):
        """Open Fishtest web interface"""
        webbrowser.open("https://tests.stockfishchess.org")


class SettingsFrame(ttk.LabelFrame):
    """Settings and preferences frame"""

    def __init__(self, parent, config_manager, theme=None, theme_change_callback=None):
        super().__init__(parent, text="⚙️ Settings", padding="15", style='Card.TLabelframe')
        self.config_manager = config_manager
        self.theme = theme
        self.theme_change_callback = theme_change_callback
        self.create_widgets()

    def create_widgets(self):
        """Create settings widgets"""
        # Theme selection
        theme_frame = ttk.Frame(self, style='Card.TFrame')
        theme_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(theme_frame, text="Theme:", style='Heading.TLabel').pack(side=tk.LEFT)

        # Get current theme from the theme object
        current_theme = "Light" if self.theme and self.theme.current_theme == 'light' else "Dark"
        self.theme_var = tk.StringVar(value=current_theme)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                  values=["Light", "Dark"], state="readonly", width=10)
        theme_combo.pack(side=tk.RIGHT)
        theme_combo.bind('<<ComboboxSelected>>', self.on_theme_change)

        # Auto-start options
        autostart_frame = ttk.Frame(self, style='Card.TFrame')
        autostart_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(autostart_frame, text="Auto-start:", style='Heading.TLabel').pack(side=tk.LEFT)

        self.autostart_var = tk.BooleanVar()
        ttk.Checkbutton(autostart_frame, text="Start worker on login",
                       variable=self.autostart_var).pack(side=tk.RIGHT)

        # Notification settings
        notification_frame = ttk.Frame(self, style='Card.TFrame')
        notification_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(notification_frame, text="Notifications:", style='Heading.TLabel').pack(anchor=tk.W)

        self.notify_completion_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(notification_frame, text="Notify on test completion",
                       variable=self.notify_completion_var).pack(anchor=tk.W, padx=(20, 0))

        self.notify_errors_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(notification_frame, text="Notify on errors",
                       variable=self.notify_errors_var).pack(anchor=tk.W, padx=(20, 0))

        # System tray option
        tray_frame = ttk.Frame(self, style='Card.TFrame')
        tray_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(tray_frame, text="System Integration:", style='Heading.TLabel').pack(side=tk.LEFT)

        self.minimize_to_tray_var = tk.BooleanVar()
        ttk.Checkbutton(tray_frame, text="Minimize to system tray",
                       variable=self.minimize_to_tray_var).pack(side=tk.RIGHT)

        # Action buttons
        button_frame = ttk.Frame(self, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(15, 0))

        ttk.Button(button_frame, text="💾 Save Settings",
                  command=self.save_settings, style='Primary.TButton').pack(side=tk.LEFT)

        ttk.Button(button_frame, text="🔄 Reset to Defaults",
                  command=self.reset_settings).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(button_frame, text="📁 Open Config Folder",
                  command=self.open_config_folder).pack(side=tk.RIGHT)

    def on_theme_change(self, event=None):
        """Handle theme change"""
        new_theme = self.theme_var.get().lower()
        if self.theme_change_callback:
            self.theme_change_callback(new_theme)

        # Show feedback to user
        from notification_system import StatusToast
        if hasattr(self, 'master') and hasattr(self.master, 'master'):
            toast = StatusToast(self.master.master)
            toast.show(f"Theme changed to {self.theme_var.get()}", toast_type='info')

    def save_settings(self):
        """Save current settings"""
        settings = {
            'theme': self.theme_var.get().lower(),
            'autostart': self.autostart_var.get(),
            'notify_completion': self.notify_completion_var.get(),
            'notify_errors': self.notify_errors_var.get(),
            'minimize_to_tray': self.minimize_to_tray_var.get()
        }
        # Save to config manager
        pass

    def reset_settings(self):
        """Reset settings to defaults"""
        self.theme_var.set("Light")
        self.autostart_var.set(False)
        self.notify_completion_var.set(True)
        self.notify_errors_var.set(True)
        self.minimize_to_tray_var.set(False)

    def open_config_folder(self):
        """Open configuration folder in file manager"""
        import subprocess
        import platform

        config_path = self.config_manager.config_file.parent

        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(config_path)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(config_path)])
            else:  # Linux
                subprocess.run(["xdg-open", str(config_path)])
        except Exception as e:
            print(f"Failed to open config folder: {e}")
