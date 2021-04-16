class Parking_floor:
    def __init__(self, p_id, pf_floor,pf_space,pf_data):
        self.p_id = p_id;
        self.pf_floor = pf_floor;
        self.pf_space = pf_space;
        self.pf_data = pf_data;

    def __str__(self):
        return str(self.p_id) + ' ' + str(self.pf_floor) + ' ' + str(self.pf_space) + ' ' + str(self.pf_data) + ' ';