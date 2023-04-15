# This class controls the workings of the car's battery.  It can be used to change the current level of the battery,
# as well as to retrieve it's capacity and current level.
class Battery:
    total_capacity = 75 #kWh

    def __init__(self, battery_level):
        self.battery_level = battery_level
    
    def update_level(self, required_energy):
        self.battery_level -= required_energy

    def get_current_level(self):
        return self.battery_level
    
    def set_current_level(self, new_level):
        self.battery_level = new_level
        
    

# The EnergyMonitor class is the "host" of the battery, as all interactions with the battery itself run through this class (or an instance of it).
# This class is also responsible for approving routes calculated by the RoutePlanner class.
class EnergyMonitor:
    usage_per_kilometer = 0.16
    min_battery = 7.5
    
    def calculate_energy(self, distance):
        return distance * self.usage_per_kilometer
    
    def calculate_battery_level(self, battery):
        return battery.get_current_level()
    
    # "distance" will be provided by RoutePlanner
    def route_approval(self, battery, distance):
        total_required_energy = self.calculate_energy(distance)
        remaining_battery = self.calculate_battery_level(battery)
        if total_required_energy < remaining_battery and remaining_battery - total_required_energy >= self.min_battery:
            battery.update_level(total_required_energy)
            return True
        elif total_required_energy >= remaining_battery:
            print("The car needs to be charged to complete this trip.")
            return False

main_battery = Battery(75)
energy_monitor = EnergyMonitor()

# --- TESTS ---
assert isinstance(main_battery, Battery), "main_battery must be an instance of the Battery class" # PASSED
