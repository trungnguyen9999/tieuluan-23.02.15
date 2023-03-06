import psycopg2
import dataprovider as dp

class CanBo:
    def __init__(self, cb_maso=None, cb_matkhau=None, cb_hoten=None, cb_ngaysinh=None, cb_diachi=None, 
                 cb_email=None, cb_dienthoai=None, cb_id_tao=None, cb_ngaytao=None, cb_quyentruycap=0, cb_trangthai=False):
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
    
    
    def get_canbo_list(self, limit, offset):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT cb_id, cb_maso, cb_hoten, cb_ngaysinh, cb_email, cb_dienthoai, cb_diachi, cb_ngaytao, cb_quyentruycap, cb_trangthai, cb_hinh \
                FROM public.canbo LIMIT %s OFFSET %s", (limit, offset))
            rows = cur.fetchall()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return rows
            
    def get_canbo_by_maso(self, cb_maso):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            query = "Select cb_id, cb_maso, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_ngaytao, cb_hinh, cb_quyentruycap \
                from canbo where cb_maso = %s"
            cur.execute(query, (cb_maso, ))
            canbo = cur.fetchone()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return canbo
    
    def create(self):
        try:
            conn = dp.connect()
            cur = self.conn.cursor()
            cur.execute("INSERT INTO public.canbo (cb_maso, cb_matkhau, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_id_tao, cb_ngaytao, cb_quyentruycap, cb_trangthai) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai))
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        
    def update(self, cb_id):
        try:
            conn = dp.connect()
            cur = conn.cursor()
            cur.execute("UPDATE public.canbo SET cb_maso = %s, cb_matkhau = %s, cb_hoten = %s, cb_ngaysinh = %s, cb_diachi = %s, cb_email = %s, cb_dienthoai = %s, cb_id_tao = %s, cb_ngaytao = %s, cb_quyentruycap = %s, cb_trangthai = %s, cb_hinh = %s WHERE cb_id = %s", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai, self.cb_hinh, cb_id))
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            self
            
    def delete(self):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM public.canbo WHERE cb_id=%s", (self.cb_id,))
            conn.commit()
            print("Deleted successfully!")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error deleting row: ", e)
        finally:
            cur.close()
            conn.close()
