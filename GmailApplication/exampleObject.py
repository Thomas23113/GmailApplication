class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def display_info(self):
        return f"This is a {self.year} {self.make} {self.model}."

# Creating an object of the Car class
my_car = Car("Toyota", "Camry", 2022)

# Accessing attributes and methods of the object
print(my_car.make)  # Output: Toyota
print(my_car.display_info())  # Output: This is a 2022 Toyota Camry.