import psycopg2

class LopHoc:
    def __init__(self, lop_maso, lop_ten, lop_soluong_sv, lop_convan, nh_id, nienkhoa):
        self.lop_id = None
        self.lop_maso = lop_maso
        self.lop_ten = lop_ten
        self.lop_soluong_sv = lop_soluong_sv
        self.lop_convan = lop_convan
        self.nh_id = nh_id
        self.nienkhoa = nienkhoa