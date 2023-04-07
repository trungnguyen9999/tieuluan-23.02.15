import psycopg2
import dataprovider as dp

class LopHoc:
    def __init__(self, lop_maso=None, lop_ten=None, lop_soluong_sv=None, lop_convan=None, nh_id=None, nienkhoa=None):
        self.lop_id = None
        self.lop_maso = lop_maso
        self.lop_ten = lop_ten
        self.lop_soluong_sv = lop_soluong_sv
        self.lop_convan = lop_convan
        self.nh_id = nh_id
        self.nienkhoa = nienkhoa
        
        
    def get_lophoc_list(self, cbmaso):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            if(cbmaso != "-1"):
                query = "SELECT distinct lh.* FROM public.lophoc lh \
                    INNER JOIN thoikhoabieu tkb USING (lop_id) \
                    INNER JOIN canbo cb ON tkb.cb_id = cb.cb_id \
                    WHERE cb_maso = %s"
                cur.execute(query, (cbmaso, ))
                rows = cur.fetchall()
            else:
                query = "SELECT distinct lh.* FROM public.lophoc lh \
                    LEFT JOIN thoikhoabieu tkb USING (lop_id) \
                    LEFT JOIN canbo cb ON tkb.cb_id = cb.cb_id"
                cur.execute(query)
                rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return None
    
    def get_info_diemdanh(self, cbmaso):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            query = "SELECT tkb_id FROM public.lophoc lh \
                INNER JOIN thoikhoabieu tkb USING (lop_id) \
                INNER JOIN canbo cb ON tkb.cb_id = cb.cb_id \
                WHERE cb_maso = %s and tkb_ngayhoc = current_date and giovao <= current_time and giora >= current_time"
            cur.execute(query, (cbmaso, ))
            row = cur.fetchone()
            return row
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return None