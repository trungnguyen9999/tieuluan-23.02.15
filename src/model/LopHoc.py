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


    def get_lophoc_list(cbmaso):
            query = "SELECT distinct lh.* FROM public.lophoc lh \
                INNER JOIN thoikhoabieu tkb USING (lop_id) \
                INNER JOIN canbo cb ON tkb.cb_id = cb.cb_id \
                WHERE cb_maso = :cb_maso"
            params = {'cb_maso': cbmaso}
            result = db.session.execute(query, params)
            return result