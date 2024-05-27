import traci

class TrafficController:
    TOP    = 0
    RIGHT  = 1
    BOTTOM = 2
    LEFT   = 3
    def __init__(self):
        self.sumoBin = '/home/linuxbrew/.linuxbrew/bin/sumo-gui'
        self.sumoCmd = [self.sumoBin, '-c', 'handmade.sumocfg',
                        '--delay', '100']
        self.traffic_light_id = "center_traffic_light"
        traci.start(self.sumoCmd)

    def get_lane_vehicle_counts(self):
        lanes = {}
        lane_ids = [lane_id for lane_id in traci.lane.getIDList() if "to_center" in lane_id]
        for lane_id in lane_ids:
            lanes[lane_id] = traci.lane.getLastStepHaltingNumber(lane_id)
        return lanes

    def get_max_vehicle_lane(self, lanes):
        key = list(lanes.keys())[0]
        max_lane = {key: lanes[key]}
        for key in lanes.keys():
            if max_lane[list(max_lane.keys())[0]] < lanes[key]:
                max_lane = {key: lanes[key]}
        return max_lane

    def empty_max_vehicle_lane(self, lane_and_number, step):
        lane = list(lane_and_number.keys())[0]

        NS = 4
        laneTOP    = 'r' * NS
        laneRIGHT  = 'r' * NS
        laneBOTTOM = 'r' * NS
        laneLEFT   = 'r' * NS

        if "left" in lane:
            laneTOP    = 'r' * NS
            laneRIGHT  = 'r' * NS
            laneBOTTOM = 'r' * NS
            laneLEFT   = 'G' * NS
        elif "right" in lane:
            laneTOP    = 'r' * NS
            laneRIGHT  = 'G' * NS
            laneBOTTOM = 'r' * NS
            laneLEFT   = 'r' * NS
        elif "top" in lane:
            laneTOP    = 'G' * NS
            laneRIGHT  = 'r' * NS
            laneBOTTOM = 'r' * NS
            laneLEFT   = 'r' * NS
        elif "bottom" in lane:
            laneTOP    = 'r' * NS
            laneRIGHT  = 'r' * NS
            laneBOTTOM = 'G' * NS
            laneLEFT   = 'r' * NS

        traffic_program = f"{laneTOP}{laneRIGHT}{laneBOTTOM}{laneLEFT}"
        # print(traffic_program)
        try:
            traci.trafficlight.setRedYellowGreenState(self.traffic_light_id, traffic_program)
        except:
            # print(traffic_program)
            exit(0)
        while traci.lane.getLastStepHaltingNumber(lane) > 0:
            traci.simulationStep()
            step += 1
        return step

    def run(self, duration=1000):
        step = 0
        while step < duration:
            traci.simulationStep()
            if step > 50:
                lane_vehicle = self.get_lane_vehicle_counts()
                max_lane = self.get_max_vehicle_lane(lane_vehicle)
                step = self.empty_max_vehicle_lane(max_lane, step)
            step += 1

tc = TrafficController()
tc.run(1000)
traci.close()
print("Simulation finished.")