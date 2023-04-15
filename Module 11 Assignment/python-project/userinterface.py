from energymonitor import EnergyMonitor, main_battery
from maintenancemonitor import MaintenanceMonitor, Part
from routeplanner import RoutePlanner, graph, Trip, Location
from data import charging_stations

# User Interface is the brain of the car. It controls all of the cars systems, which is why it is initialized with the classes of the three main operations.
class UserInterface:
    def __init__(self, route_planner, energy_monitor, maintenance_monitor, car):
        assert isinstance(route_planner, RoutePlanner) and isinstance(energy_monitor, EnergyMonitor) and isinstance(maintenance_monitor, MaintenanceMonitor) and isinstance(car, SelfDrivingCar), "UserInterface object must be initialized with RoutePlanner, EnergyMonitor, MaintenanceMonitor, and SelfDrivingCar objects."
        self.route_planner = route_planner
        self.energy_monitor = energy_monitor
        self.maintenance_monitor = maintenance_monitor
        self.car = car
    

    def get_user_input(self):
        user_input = self.route_planner.get_destination()
        return user_input
    
    # This method relies on the current location of the car, as well as user input for the destination.
    # For ease of testing and use, both 'origin' and 'destination' can be directly defined within the method arguments.
    # The method has an inbuilt test to catch user input that does not match the graph dictionary.
    def request_route(self, graph, origin=None, destination=None):
        if origin is None:
            origin = car.get_current_location()
        while True:
            if destination is None:
                destination = self.get_user_input()
            if destination in graph:
                return self.route_planner.calculate_route(graph, origin, destination)
            else:
                print("Error - Your car is unable to travel to this location. Please select a different location to proceed.")

    def suggest_route(self, graph, origin, destination):
        distance, route, approval = self.route_planner.calculate_route(graph, origin, destination)
        return route
    
    # This method is effectively useless, besides simulating navigation to the destination. It also updates the current location of the car.
    def begin_driving(self, destination):
        car.start_moving()
        car.stop_moving()
        car.set_current_location(destination)
        return "You have reached your destination."

    def display_battery_level(self, battery):
        return self.energy_monitor.calculate_battery_level(battery)

    def display_maintenance_date(self):
        return self.maintenance_monitor.calc_maintenance()

    def display_car_condition(self):
        total_condition = 0
        parts_count = len(maintenance_monitor.parts)

        for part in maintenance_monitor.parts.values():
            total_condition += part["condition"]

        return total_condition / parts_count

    def display_emergency(self):
        if maintenance_monitor.car_emergency == True:
            return "ALERT: CAR REQUIRES MAINTENANCE IMMEDIATELY. CALL ROADSIDE ASSISTANCE!"
        else:
            pass

    def car_ui(self):
        while True:
            print("Main Menu")
            print("---------")
            print("1. Battery Level")
            print("2. Maintenance Date")
            print("3. Car Condition")
            print("4. Navigation")
            print("5. Trips")
            print("6. Exit")
            print("-------------------")
            choice = input("Please choose (1-6):\n")

            if choice == '1':
                print("--- Battery Level ---")
                print(self.display_battery_level(main_battery))
                print("---------------------\n")
            elif choice == '2':
                print("--- Days until Maintenance ---")
                print(self.display_maintenance_date())
                print("------------------------------\n")
            elif choice == "3":
                print("--- Car Condition ---")
                print(self.display_car_condition())
                print("------------------------------\n")
            elif choice == "4":
                location = car.get_current_location()
                print("You are currently at {}.".format(location))
                destination = input("Where would you like to go:\n")
                self.request_route(graph, location, destination)
                ui.begin_driving(destination)
                print("You are now at {}.".format(destination))
            elif choice == "5":
                print("--- Trips ---")
                print(ui.route_planner.trips_taken)
                print("-------------\n")
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Incorrect input - Please enter a number between 1 and 6.\n")


