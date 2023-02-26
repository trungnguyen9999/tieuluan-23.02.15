import psycopg2
class NganhHoc:
    def __init__(self, nh_id, nh_ma, nh_ten, khoa_id):
        self.nh_id = nh_id
        self.nh_ma = nh_ma
        self.nh_ten = nh_ten
        self.khoa_id = khoa_id