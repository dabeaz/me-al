# example.py
try:
    import meẗal
except ImportError:
    meẗal = __import__('met\u0308al')

def decorator1(func):
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        return func(*args, **kwargs)
    return wrapper

# Use a module with decorator1 meẗal applied
with meẗal(decorator1):
    import simple
    simple.hello('Guido')

# Use a module with decorator2 meẗal applied
with meẗal(decorator2):
    import simple
    simple.hello('Guido')

# Use a module with decorator1 and decorator2 meẗal applied
with meẗal(decorator1), meẗal(decorator2):
    import simple
    simple.hello('Guido')
