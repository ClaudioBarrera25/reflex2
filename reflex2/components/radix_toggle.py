import reflex as rx

class ToggleGroup(rx.Component):
    """Toggle group component."""
    
    library = "@radix-ui/react-toggle-group"
    tag = "ToggleGroup"

    is_default = True
    scene: rx.Var[str]

# class ToggleGroup(rx.Component):
#     """Toggle group component."""
    
#     library = "@radix-ui/react-toggle-group"
#     tag = "Root"  # Radix uses Root for main component
    
#     # Define props using rx.Var
#     type: rx.Var[str]
#     value: rx.Var[str]
#     defaultValue: rx.Var[str]
    
#     # Event handler for value changes
#     on_value_change: rx.EventHandler