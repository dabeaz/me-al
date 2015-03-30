# example.py
try:
    import meẗal
except ImportError:
    meẗal = __import__('met\u0308al')

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Decorator")
        return func(*args, **kwargs)
    return wrapper

# Apply meẗal to the module
with meẗal(decorator):
    import simple

# Call the module with meẗal applied
simple.hello('Guido')

# Import the module without meẗal
import simple
simple.hello('Guido')
