import psycopg2
import dataprovider as dp
from database import db

class LopHoc(db.Model):
    __tablename__ = 'lophoc'
    lop_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lop_maso = db.Column(db.String(20), nullable=False)
    lop_ten = db.Column(db.Text, nullable=False)
    lop_soluong_sv = db.Column(db.Integer, nullable=False)
    lop_convan = db.Column(db.Integer, nullable=False)
    nh_id = db.Column(db.Integer, nullable=False)
    nienkhoa = db.Column(db.Integer, nullable=False)
    
    def __init__(self, lop_maso=None, lop_ten=None, lop_soluong_sv=None, lop_convan=None, nh_id=None, nienkhoa=None):
        self.lop_id = None
        self.lop_maso = lop_maso
        self.lop_ten = lop_ten
        self.lop_soluong_sv = lop_soluong_sv
        self.lop_convan = lop_convan
        self.nh_id = nh_id
        self.nienkhoa = nienkhoa
        
    @staticmethod
    def get_lop():
        lophocs = LopHoc.query.order_by(LopHoc.lop_id.desc()).all()
        return lophocs

    @staticmethod
    def save_lophoc(lop_id, lop_maso, lop_ten, lop_soluong_sv, lop_convan, nh_id, nienkhoa):
        print("---------- Saving lophoc -------------")
        existing_lophoc = LopHoc.query.filter_by(lop_maso=lop_maso).first()
        
        # Nếu tồn tại lophoc khác có cùng maso, trả về thông báo lỗi
        if existing_lophoc and (str(existing_lophoc.lop_id) != str(lop_id)):
            print("không thể saved")
            return None
        else:
            print("có thể saved")
            lophoc = LopHoc.query.filter_by(lop_id = lop_id).first() or LopHoc()
            lophoc.lop_id = lop_id
            lophoc.lop_maso = lop_maso
            lophoc.lop_ten = lop_ten
            lophoc.lop_soluong_sv = lop_soluong_sv
            lophoc.lop_convan = lop_convan
            lophoc.nh_id = nh_id
            lophoc.nienkhoa = nienkhoa
            db.session.add(lophoc)  
            db.session.commit()
            
    @staticmethod
    def delete_lophoc_by_id(lop_id):
        lophoc = LopHoc.query.filter_by(lop_id=lop_id).first()
        if lophoc:
            db.session.delete(lophoc)
            db.session.commit()
            return True
        else:
            return False
        
        
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