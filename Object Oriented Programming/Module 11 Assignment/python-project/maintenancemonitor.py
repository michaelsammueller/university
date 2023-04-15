from routeplanner import route_planner

# All parts of the car are instances of this class and stored in the 'parts' dictionary of the MaintenanceMonitor class.
class Part:
    def __init__(self, name, condition, max_condition, min_condition):
        self.name = name
        self.condition = condition
        self.max_condition = max_condition
        self.min_condition = min_condition
    
    def get_current(self):
        return self.condition
    
    def set_current(self, new_condition):
        self.condition = new_condition

    def get_min(self):
        return self.min_condition
        

# This class controls all car parts and can retrieve data about them. It also calculates how many days are left until maintenance is due,
# based on degradation of parts and trips taken.
class MaintenanceMonitor:
    car_emergency = False

    def __init__(self):
        self.parts = {}

    def add_part(self, part_name, condition, max_condition, min_condition):
        self.parts[part_name] = {"condition": condition, "max": max_condition, "min": min_condition}

    def get_current_condition(self, part_name):
        return self.parts[part_name]["condition"]
    
    def get_min_condition(self, part_name):
        return self.parts[part_name]["min"]
    
    def get_max_condition(self, part_name):
        return self.parts[part_name]["max"]
    
    def list_parts(self):
        return list(self.parts.keys())

    # Need to get info from RoutePlanner
    def get_total_km(self):
        total_km = 0
        for trip in route_planner.trips_taken.values():
            total_km += trip["km"]
        return total_km

    def get_total_days(self):
        days = set()
        for trip in route_planner.trips_taken.values():
            days.add(trip['date'])
        return len(days)

    # Based on info from RoutePlanner
    def calc_maintenance(self):
        total_days = self.get_total_days()

        maintenance_dates = []

        for part_name, part in self.parts.items():
            min_condition = self.get_min_condition(part_name)
            current_condition = self.get_current_condition(part_name)
            max_condition = self.get_max_condition(part_name)

            if current_condition <= min_condition:
                self.car_emergency = True
                return "Warning: The {} of your car needs to be replaced immediately! Current condition: {}%.".format(part_name, current_condition)
            
            else: 
                try: 
                    decline = max_condition - current_condition
                    per_day = total_days / decline
                    life_span = current_condition - min_condition
                    days_until_maint = int(life_span / per_day)

                    if days_until_maint == 0:
                        self.car_emergency = True
                        maintenance_dates.append((part_name, "today"))
                    else:
                        maintenance_dates.append((part_name, "in {} days".format(days_until_maint)))
                except ZeroDivisionError:
                    print("{} remains at {}".format(part_name, current_condition))
        return maintenance_dates



# --- TESTS ---
# The below code was used to test the Maintenance Monitor class.

# maintenance_monitor = MaintenanceMonitor()

# maintenance_monitor.add_part("Heat Pump", 99.0, 100.0, 50.0)
# maintenance_monitor.add_part("Front Motor", 100.0, 100.0, 60.0)
# maintenance_monitor.add_part("Battery", 100.0, 100.0, 50.0)
# maintenance_monitor.add_part("Rear Motor", 100.0, 100.0, 60.0)
# maintenance_monitor.add_part("Charge Port", 100.0, 100.0, 30.0)



# print(maintenance_monitor.get_current_condition("Heat Pump")) # WORKS
# print(maintenance_monitor.get_min_condition("Heat Pump")) # WORKS
# print(maintenance_monitor.list_parts()) # WORKS
# print(maintenance_monitor.parts) # WORKS

# maintenance_monitor.calc_maintenance() # WORKS
# print(maintenance_monitor.get_total_km()) # WORKS
# print(maintenance_monitor.get_total_days()) # WORKS