# Contrary to my initial design, the SelfDrivingCar class does not host the User Interface. Instead, the User Interface hosts the car, as it issues the instructions to the car based on user input.
# This class controls the movement of the car and can be used to retrieve basic information about the car itself.
class SelfDrivingCar:
    def __init__(self, top_speed, current_location):
        self.top_speed = top_speed
        self.current_location = current_location
    
    def get_top_speed(self):
        return self.top_speed
    
    def get_current_location(self):
        return self.current_location
    
    def set_current_location(self, new_location):
        self.current_location = new_location
    
    def start_moving(self):
        print("Enter driving mode...")
    
    def stop_moving(self):
        print("Stopping the car...")




# --- INSTANCES ---
# The below objects, methods, and print statements were used to test the code and demonstrate its effectiveness.
route_planner = RoutePlanner(graph)
energy_monitor = EnergyMonitor()
maintenance_monitor = MaintenanceMonitor()
car = SelfDrivingCar(145, "The Pearl")
ui = UserInterface(route_planner, energy_monitor, maintenance_monitor, car)


ui.maintenance_monitor.add_part("Heat Pump", 99.0, 100.0, 50.0)
ui.maintenance_monitor.add_part("Front Motor", 100.0, 100.0, 60.0)
ui.maintenance_monitor.add_part("Battery", 100.0, 100.0, 50.0)
ui.maintenance_monitor.add_part("Rear Motor", 100.0, 100.0, 60.0)
ui.maintenance_monitor.add_part("Charge Port", 100.0, 100.0, 30.0)


if __name__ == "__main__":
    ui.car_ui()
        



# --- UNIT TESTS ---
# This section of the code contains all tests written using the assert statement. I tried to test every method within my code,
# among other data, to ensure that the code works as expected. Test can be commented out (#) to run individual code elements.
# Since the 'assert' statements are currently active, the program will print to the console automatically.

# --- SELF DRIVING CAR TESTS ---
# assert isinstance(car.top_speed, int) # PASSED
# assert car.top_speed == 145 # PASSED
# assert isinstance(car.current_location, str) # PASSED
# ui.begin_driving("Mall of Qatar")
# assert car.current_location == "Mall of Qatar" # PASSED
# car.set_current_location("Souq Waqif")
# assert car.get_current_location() == "Souq Waqif" # PASSED

# --- USER INTERFACE TESTS ---
# assert isinstance(route_planner, RoutePlanner) # PASSED
# assert isinstance(energy_monitor, EnergyMonitor) # PASSED
# assert isinstance(maintenance_monitor, MaintenanceMonitor) # PASSED
# assert isinstance(car, SelfDrivingCar) # PASSED
# assert isinstance(ui.get_user_input(), str), "User Input should be a string." # PASSED
# assert ui.request_route(graph, "Souq Waqif", "Aspire") == (11, ['Souq Waqif', 'Aspire'], True) # PASSED
# assert ui.suggest_route(graph, "Aspire", "City Center") == ['Aspire', 'Souq Waqif', 'Corniche', 'Doha Exhibition Center', 'City Center'] # PASSED
# assert isinstance(ui.display_battery_level(main_battery), float), "The battery level must be represented as a float" # PASSED
# assert isinstance(ui.display_car_condition(), float), "The condition of the car must be represented as a float" # PASSED
# print(ui.display_maintenance_date())
# ui.maintenance_monitor.car_emergency = True
# assert ui.display_emergency() == "ALERT: CAR REQUIRES MAINTENANCE IMMEDIATELY. CALL ROADSIDE ASSISTANCE!", "Emergency should be triggered"
# ui.maintenance_monitor.car_emergency = False

# --- BATTERY TESTS ---
# main_battery.set_current_level(75)
# assert main_battery.battery_level == 75, "Level should be 75" # PASSED
# main_battery.set_current_level(40)
# assert main_battery.battery_level == 40, "Total Capacity should be 40" # PASSED
# main_battery.update_level(20)
# assert main_battery.get_current_level() == 20, "Level should be 20" # PASSED

# --- ENERGY MONITOR TESTS ---
# assert energy_monitor.calculate_energy(20) == 3.2, "Should equal to 3.2" # PASSED
# assert energy_monitor.calculate_battery_level(main_battery) == 20, "Level should be 20" # PASSED
# assert energy_monitor.route_approval(main_battery, 20) == True, "Route should be approved" # PASSED
# assert energy_monitor.route_approval(main_battery, 1000) == False, "Route should be rejected" # PASSED

