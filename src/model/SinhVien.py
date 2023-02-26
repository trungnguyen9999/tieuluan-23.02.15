class SinhVien:
    def __init__(self, sv_id, sv_maso, sv_hoten, sv_ngaysinh, sv_diachi, sv_email, sv_dienthoai, lop_id, sv_conhoc=True, sv_hinh=None):
        self.sv_id = sv_id
        self.sv_maso = sv_maso
        self.sv_hoten = sv_hoten
        self.sv_ngaysinh = sv_ngaysinh
        self.sv_diachi = sv_diachi
        self.sv_email = sv_email
        self.sv_dienthoai = sv_dienthoai
        self.lop_id = lop_id
        self.sv_conhoc = sv_conhoc
        self.sv_hinh = sv_hinh