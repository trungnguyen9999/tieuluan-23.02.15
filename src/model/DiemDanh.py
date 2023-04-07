from database import db

class DiemDanh(db.Model):
    __tablename__ = 'diemdanh'
    dd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sv_id = db.Column(db.Integer, nullable=False)
    tkb_id = db.Column(db.Integer, nullable=False)
    thoigiandiemdanh = db.Column(db.Date, nullable=False)
    trangthai = db.Column(db.Integer, nullable=False)
    ghichu = db.Column(db.Text, nullable=False)
    hinhthuc = db.Column(db.Integer, nullable=False)
    dd_giovao = db.Column(db.Boolean, nullable=False )

    @staticmethod
    def save_diemdanh(dd_id, sv_id, tkb_id, thoigiandiemdanh, trangthai, ghichu, hinhthuc, dd_giovao):
        dd = DiemDanh.query.filter_by(dd_id=dd_id).first() or DiemDanh()
        dd.dd_id = dd_id
        dd.sv_id = sv_id
        dd.tkb_id = tkb_id
        dd.thoigiandiemdanh = thoigiandiemdanh
        dd.trangthai = trangthai
        dd.ghichu = ghichu
        dd.hinhthuc = hinhthuc
        dd.dd_giovao = dd_giovao
        db.session.add(dd)  
        db.session.commit()