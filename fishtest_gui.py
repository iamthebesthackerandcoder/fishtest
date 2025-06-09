#!/usr/bin/env python3
"""
Fishtest Worker GUI - Main Application
Modern GUI for fishtest worker with enhanced UX, login, core selection, password memory, and background operation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
from pathlib import Path

from config_manager import ConfigManager
from worker_controller import WorkerController
from gui_components import ModernLoginFrame, ModernStatusFrame, ModernControlFrame, SettingsFrame
from ui_theme import UITheme
from notification_system import NotificationManager, ProgressIndicator, StatusToast

class FishtestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🐟 Fishtest Worker")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        self.root.minsize(700, 600)

        # Load saved configuration first to get theme preference
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()

        # Initialize theme with saved preference
        saved_theme = self.config.get('theme', 'light')
        self.theme = UITheme(saved_theme)
        self.style = self.theme.apply_theme(self.root)

        # Initialize components
        self.worker_controller = WorkerController()
        self.notification_manager = NotificationManager()
        self.progress_indicator = ProgressIndicator(self.root)
        self.status_toast = StatusToast(self.root)

        # Create GUI components
        self.create_widgets()

        # Set up window closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Set up keyboard shortcuts
        self.setup_shortcuts()
        
    def create_widgets(self):
        """Create the modern tabbed GUI widgets"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="15", style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Modern.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_main_tab()
        self.create_logs_tab()
        self.create_settings_tab()

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def create_main_tab(self):
        """Create the main worker tab"""
        main_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(main_tab, text="🏠 Worker")

        # Create main tab content with padding
        content_frame = ttk.Frame(main_tab, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Login section
        self.login_frame = ModernLoginFrame(content_frame, self.config, self.on_login, self.theme)
        self.login_frame.pack(fill=tk.X, pady=(0, 15))

        # Control section
        self.control_frame = ModernControlFrame(content_frame, self.on_start_stop, self.theme)
        self.control_frame.pack(fill=tk.X, pady=(0, 15))

        # Quick status section
        quick_status_frame = ttk.LabelFrame(content_frame, text="📈 Quick Status",
                                          padding="10", style='Card.TLabelframe')
        quick_status_frame.pack(fill=tk.X)

        self.quick_status_var = tk.StringVar(value="Ready to start")
        quick_status_label = ttk.Label(quick_status_frame, textvariable=self.quick_status_var,
                                     style='Status.TLabel', font=('Segoe UI', 11))
        quick_status_label.pack()

    def create_logs_tab(self):
        """Create the logs and monitoring tab"""
        logs_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(logs_tab, text="📊 Logs & Stats")

        # Create logs tab content
        content_frame = ttk.Frame(logs_tab, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Status and logs section
        self.status_frame = ModernStatusFrame(content_frame, self.theme)
        self.status_frame.pack(fill=tk.BOTH, expand=True)

    def create_settings_tab(self):
        """Create the settings tab"""
        settings_tab = ttk.Frame(self.notebook, style='Card.TFrame')
        self.notebook.add(settings_tab, text="⚙️ Settings")

        # Create settings tab content
        content_frame = ttk.Frame(settings_tab, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Settings section
        self.settings_frame = SettingsFrame(content_frame, self.config_manager, self.theme, self.on_theme_change)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        # About section
        about_frame = ttk.LabelFrame(content_frame, text="ℹ️ About",
                                   padding="10", style='Card.TLabelframe')
        about_frame.pack(fill=tk.X, pady=(15, 0))

        about_text = """Fishtest Worker GUI v2.0
A modern interface for the Fishtest distributed testing framework.
Built with Python and tkinter for enhanced user experience."""

        ttk.Label(about_frame, text=about_text, style='Secondary.TLabel',
                 justify=tk.LEFT).pack(anchor=tk.W)

        # Links
        links_frame = ttk.Frame(about_frame)
        links_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(links_frame, text="🌐 Fishtest Website",
                  command=lambda: self.open_url("https://tests.stockfishchess.org")).pack(side=tk.LEFT)
        ttk.Button(links_frame, text="📚 Documentation",
                  command=lambda: self.open_url("https://github.com/official-stockfish/fishtest")).pack(side=tk.LEFT, padx=(10, 0))

    def setup_shortcuts(self):
        """Set up keyboard shortcuts"""
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<Control-l>', lambda e: self.focus_login())
        self.root.bind('<Control-s>', lambda e: self.toggle_worker())
        self.root.bind('<F5>', lambda e: self.refresh_status())
        self.root.bind('<Control-t>', lambda e: self.toggle_theme())

    def focus_login(self):
        """Focus on login username field"""
        self.notebook.select(0)  # Switch to main tab
        if hasattr(self.login_frame, 'username_entry'):
            self.login_frame.username_entry.focus()

    def toggle_worker(self):
        """Toggle worker start/stop via keyboard"""
        if self.control_frame.is_logged_in:
            self.on_start_stop()

    def refresh_status(self):
        """Refresh status display"""
        if hasattr(self, 'status_frame'):
            self.status_frame.add_log_message("Status refreshed", 'info')

    def toggle_theme(self):
        """Toggle between light and dark theme via keyboard shortcut"""
        current_theme = self.theme.current_theme
        new_theme = 'dark' if current_theme == 'light' else 'light'
        self.on_theme_change(new_theme)

        # Update the settings dropdown if it exists
        if hasattr(self, 'settings_frame') and hasattr(self.settings_frame, 'theme_var'):
            self.settings_frame.theme_var.set(new_theme.title())

    def open_url(self, url):
        """Open URL in default browser"""
        import webbrowser
        webbrowser.open(url)

    def on_theme_change(self, new_theme):
        """Handle theme change from settings"""
        try:
            # Update theme
            self.theme.switch_theme(new_theme)

            # Reapply theme to root and get new style
            self.style = self.theme.apply_theme(self.root)

            # Refresh all widgets with new theme
            self.theme.refresh_all_widgets(self.root)

            # Update all components to use new theme
            self._update_component_themes()

            # Save theme preference
            config = self.config_manager.load_config()
            config['theme'] = new_theme
            self.config_manager.save_config(config)

            # Show success message
            self.status_toast.show(f"Theme changed to {new_theme.title()}", toast_type='success')

            # Log the theme change
            if hasattr(self, 'status_frame'):
                self.status_frame.add_log_message(f"Theme changed to {new_theme.title()}", 'info')

        except Exception as e:
            self.status_toast.show(f"Failed to change theme: {e}", toast_type='error')
            if hasattr(self, 'status_frame'):
                self.status_frame.add_log_message(f"Theme change failed: {e}", 'error')

    def _update_component_themes(self):
        """Update all components to use the new theme"""
        try:
            # Update login frame theme
            if hasattr(self, 'login_frame'):
                self.login_frame.theme = self.theme

            # Update status frame theme
            if hasattr(self, 'status_frame'):
                self.status_frame.theme = self.theme
                # Update log text colors
                if hasattr(self.status_frame, 'log_text'):
                    bg_color = self.theme.get_color('bg_secondary')
                    fg_color = self.theme.get_color('text_primary')
                    self.status_frame.log_text.config(bg=bg_color, fg=fg_color)

            # Update control frame theme
            if hasattr(self, 'control_frame'):
                self.control_frame.theme = self.theme

            # Update settings frame theme
            if hasattr(self, 'settings_frame'):
                self.settings_frame.theme = self.theme

            # Force a refresh of the display
            self.root.update_idletasks()

        except Exception as e:
            print(f"Error updating component themes: {e}")
        
    def on_login(self):
        """Login to fishtest"""
        def login_in_thread():
            try:
                # Get current values
                username = self.login_frame.get_username()
                password = self.login_frame.get_password()
                cores = self.login_frame.get_cores()

                if not username or not password:
                    messagebox.showerror("Error", "Please enter username and password")
                    return

                self.status_frame.set_status("Logging in...")
                self.progress_indicator.show("Connecting to Fishtest server...")

                # Import here to avoid issues
                sys.path.insert(0, str(Path(__file__).resolve().parent / "worker"))
                from worker import verify_credentials

                # Test connection
                remote = "https://tests.stockfishchess.org"
                result = verify_credentials(remote, username, password, False)

                if result is True:
                    self.progress_indicator.hide()
                    self.status_frame.set_status("Login successful!")
                    self.status_frame.add_log_message("Successfully logged in to Fishtest!", 'success')
                    self.quick_status_var.set("✅ Logged in - Ready to start worker")
                    self.status_toast.show("Successfully logged in to Fishtest!", toast_type='success')
                    self.notification_manager.notify_login_success()

                    # Save configuration
                    self.config = {
                        'username': username,
                        'password': password,
                        'cores': cores
                    }
                    self.config_manager.save_config(self.config)

                    # Update UI
                    self.login_frame.set_logged_in(True)
                    self.control_frame.set_logged_in(True)

                elif result is False:
                    self.progress_indicator.hide()
                    self.status_frame.set_status("Login failed - Invalid credentials")
                    self.status_frame.add_log_message("Login failed - Invalid credentials", 'error')
                    self.quick_status_var.set("❌ Login failed")
                    self.status_toast.show("Invalid username or password", toast_type='error')
                    self.notification_manager.notify_login_failed()
                    self.login_frame.set_logged_in(False)
                    self.control_frame.set_logged_in(False)
                else:
                    self.progress_indicator.hide()
                    self.status_frame.set_status("Login failed - Network error")
                    self.status_frame.add_log_message("Login failed - Network error", 'error')
                    self.quick_status_var.set("⚠️ Network error")
                    self.status_toast.show("Network error - unable to connect to server", toast_type='error')
                    self.notification_manager.notify_error("Network connection failed")
                    self.login_frame.set_logged_in(False)
                    self.control_frame.set_logged_in(False)

            except Exception as e:
                self.progress_indicator.hide()
                self.status_frame.set_status(f"Error: {e}")
                self.status_frame.add_log_message(f"Login error: {e}", 'error')
                self.quick_status_var.set("❌ Error occurred")
                self.status_toast.show(f"Login failed: {e}", toast_type='error')
                self.notification_manager.notify_error(str(e))
                self.login_frame.set_logged_in(False)
                self.control_frame.set_logged_in(False)

        threading.Thread(target=login_in_thread, daemon=True).start()
        
    def on_start_stop(self):
        """Start or stop the worker"""
        if self.worker_controller.is_running():
            self.stop_worker()
        else:
            self.start_worker()
            
    def start_worker(self):
        """Start the fishtest worker"""
        try:
            # Check if logged in
            if not self.control_frame.is_logged_in:
                messagebox.showerror("Error", "Please login first")
                return

            # Get current values
            username = self.login_frame.get_username()
            password = self.login_frame.get_password()
            cores = self.login_frame.get_cores()

            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password")
                return
                
            # Save configuration
            self.config = {
                'username': username,
                'password': password,
                'cores': cores
            }
            self.config_manager.save_config(self.config)
            
            # Start worker
            self.status_frame.set_status("Starting worker...")
            self.status_frame.add_log_message("Starting fishtest worker...", 'info')
            self.quick_status_var.set("🚀 Starting worker...")
            self.status_toast.show("Starting fishtest worker...", toast_type='info')
            self.worker_controller.start_worker(username, password, cores, self.on_worker_output)

            # Update UI
            self.login_frame.set_worker_running(True)
            self.control_frame.set_worker_running(True)
            self.status_frame.set_status("Worker running in background")
            self.status_frame.add_log_message("Worker started successfully", 'success')
            self.quick_status_var.set("🟢 Worker running")
            self.status_toast.show("Worker started successfully!", toast_type='success')
            self.notification_manager.notify_worker_started()

        except Exception as e:
            self.status_frame.set_status(f"Error: {e}")
            self.status_frame.add_log_message(f"Failed to start worker: {e}", 'error')
            self.quick_status_var.set("❌ Start failed")
            self.status_toast.show(f"Failed to start worker: {e}", toast_type='error')
            self.notification_manager.notify_error(f"Failed to start worker: {e}")
            messagebox.showerror("Error", f"Failed to start worker: {e}")
            
    def stop_worker(self):
        """Stop the fishtest worker"""
        try:
            self.status_frame.set_status("Stopping worker...")
            self.status_frame.add_log_message("Stopping fishtest worker...", 'info')
            self.quick_status_var.set("⏹️ Stopping worker...")
            self.status_toast.show("Stopping worker...", toast_type='info')
            self.worker_controller.stop_worker()

            # Update UI
            self.login_frame.set_worker_running(False)
            self.control_frame.set_worker_running(False)
            self.status_frame.set_status("Worker stopped")
            self.status_frame.add_log_message("Worker stopped successfully", 'info')
            self.quick_status_var.set("⏹️ Worker stopped")
            self.status_toast.show("Worker stopped successfully", toast_type='info')
            self.notification_manager.notify_worker_stopped()

        except Exception as e:
            self.status_frame.set_status(f"Error: {e}")
            self.status_frame.add_log_message(f"Failed to stop worker: {e}", 'error')
            self.quick_status_var.set("❌ Stop failed")
            self.status_toast.show(f"Failed to stop worker: {e}", toast_type='error')
            self.notification_manager.notify_error(f"Failed to stop worker: {e}")
            messagebox.showerror("Error", f"Failed to stop worker: {e}")
            
    def on_worker_output(self, message):
        """Handle worker output messages with enhanced formatting"""
        # Determine message type based on content
        msg_type = 'info'
        if any(word in message.lower() for word in ['error', 'failed', 'exception']):
            msg_type = 'error'
        elif any(word in message.lower() for word in ['warning', 'warn']):
            msg_type = 'warning'
        elif any(word in message.lower() for word in ['completed', 'finished', 'success']):
            msg_type = 'success'

        self.status_frame.add_log_message(message, msg_type)

        # Update quick status for important messages
        if 'completed' in message.lower():
            self.quick_status_var.set("✅ Test completed")
        elif 'error' in message.lower():
            self.quick_status_var.set("⚠️ Error occurred")
        
    def on_closing(self):
        """Handle window closing"""
        if self.worker_controller.is_running():
            if messagebox.askokcancel("Quit", "Worker is still running. Stop worker and quit?"):
                self.worker_controller.stop_worker()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    """Main function"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        return 1

    root = tk.Tk()
    FishtestGUI(root)
    root.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main())
