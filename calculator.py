import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Smooth Modern Calculator")
        self.root.geometry("320x500")
        self.root.resizable(False, False)
        
        # Color scheme
        self.bg_color = "#1E1E1E"
        self.display_bg = "#252525"
        self.num_button_bg = "#2D2D2D"
        self.op_button_bg = "#FF9500"
        self.clear_button_bg = "#FF3B30"
        self.button_fg = "#FFFFFF"
        self.active_num_bg = "#3E3E3E"
        self.active_op_bg = "#FFAA33"
        
        self.root.configure(bg=self.bg_color)
        
        # Custom fonts
        self.display_font = font.Font(family="Segoe UI", size=28)
        self.button_font = font.Font(family="Segoe UI", size=18)
        
        # Create display
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        self.display = tk.Label(
            root, 
            textvariable=self.display_var,
            font=self.display_font,
            bg=self.display_bg,
            fg=self.button_fg,
            anchor="e",
            padx=20,
            pady=25,
            relief=tk.FLAT
        )
        self.display.pack(fill=tk.X)
        
        # Create buttons
        buttons = [
            ('C', 'clear'), ('⌫', 'back'), ('%', 'percent'), ('/', 'divide'),
            ('7', '7'), ('8', '8'), ('9', '9'), ('×', 'multiply'),
            ('4', '4'), ('5', '5'), ('6', '6'), ('-', 'subtract'),
            ('1', '1'), ('2', '2'), ('3', '3'), ('+', 'add'),
            ('±', 'negate'), ('0', '0'), ('.', 'decimal'), ('=', 'equals')
        ]
        
        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        for i, (text, cmd) in enumerate(buttons):
            row = i // 4
            col = i % 4
            
            # Determine button style
            if cmd == 'clear':
                bg = self.clear_button_bg
            elif cmd in ['add', 'subtract', 'multiply', 'divide', 'percent', 'equals']:
                bg = self.op_button_bg
            else:
                bg = self.num_button_bg
                
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.button_font,
                bg=bg,
                fg=self.button_fg,
                activebackground=self.active_op_bg if cmd in ['add', 'subtract', 'multiply', 'divide', 'percent', 'equals'] else self.active_num_bg,
                activeforeground=self.button_fg,
                borderwidth=0,
                relief=tk.FLAT,
                command=lambda c=cmd: self.button_pressed(c)
            )
            btn.grid(
                row=row, 
                column=col, 
                sticky="nsew", 
                padx=2, 
                pady=2,
                ipadx=5,
                ipady=15
            )
            
            # Bind animation effects
            btn.bind('<ButtonPress-1>', lambda e, b=btn: self.animate_button_press(b))
            
            button_frame.grid_columnconfigure(col, weight=1)
            button_frame.grid_rowconfigure(row, weight=1)
        
        # Calculator state
        self.current_value = "0"
        self.stored_value = None
        self.operation = None
        self.reset_display = False
    
    def animate_button_press(self, button):
        """Add visual feedback when button is pressed"""
        original_bg = button.cget('bg')
        active_bg = button.cget('activebackground')
        
        # Immediately change to active color
        button.config(bg=active_bg)
        
        # Return to original color after 100ms
        button.after(100, lambda: button.config(bg=original_bg))
    
    def update_display(self):
        """Update the display with current value"""
        self.display_var.set(self.current_value)
    
    def button_pressed(self, command):
        """Handle all button presses"""
        if command.isdigit():
            self.input_digit(command)
        elif command == 'decimal':
            self.input_decimal()
        elif command == 'clear':
            self.clear()
        elif command == 'back':
            self.backspace()
        elif command == 'negate':
            self.negate()
        elif command in ['add', 'subtract', 'multiply', 'divide']:
            self.set_operation(command)
        elif command == 'equals':
            self.calculate()
        elif command == 'percent':
            self.percent()
    
    def input_digit(self, digit):
        """Handle digit input"""
        if self.reset_display:
            self.current_value = "0"
            self.reset_display = False
            
        if self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit
        self.update_display()
    
    def input_decimal(self):
        """Handle decimal point input"""
        if self.reset_display:
            self.current_value = "0"
            self.reset_display = False
            
        if '.' not in self.current_value:
            self.current_value += '.'
            self.update_display()
    
    def clear(self):
        """Clear the calculator"""
        self.current_value = "0"
        self.stored_value = None
        self.operation = None
        self.update_display()
    
    def backspace(self):
        """Handle backspace/delete"""
        if self.reset_display:
            return
            
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
        self.update_display()
    
    def negate(self):
        """Toggle positive/negative"""
        if self.current_value != "0":
            if self.current_value[0] == '-':
                self.current_value = self.current_value[1:]
            else:
                self.current_value = '-' + self.current_value
            self.update_display()
    
    def set_operation(self, op):
        """Set the operation to perform"""
        if self.operation and not self.reset_display:
            self.calculate()
        
        self.stored_value = float(self.current_value)
        self.operation = op
        self.reset_display = True
    
    def calculate(self):
        """Perform the calculation"""
        if self.operation and self.stored_value is not None:
            current = float(self.current_value)
            
            try:
                if self.operation == 'add':
                    result = self.stored_value + current
                elif self.operation == 'subtract':
                    result = self.stored_value - current
                elif self.operation == 'multiply':
                    result = self.stored_value * current
                elif self.operation == 'divide':
                    result = self.stored_value / current
                
                # Format the result
                if result.is_integer():
                    self.current_value = str(int(result))
                else:
                    self.current_value = "{:.10f}".format(result).rstrip('0').rstrip('.')
                
                self.update_display()
            except ZeroDivisionError:
                self.current_value = "Error"
                self.update_display()
            
            self.reset_display = True
            self.operation = None
    
    def percent(self):
        """Calculate percentage"""
        try:
            value = float(self.current_value) / 100
            if value.is_integer():
                self.current_value = str(int(value))
            else:
                self.current_value = "{:.10f}".format(value).rstrip('0').rstrip('.')
            self.update_display()
        except:
            self.current_value = "Error"
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()