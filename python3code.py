import time
import traci
sumoBin = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'
sumoCmd = [ sumoBin, '-c', 'handmade.sumocfg', 
        #    '--start',
            '--delay', '100' ]

traci.start(sumoCmd)

tls_ids = traci.trafficlight.getIDList()

# Print all traffic light IDs
print("Traffic Light IDs:")
for tls_id in tls_ids:
    print("-", tls_id, traci.trafficlight.getRedYellowGreenState(tls_id))

traffic_light_id = "center_traffic_light"

route_ids = traci.route.getIDList()

# Print all route IDs

print("Route IDs:")
for route_id in route_ids:
    print("-", route_id)
else:
    print("not routes available")

NS = 4

step = 0
while step < 1000:
    if step > 50:
        lane_ids = traci.lane.getIDList()
        print(lane_ids)
        total_waiting_vehicles = 0
        for lane_id in lane_ids:
            waiting_vehicles = traci.lane.getLastStepHaltingNumber(lane_id)
            total_waiting_vehicles += waiting_vehicles
            print(waiting_vehicles, lane_id)
        time.sleep(1)
    
    traci.simulationStep()
    tls_state = traci.trafficlight.getRedYellowGreenState(traffic_light_id)
    x = step % 16
    t1 = "r" * NS
    t2 = "r" * NS
    t3 = "r" * NS
    t4 = "r" * NS
    if 0 < x < 3:
        t4 = "r" * NS
        t1 = "G" * NS
    if 4 < x < 7:
        t1 = "r" * NS
        t2 = "G" * NS
    if 8 < x < 12:
        t2 = "r" * NS
        t3 = "G" * NS
    if 13 < x < 16:
        t3 = "r" * NS
        t4 = "G" * NS
    new_tls_state = f"{t1}{t2}{t3}{t4}"
    traci.trafficlight.setRedYellowGreenState(traffic_light_id, new_tls_state)
    step += 1

traci.close()
print("traci closed")
# traci.start(sumoCmd)

# tls_id = traci.trafficlight.getIDList()

# for i in tls_id:
#     print(f"{i=}")

# while traci.simulation.getMinExpectedNumber():
#     traci.simulationStep()

#     traffic_light_id = 'J1'
#     tls_state = traci.trafficlight.getRedYellowGreenState(traffic_light_id)