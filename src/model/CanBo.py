import psycopg2

class CanBo:
    def __init__(self, cb_maso, cb_matkhau, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_id_tao, cb_ngaytao, cb_quyentruycap=0, cb_trangthai=True, cb_hinh=None):
        self.cb_maso = cb_maso
        self.cb_matkhau = cb_matkhau
        self.cb_hoten = cb_hoten
        self.cb_ngaysinh = cb_ngaysinh
        self.cb_diachi = cb_diachi
        self.cb_email = cb_email
        self.cb_dienthoai = cb_dienthoai
        self.cb_id_tao = cb_id_tao
        self.cb_ngaytao = cb_ngaytao
        self.cb_quyentruycap = cb_quyentruycap
        self.cb_trangthai = cb_trangthai
        self.cb_hinh = cb_hinh
        self.conn = psycopg2.connect("dbname=mydatabase user=postgres password=123456")
    
    
    def get_canbo_list(self, limit, offset):
        cur = self.conn.cursor()
        try:
            cur.execute("SELECT * FROM public.canbo LIMIT %s OFFSET %s", (limit, offset))
            rows = cur.fetchall()
            print("Can Bo List:")
            for row in rows:
                print(row)
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            self.conn.close()
            
    def create(self):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO public.canbo (cb_maso, cb_matkhau, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_id_tao, cb_ngaytao, cb_quyentruycap, cb_trangthai, cb_hinh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai, self.cb_hinh))
            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        
    def update(self, cb_id):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE public.canbo SET cb_maso = %s, cb_matkhau = %s, cb_hoten = %s, cb_ngaysinh = %s, cb_diachi = %s, cb_email = %s, cb_dienthoai = %s, cb_id_tao = %s, cb_ngaytao = %s, cb_quyentruycap = %s, cb_trangthai = %s, cb_hinh = %s WHERE cb_id = %s", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai, self.cb_hinh, cb_id))
            self.conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            self
            
    def delete(self):
        cur = self.conn.cursor()
        try:
            cur.execute("DELETE FROM public.canbo WHERE cb_id=%s", (self.cb_id,))
            self.conn.commit()
            print("Deleted successfully!")
        except psycopg2.Error as e:
            self.conn.rollback()
            print("Error deleting row: ", e)
        finally:
            cur.close()
            self.conn.close()
