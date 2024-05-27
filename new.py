import traci
import os
import random

# Function to start the SUMO simulation
def start_sumo(config_file):
    sumo_cmd = ['sumo', '-c', config_file, '--start', '--quit-on-end']
    traci.start(sumo_cmd)

# Function to control the number of vehicles spawned
def control_vehicle_spawn():
    # Define route ID and flow
    route_id = "route0"  # Route ID for the cross-shaped network
    flow = random.randint(50, 100)  # Randomly choose the flow rate
    traci.flow.add(route_id, flow, 0, 3600, vehsPerHour=True)

# Function to control the traffic light timing based on the number of vehicles
def control_traffic_light():
    # Get the traffic light ID
    traffic_light_id = "center_traffic_light"

    # Get the number of vehicles on each lane
    lanes = ["lane_north", "lane_south", "lane_east", "lane_west"]
    num_vehicles_on_lanes = {lane: traci.lane.getLastStepVehicleNumber(lane) for lane in lanes}

    # Calculate the proportion of vehicles on each lane
    total_vehicles = sum(num_vehicles_on_lanes.values())
    proportions = {lane: num_vehicles / total_vehicles for lane, num_vehicles in num_vehicles_on_lanes.items()}

    # Calculate the new traffic light timings based on proportions
    timings = {lane: int(proportion * 100) for lane, proportion in proportions.items()}

    # Construct the new traffic light state
    new_state = ""
    for lane in lanes:
        if timings[lane] > 0:
            new_state += "G"
        else:
            new_state += "r"
        timings[lane] -= 1

    # Set the new state for the traffic light
    traci.trafficlight.setRedYellowGreenState(traffic_light_id, new_state)

# Main function
def main(config_file):
    # Start the SUMO simulation
    start_sumo(config_file)

    try:
        # Main simulation loop
        while traci.simulation.getMinExpectedNumber() > 0:
            # Advance the simulation by one step
            traci.simulationStep()

            # Control the number of vehicles spawned
            control_vehicle_spawn()

            # Control the traffic light timing
            control_traffic_light()

    finally:
        # Disconnect from the SUMO simulation
        traci.close()

# Main entry point
if __name__ == "__main__":
    # Specify the SUMO configuration file
    SUMO_CONFIG_FILE = "handmade.sumocfg"

    # Set SUMO_HOME environment variable (replace with your SUMO installation path)
    os.environ['SUMO_HOME'] = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'

    # Import TraCI
    import traci

    # Run the simulation
    main(SUMO_CONFIG_FILE)
