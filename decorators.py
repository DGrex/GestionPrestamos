def decorator_menu(title):
    def wrapper(func):
        def inner(*args, **kwargs):
            print("\n========================================")
            print(f" {title} ")
            print("========================================")
            return func(*args, **kwargs)
        return inner
    return wrapper
