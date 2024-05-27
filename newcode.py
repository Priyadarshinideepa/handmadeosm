import traci
import os
import sys

def start_sumo():
    sumoBinary = "sumo"  # or "sumo-gui" for the graphical interface
    sumoCmd = [sumoBinary, "-c", "simple.sumocfg"]
    traci.start(sumoCmd)

def get_lane_vehicle_count():
    lane_vehicle_count = {}
    lane_ids = traci.lane.getIDList()
    for lane_id in lane_ids:
        lane_vehicle_count[lane_id] = traci.lane.getLastStepVehicleNumber(lane_id)
    return lane_vehicle_count

def set_traffic_light(lane_vehicle_count):
    max_lane = max(lane_vehicle_count, key=lane_vehicle_count.get)
    tls_id = traci.trafficlight.getIDList()[0]  # assuming one traffic light

    # Assuming a simple traffic light program with green phases for each lane
    current_program = traci.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)[0]
    green_phases = [phase for phase in current_program.phases if 'g' in phase.state.lower()]
    
    for phase in green_phases:
        if max_lane in phase.state:
            traci.trafficlight.setPhase(tls_id, green_phases.index(phase))
            break

def run_simulation(duration):
    step = 0
    while step < duration:
        traci.simulationStep()
        lane_vehicle_count = get_lane_vehicle_count()
        set_traffic_light(lane_vehicle_count)
        step += 1
    traci.close()

if __name__ == "__main__":
    if 'SUMO_HOME' not in os.environ:
        sys.exit("please declare environment variable 'SUMO_HOME'")
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    
    start_sumo()
    
    simulation_duration = 1000  # steps
    run_simulation(simulation_duration)
    
    print("Simulation finished.")
