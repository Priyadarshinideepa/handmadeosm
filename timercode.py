import time
import traci
import matplotlib.pyplot as plt

# Define the SUMO binary and command
sumoBin = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'
sumoCmd = [sumoBin, '-c', 'handmade.sumocfg', '--start', '--delay', '100', '-Q']

# Start SUMO
traci.start(sumoCmd)

# Get traffic light IDs
tls_ids = traci.trafficlight.getIDList()

# Define the traffic light and number of phases
traffic_light_id = "center_traffic_light"
NS = 4
THRESHOLD = 5  # Define a threshold for comparison

# Initialize variables for data collection
step = 0
car_passed_time = []  # List to store simulation time when a car passes
time_given = []       # List to store current phase time

# Main simulation loop
while step < 1000:
    # Print lane IDs and the number of waiting vehicles after 50 simulation steps
    if step > 50:
        lane_ids = traci.lane.getIDList()
        waiting_vehicles = {lane_id: traci.lane.getLastStepHaltingNumber(lane_id) for lane_id in lane_ids}
        import traci
import matplotlib.pyplot as plt
import traci
import matplotlib.pyplot as plt

# Define the SUMO binary and command
sumoBin = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'
sumoCmd = [sumoBin, '-c', 'handmade.sumocfg', '--start', '--delay', '100', '-Q']

# Start SUMO
traci.start(sumoCmd)

# Define the traffic light and threshold
traffic_light_id = "center_traffic_light"
lane_ids = ["lane_1", "lane_2", "lane_3", "lane_4"]  # Example lane IDs, replace with actual IDs

# Initialize variables for data collection
step = 0
stationary_vehicles = {lane_id: [] for lane_id in lane_ids}  # Dictionary to track stationary vehicles

# Main simulation loop
while step < 1000:
    # Advance the simulation
    traci.simulationStep()
    
    if step > 50:
        # Get the number of waiting vehicles for each lane
        waiting_vehicles = {lane_id: traci.lane.getLastStepHaltingNumber(lane_id) for lane_id in lane_ids}

        # Identify the lane with the most waiting vehicles
        max_waiting_lane = max(waiting_vehicles, key=waiting_vehicles.get)
        
        # Set traffic lights: green for the lane with the most vehicles, red for others
        tls_state = ["r"] * len(lane_ids)
        max_waiting_index = lane_ids.index(max_waiting_lane)
        tls_state[max_waiting_index] = "G"
        new_tls_state = "".join(tls_state)
        traci.trafficlight.setRedYellowGreenState(traffic_light_id, new_tls_state)
        
        # Track the number of stationary vehicles in the lane with the green light
        stationary_vehicles[max_waiting_lane].append(waiting_vehicles[max_waiting_lane])

        print(f"Step: {step}, Green Lane: {max_waiting_lane}, Waiting Vehicles: {waiting_vehicles}")
    
    # Increment step counter
    step += 1

# Close SUMO simulation
traci.close()

# Plot the data
plt.figure(figsize=(10, 5))
for lane_id, data in stationary_vehicles.items():
    plt.plot(range(51, 1000), data, label=f'{lane_id} Stationary Vehicles')
plt.xlabel('Simulation Step')
plt.ylabel('Number of Stationary Vehicles')
plt.title('Stationary Vehicles in Green Light Lane')
plt.legend()
plt.grid(True)
plt.show()

import traci
import matplotlib.pyplot as plt

# Define the SUMO binary and command
sumoBin = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'
sumoCmd = [sumoBin, '-c', 'handmade.sumocfg', '--start', '--delay', '100', '-Q']

# Start SUMO
traci.start(sumoCmd)

# Define the traffic light ID and the lane IDs connected to the central traffic light
traffic_light_id = "center_traffic_light"
lane_ids = [
    "lane_1",  # North
    "lane_2",  # East
    "lane_3",  # South
    "lane_4"   # West
]

# Initialize variables for data collection
step = 0
waiting_vehicles_data = {lane_id: [] for lane_id in lane_ids}  # Dictionary to store waiting vehicles per lane

# Main simulation loop
while step < 1000:
    # Print lane IDs and the number of waiting vehicles after 50 simulation steps
    if step > 50:
        waiting_vehicles = {lane_id: traci.lane.getLastStepHaltingNumber(lane_id) for lane_id in lane_ids}
        
        # Determine which lane has the most waiting vehicles
        max_waiting_lane = max(waiting_vehicles, key=waiting_vehicles.get)
        
        # Set the traffic light state: green for the lane with the most waiting vehicles, red for others
        tls_state = ["r"] * len(lane_ids)
        green_light_index = lane_ids.index(max_waiting_lane)
        tls_state[green_light_index] = "G"
        new_tls_state = "".join(tls_state)
        traci.trafficlight.setRedYellowGreenState(traffic_light_id, new_tls_state)
        
        # Collect data for the number of vehicles staying in the rest position
        for lane_id, count in waiting_vehicles.items():
            waiting_vehicles_data[lane_id].append(count)
        
        print(f"Step: {step}, Green Lane: {max_waiting_lane}, Waiting Vehicles: {waiting_vehicles}")
    
    # Advance the simulation
    traci.simulationStep()
    
    # Increment step counter
    step += 1

# Close SUMO simulation
traci.close()

# Plot the data
plt.figure(figsize=(10, 5))
for lane_id, data in waiting_vehicles_data.items():
    plt.plot(range(len(data)), data, label=f'Waiting Vehicles in {lane_id}')

plt.xlabel('Simulation Step')
plt.ylabel('Number of Waiting Vehicles')
plt.title('Number of Waiting Vehicles in Each Lane')
plt.legend()
plt.grid(True)
plt.show()

print("traci closed")
print("traci closed")

plt.title('Simulation Data')
plt.legend()
plt.grid(True)
plt.show()

print("traci closed")

        # Calculate the total waiting vehicles
        total_waiting_vehicles = sum(waiting_vehicles.values())

        # Determine which lane should get the green light
        green_lane_id = None
        for lane_id, count in waiting_vehicles.items():
            if count > total_waiting_vehicles - count + THRESHOLD:
                green_lane_id = lane_id
                break
        
        # Control traffic lights based on the green lane
        if green_lane_id:
            green_light_index = lane_ids.index(green_lane_id)
            tls_state = ["r"] * len(lane_ids)
            tls_state[green_light_index] = "G"
            new_tls_state = "".join(tls_state)
            traci.trafficlight.setRedYellowGreenState(traffic_light_id, new_tls_state)
        else:
            # Default traffic light state if no lane exceeds the threshold
            traci.trafficlight.setRedYellowGreenState(traffic_light_id, "r" * len(lane_ids))
        
        print(f"Step: {step}, Green Lane: {green_lane_id}, Waiting Vehicles: {waiting_vehicles}")
    
    # Advance the simulation
    traci.simulationStep()
    
    # Track time taken for a car to pass
    if step % 10 == 0:  # Check every 10 steps
        car_passed_time.append(traci.simulation.getTime())

    # Track time given to traffic lights (here using step as the phase indicator)
    time_given.append(step)  # Store the current step

    # Increment step counter
    step += 1

# Close SUMO simulation
traci.close()

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(range(0, 1000, 10), car_passed_time, label='Simulation Time for Car Passing')
plt.plot(range(1000), time_given, label='Simulation Steps')
plt.xlabel('Simulation Step')
plt.ylabel('Time')
plt.title('Simulation Data')
plt.legend()
plt.grid(True)
plt.show()

print("traci closed")
