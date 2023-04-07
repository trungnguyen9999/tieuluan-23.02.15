from database import db

class CanBo(db.Model):
    __tablename__ = 'canbo'
    cb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cb_maso = db.Column(db.String(20), nullable=False)
    cb_matkhau = db.Column(db.Text, nullable=False)
    cb_hoten = db.Column(db.Text, nullable=False)
    cb_ngaysinh = db.Column(db.Date, nullable=False)
    cb_diachi = db.Column(db.Text, nullable=False)
    cb_email = db.Column(db.String(100), nullable=True)
    cb_dienthoai = db.Column(db.String(10), nullable=True)
    cb_id_tao = db.Column(db.Integer, nullable=False)
    cb_ngaytao = db.Column(db.Date, nullable=False)
    cb_quyentruycap = db.Column(db.Integer, nullable=True)
    cb_trangthai = db.Column(db.Boolean, nullable=True)
    cb_hinh = db.Column(db.Text, nullable=True)
    
    @staticmethod
    def get_canbo_list():
        canbo = CanBo.query.order_by(CanBo.cb_id.asc()).all()
        if(canbo == None):
            canbo = CanBo()
        return canbo
    @staticmethod    
    def get_canbo_by_maso(cb_maso):
        canbo = CanBo.query.filter_by(cb_maso=cb_maso).first()
        if(canbo == None):
            canbo = CanBo()
        return canbo
    
    @staticmethod    
    def get_canbo_id_by_maso(cb_maso):
        canbo = CanBo.query.filter_by(cb_maso=cb_maso).first()
        return canbo.cb_id
    
    @staticmethod
    def save_canbo(cb_id, cb_maso, cb_matkhau, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_id_tao, cb_ngaytao, cb_quyentruycap, cb_trangthai, cb_hinh):
        print("---------- Saving canbo -------------")
        existing_cb_id = CanBo.query.filter_by(cb_id=cb_id).first()

        if existing_cb_id:
            existing_cb_id.cb_id = cb_id
            existing_cb_id.cb_maso = cb_maso
            existing_cb_id.cb_hoten = cb_hoten
            existing_cb_id.cb_ngaysinh = cb_ngaysinh
            existing_cb_id.cb_diachi = cb_diachi
            existing_cb_id.cb_email = cb_email
            existing_cb_id.cb_dienthoai = cb_dienthoai
            existing_cb_id.cb_id_tao = cb_id_tao
            existing_cb_id.cb_ngaytao = cb_ngaytao
            existing_cb_id.cb_quyentruycap = cb_quyentruycap
            existing_cb_id.cb_trangthai = cb_trangthai
            existing_cb_id.cb_hinh = cb_hinh
            db.session.commit()
        else:
            print("có thể saved")
            canbo = CanBo.query.filter_by(cb_id = -1).first() or CanBo()
            canbo.cb_maso = cb_maso
            canbo.cb_hoten = cb_hoten
            canbo.cb_matkhau = cb_matkhau
            canbo.cb_ngaysinh = cb_ngaysinh
            canbo.cb_diachi = cb_diachi
            canbo.cb_email = cb_email
            canbo.cb_dienthoai = cb_dienthoai
            canbo.cb_id_tao = cb_id_tao
            canbo.cb_ngaytao = cb_ngaytao
            canbo.cb_quyentruycap = cb_quyentruycap
            canbo.cb_trangthai = cb_trangthai
            canbo.cb_hinh = cb_hinh
            db.session.add(canbo)  
            db.session.commit()

