import psycopg2
import dataprovider as dp

class SinhVien:
    
    def __init__(self, sv_maso=None, sv_hoten=None, sv_ngaysinh=None, sv_diachi=None, sv_email=None, sv_dienthoai=None, lop_id=None, sv_conhoc=True, sv_hinh=None, sv_gioitinh=0):
        self.sv_id = None
        self.sv_maso = sv_maso
        self.sv_hoten = sv_hoten
        self.sv_ngaysinh = sv_ngaysinh
        self.sv_diachi = sv_diachi
        self.sv_email = sv_email
        self.sv_dienthoai = sv_dienthoai
        self.lop_id = lop_id
        self.sv_conhoc = sv_conhoc
        self.sv_hinh = sv_hinh
        self.sv_gioitinh = sv_gioitinh
    
    def get_sinhvien_list(self,lop_id):
    
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT sv_maso, sv_hoten, cast(sv_ngaysinh as text), sv_diachi, sv_email, sv_dienthoai, lh.lop_maso, coalesce(sv_hinh, ''), sv_gioitinh, sv_id \
                FROM sinhvien sv \
                INNER JOIN lophoc lh USING (lop_id)\
                where lop_id = %s", (lop_id,))
            rows = cur.fetchall()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return rows
    
    def get_sinhvien_by_id(self, svid):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            query = "SELECT sv_maso, sv_hoten, cast(sv_ngaysinh as text), sv_diachi, sv_email, sv_dienthoai, lh.lop_maso, coalesce(sv_hinh, ''), sv_gioitinh, sv_id, lh.lop_ten \
                FROM sinhvien sv \
                INNER JOIN lophoc lh USING (lop_id)\
                where sv_id = %s"
            cur.execute(query, (svid, ))
            canbo = cur.fetchone()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return canbo
    
    def create(self):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO public.sinhvien (sv_maso, sv_hoten, sv_ngaysinh, sv_diachi, sv_email, sv_dienthoai, lop_id, sv_gioitinh) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (self.sv_maso, self.sv_hoten, self.sv_ngaysinh, self.sv_diachi, self.sv_email, self.sv_dienthoai, self.lop_id, self.sv_gioitinh))
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False