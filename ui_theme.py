"""
UI Theme and Styling for Fishtest Worker GUI
Provides modern styling, colors, and theme management.
"""

import tkinter as tk
from tkinter import ttk

class UITheme:
    """Modern UI theme with colors and styling"""
    
    # Color schemes
    LIGHT_THEME = {
        'bg_primary': '#ffffff',
        'bg_secondary': '#f8f9fa',
        'bg_accent': '#e9ecef',
        'text_primary': '#212529',
        'text_secondary': '#6c757d',
        'accent_color': '#0d6efd',
        'success_color': '#198754',
        'warning_color': '#fd7e14',
        'danger_color': '#dc3545',
        'border_color': '#dee2e6',
        'hover_color': '#e9ecef'
    }
    
    DARK_THEME = {
        'bg_primary': '#212529',
        'bg_secondary': '#343a40',
        'bg_accent': '#495057',
        'text_primary': '#f8f9fa',
        'text_secondary': '#adb5bd',
        'accent_color': '#0d6efd',
        'success_color': '#198754',
        'warning_color': '#fd7e14',
        'danger_color': '#dc3545',
        'border_color': '#495057',
        'hover_color': '#495057'
    }
    
    def __init__(self, theme='light'):
        self.current_theme = theme
        self.colors = self.LIGHT_THEME if theme == 'light' else self.DARK_THEME
        
    def apply_theme(self, root):
        """Apply theme to the root window and configure ttk styles"""
        # Configure root window
        root.configure(bg=self.colors['bg_primary'])
        
        # Create and configure ttk style
        style = ttk.Style()
        
        # Configure frame styles
        style.configure('Card.TFrame',
                       background=self.colors['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Accent.TFrame',
                       background=self.colors['bg_accent'],
                       relief='flat')
        
        # Configure label styles
        style.configure('Heading.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure('Secondary.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       font=('Segoe UI', 9))
        
        style.configure('Status.TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_color'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure button styles
        style.configure('Primary.TButton',
                       background=self.colors['accent_color'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        
        style.map('Primary.TButton',
                 background=[('active', self.colors['accent_color']),
                           ('pressed', self.colors['accent_color'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success_color'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        
        style.configure('Danger.TButton',
                       background=self.colors['danger_color'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10))
        
        # Configure entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['bg_primary'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=self.colors['text_primary'])
        
        # Configure labelframe styles
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_secondary'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=self.colors['border_color'])
        
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'))
        
        # Configure notebook styles for tabs
        style.configure('Modern.TNotebook',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       padding=[20, 10],
                       font=('Segoe UI', 10))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.colors['bg_secondary']),
                           ('active', self.colors['hover_color'])])
        
        return style
    
    def get_color(self, color_name):
        """Get a color from the current theme"""
        return self.colors.get(color_name, '#000000')
    
    def switch_theme(self, theme_name):
        """Switch to a different theme"""
        self.current_theme = theme_name
        self.colors = self.LIGHT_THEME if theme_name == 'light' else self.DARK_THEME
    
    @staticmethod
    def create_tooltip(widget, text):
        """Create a tooltip for a widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, 
                           background='#ffffe0', 
                           foreground='#000000',
                           relief='solid', 
                           borderwidth=1,
                           font=('Segoe UI', 9))
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