# --- TRIP TEST ---
# trip = Trip("Holiday", 200, "08/04/2023")
# assert trip.name == "Holiday", "Trip name should be 'Holiday'" # PASSED
# assert trip.distance == 200, "Trip distance should be 200" # PASSED
# assert trip.date == "08/04/2023", "Trip date should be '08/04/2023" # PASSED

# --- LOCATION TEST ---
# location = Location("The Pearl", 25.36898, 51.55106)
# assert location.name == "The Pearl", "Location name should be 'The Pearl'" # PASSED
# assert isinstance(location.lat_coord, float), "Coordinates should be floats" # PASSED
# assert isinstance(location.long_coord, float), "Coordinates should be floats" # PASSED

# --- ROUTE PLANNER TEST ---
# assert isinstance(route_planner.original_graph, dict), "Original Graph should be a dictionary" # PASSED
# assert route_planner.calculate_route(graph, "The Pearl", "Aspire") == (26, ['The Pearl', 'Landmark Mall', 'Aspire'], True), "Should return/print '(26, ['The Pearl', 'Landmark Mall', 'Aspire'], True)'" # PASSED
# assert isinstance(route_planner.calculate_route(graph, "The Pearl", "Aspire"), tuple), "This function should return a tuple" # PASSED
# main_battery.set_current_level(75)
# assert route_planner.suggest_charging(graph, "Corniche", charging_stations) == "Your car needs to be charged and will be travelling to The Pearl, which is 13 km away from here." # PASSED
# assert route_planner.check_battery(20) == True, "Should return 'True'" # PASSED
# assert isinstance(route_planner.get_trips(), dict), "'get_trips' should be a dictionary" # PASSED

# --- PART TEST ---
# part = Part("Headlight Fluid", 79.0, 100.0, 10.0)
# assert all([isinstance(part.name, str), (part.condition, float), (part.max_condition, float), (part.min_condition, float), part.name == "Headlight Fluid"])
# part.set_current(44.0)
# assert part.get_current() == 44.0, "Current condition should be 44.0"
# assert part.get_min() == 10.0, "Min condition should be 10.0"

# --- MAINTENANCE MONITOR TEST ---
# assert maintenance_monitor.car_emergency == False, "Car emergency should be False"
# assert maintenance_monitor.parts == {'Heat Pump': {'condition': 99.0, 'max': 100.0, 'min': 50.0}, 'Front Motor': {'condition': 100.0, 'max': 100.0, 'min': 60.0}, 'Battery': {'condition': 100.0, 'max': 100.0, 'min': 50.0}, 'Rear Motor': {'condition': 100.0, 'max': 100.0, 'min': 60.0}, 'Charge Port': {'condition': 100.0, 'max': 100.0, 'min': 30.0}}
# assert maintenance_monitor.get_current_condition("Heat Pump") == 99.0, "Current condition should be 99.0"
# assert maintenance_monitor.get_min_condition("Battery") == 50.0, "Min condition should be 50.0"
# assert maintenance_monitor.get_max_condition("Charge Port") ==  100.0, "Max condition should be 100.0"
# assert maintenance_monitor.list_parts() == ['Battery', 'Heat Pump', 'Rear Motor', 'Front Motor', 'Charge Port']
# assert isinstance(maintenance_monitor.list_parts(), list), "Should be a list"
# assert isinstance(maintenance_monitor.get_total_km(), int), "Should be an integer"
# assert isinstance(maintenance_monitor.get_total_days(), int), "Should be an integer"


# print(ui.request_route(graph, "The Pearl")) # WORKS
# print(ui.route_planner.get_origin(car)) # WORKS
# print(ui.request_route(graph, "Aspire", "Mall of Qatar")) # WORKS
# print(ui.suggest_route(graph, "The Pearl", "Aspire")) # WORKS
# print(ui.display_battery_level(main_battery)) # WORKS
# print(ui.begin_driving("Aspire")) # WORKS

# print(ui.display_maintenance_date()) # WORKS
# print(ui.display_car_condition()) # WORKS
