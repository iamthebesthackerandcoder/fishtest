"""
Notification System for Fishtest Worker GUI
Provides desktop notifications and system tray integration.
"""

import tkinter as tk
from tkinter import messagebox
import threading

try:
    # Try to import plyer for cross-platform notifications
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

class NotificationManager:
    """Manages desktop notifications and system alerts"""
    
    def __init__(self, app_name="Fishtest Worker"):
        self.app_name = app_name
        self.enabled = True
        self.sound_enabled = True
        
    def show_notification(self, title, message, notification_type='info', timeout=5):
        """Show a desktop notification"""
        if not self.enabled:
            return
            
        try:
            if PLYER_AVAILABLE:
                # Use plyer for cross-platform notifications
                notification.notify(
                    title=title,
                    message=message,
                    app_name=self.app_name,
                    timeout=timeout
                )
            else:
                # Fallback to tkinter messagebox
                self._show_fallback_notification(title, message, notification_type)
                
        except Exception as e:
            print(f"Notification error: {e}")
            self._show_fallback_notification(title, message, notification_type)
    
    def _show_fallback_notification(self, title, message, notification_type):
        """Fallback notification using tkinter"""
        def show_popup():
            if notification_type == 'error':
                messagebox.showerror(title, message)
            elif notification_type == 'warning':
                messagebox.showwarning(title, message)
            else:
                messagebox.showinfo(title, message)
        
        # Show in a separate thread to avoid blocking
        threading.Thread(target=show_popup, daemon=True).start()
    
    def notify_worker_started(self):
        """Notify when worker starts"""
        self.show_notification(
            "Fishtest Worker",
            "Worker started successfully and is now processing tests.",
            'info'
        )
    
    def notify_worker_stopped(self):
        """Notify when worker stops"""
        self.show_notification(
            "Fishtest Worker", 
            "Worker has been stopped.",
            'info'
        )
    
    def notify_test_completed(self, test_name=""):
        """Notify when a test is completed"""
        message = f"Test completed: {test_name}" if test_name else "Test completed successfully"
        self.show_notification(
            "Test Completed",
            message,
            'info'
        )
    
    def notify_error(self, error_message):
        """Notify about errors"""
        self.show_notification(
            "Fishtest Worker Error",
            f"An error occurred: {error_message}",
            'error'
        )
    
    def notify_login_success(self):
        """Notify successful login"""
        self.show_notification(
            "Login Successful",
            "Successfully logged in to Fishtest server.",
            'info'
        )
    
    def notify_login_failed(self):
        """Notify failed login"""
        self.show_notification(
            "Login Failed",
            "Failed to log in to Fishtest server. Please check your credentials.",
            'error'
        )
    
    def set_enabled(self, enabled):
        """Enable or disable notifications"""
        self.enabled = enabled
    
    def set_sound_enabled(self, enabled):
        """Enable or disable notification sounds"""
        self.sound_enabled = enabled


class ProgressIndicator:
    """Progress indicator for long-running operations"""
    
    def __init__(self, parent, title="Processing..."):
        self.parent = parent
        self.title = title
        self.window = None
        self.progress_var = None
        self.status_var = None
        self.is_active = False
        
    def show(self, message="Please wait..."):
        """Show progress indicator"""
        if self.is_active:
            return
            
        self.is_active = True
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("400x150")
        self.window.resizable(False, False)
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.window.winfo_screenheight() // 2) - (150 // 2)
        self.window.geometry(f"400x150+{x}+{y}")
        
        # Create content
        main_frame = tk.Frame(self.window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status message
        self.status_var = tk.StringVar(value=message)
        status_label = tk.Label(main_frame, textvariable=self.status_var, 
                               font=('Segoe UI', 10))
        status_label.pack(pady=(0, 15))
        
        # Progress bar
        from tkinter import ttk
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                     mode='indeterminate', length=350)
        progress_bar.pack(pady=(0, 15))
        progress_bar.start(10)  # Start animation
        
        # Cancel button (optional)
        cancel_button = ttk.Button(main_frame, text="Cancel", 
                                  command=self.hide)
        cancel_button.pack()
        
        self.window.protocol("WM_DELETE_WINDOW", self.hide)
        
    def update_status(self, message):
        """Update status message"""
        if self.status_var:
            self.status_var.set(message)
            
    def set_progress(self, value):
        """Set progress value (0-100)"""
        if self.progress_var:
            self.progress_var.set(value)
            
    def hide(self):
        """Hide progress indicator"""
        if self.window and self.is_active:
            self.is_active = False
            self.window.grab_release()
            self.window.destroy()
            self.window = None


class StatusToast:
    """Temporary status toast notification"""
    
    def __init__(self, parent):
        self.parent = parent
        self.toast_window = None
        
    def show(self, message, duration=3000, toast_type='info'):
        """Show a temporary toast notification"""
        if self.toast_window:
            self.toast_window.destroy()
            
        self.toast_window = tk.Toplevel(self.parent)
        self.toast_window.wm_overrideredirect(True)
        self.toast_window.attributes('-topmost', True)
        
        # Position at bottom right of parent window
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        toast_width = 300
        toast_height = 80
        
        x = parent_x + parent_width - toast_width - 20
        y = parent_y + parent_height - toast_height - 20
        
        self.toast_window.geometry(f"{toast_width}x{toast_height}+{x}+{y}")
        
        # Style based on type
        colors = {
            'info': {'bg': '#d1ecf1', 'fg': '#0c5460', 'border': '#bee5eb'},
            'success': {'bg': '#d4edda', 'fg': '#155724', 'border': '#c3e6cb'},
            'warning': {'bg': '#fff3cd', 'fg': '#856404', 'border': '#ffeaa7'},
            'error': {'bg': '#f8d7da', 'fg': '#721c24', 'border': '#f5c6cb'}
        }
        
        color_scheme = colors.get(toast_type, colors['info'])
        
        # Create frame with border
        frame = tk.Frame(self.toast_window, 
                        bg=color_scheme['border'], 
                        padx=2, pady=2)
        frame.pack(fill=tk.BOTH, expand=True)
        
        inner_frame = tk.Frame(frame, 
                              bg=color_scheme['bg'], 
                              padx=15, pady=10)
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message label
        label = tk.Label(inner_frame, 
                        text=message, 
                        bg=color_scheme['bg'], 
                        fg=color_scheme['fg'],
                        font=('Segoe UI', 9),
                        wraplength=250,
                        justify=tk.LEFT)
        label.pack()
        
        # Auto-hide after duration
        self.parent.after(duration, self._hide_toast)
        
        # Click to dismiss
        self.toast_window.bind('<Button-1>', lambda e: self._hide_toast())
        label.bind('<Button-1>', lambda e: self._hide_toast())
        
    def _hide_toast(self):
        """Hide the toast notification"""
        if self.toast_window:
            self.toast_window.destroy()
            self.toast_window = None
