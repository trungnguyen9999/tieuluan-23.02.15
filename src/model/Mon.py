import psycopg2

class Khoa:
    def __init__(self, khoa_ma, khoa_ten):
        self.khoa_id = None
        self.khoa_ma = khoa_ma
        self.khoa_ten = khoa_ten