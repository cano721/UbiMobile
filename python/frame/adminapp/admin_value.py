class Parking:
    def __init__(self, p_id, u_id, p_name, p_addr, p_cap):
        self.p_id = p_id;
        self.u_id = u_id;
        self.p_name = p_name;
        self.p_addr = p_addr;
        self.p_cap = p_cap

    def __str__(self):
        return str(self.p_id) + ' ' + self.u_id + ' ' + self.p_name + ' ' + self.p_addr + ' ' + str(self.p_cap) + ' ';