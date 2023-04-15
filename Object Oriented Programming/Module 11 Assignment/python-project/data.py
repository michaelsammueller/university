# This file includes all navigational data used by the path finding algorithm deployed in the routeplanner.py file.

# Charging Stations
charging_stations = ["The Pearl", "Doha Festival City", "Mall of Qatar", "Aspire"]


# Locations and how they are connected to each other, i.e. the distances between them:
graph = {}

graph["The Pearl"] = {}
graph["The Pearl"]["Landmark Mall"] = 13
graph["The Pearl"]["Doha Festival City"] = 17
graph["The Pearl"]["City Center"] = 9

graph["Landmark Mall"] = {}
graph["Landmark Mall"]["The Pearl"] = 13
graph["Landmark Mall"]["Doha Festival City"] = 8
graph["Landmark Mall"]["Souq Waqif"] = 11
graph["Landmark Mall"]["City Center"] = 10
graph["Landmark Mall"]["Aspire"] = 13

graph["Doha Festival City"] = {}
graph["Doha Festival City"]["The Pearl"] = 17
graph["Doha Festival City"]["Landmark Mall"] = 8
graph["Doha Festival City"]["Mall of Qatar"] = 20

graph["Mall of Qatar"] = {}
graph["Mall of Qatar"]["Doha Festival City"] = 20
graph["Mall of Qatar"]["Aspire"] = 19

graph["Corniche"] = {}
graph["Corniche"]["Souq Waqif"] = 5
graph["Corniche"]["Doha Exhibition Center"] = 3

graph["Souq Waqif"] = {}
graph["Souq Waqif"]["Landmark Mall"] = 11
graph["Souq Waqif"]["Corniche"] = 5
graph["Souq Waqif"]["Aspire"] = 11

graph["City Center"] = {}
graph["City Center"]["The Pearl"] = 9
graph["City Center"]["Landmark Mall"] = 10
graph["City Center"]["Doha Exhibition Center"] = 1

graph["Doha Exhibition Center"] = {}
graph["Doha Exhibition Center"]["Corniche"] = 3
graph["Doha Exhibition Center"]["City Center"] = 1

graph["Aspire"] = {}
graph["Aspire"]["Landmark Mall"] = 13
graph["Aspire"]["Mall of Qatar"] = 19
graph["Aspire"]["Souq Waqif"] = 11
