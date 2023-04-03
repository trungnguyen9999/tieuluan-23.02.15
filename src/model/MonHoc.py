from database import db

class MonHoc(db.Model):
    __tablename__ = 'monhoc'

    mh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mh_maso = db.Column(db.String(20), nullable=False)
    mh_ten = db.Column(db.Text, nullable=False)
    mh_sotinchi = db.Column(db.Integer, nullable=False)
    mh_lythuyet = db.Column(db.Integer, nullable=False)
    mh_thuchanh = db.Column(db.Integer, nullable=False)
        
    @staticmethod
    def get_monhoc():
        monhocs = MonHoc.query.order_by(MonHoc.mh_id.desc()).all()
        return monhocs
    
    @staticmethod
    def save_monhoc(mh_id, mh_maso, mh_ten, mh_sotinchi,mh_lythuyet,mh_thuchanh):
        print("---------- Saving monhoc -------------")
        existing_monhoc = MonHoc.query.filter_by(mh_maso=mh_maso).first()
        
        # Nếu tồn tại monhoc khác có cùng maso, trả về thông báo lỗi
        if existing_monhoc and (str(existing_monhoc.mh_id) != str(mh_id)):
            return None
        else:
            print("có thể saved")
            monhoc = MonHoc.query.filter_by(mh_id = mh_id).first() or MonHoc()
            monhoc.mh_id = mh_id
            monhoc.mh_maso = mh_maso
            monhoc.mh_ten = mh_ten
            monhoc.mh_sotinchi = mh_sotinchi
            monhoc.mh_lythuyet = mh_lythuyet
            monhoc.mh_thuchanh = mh_thuchanh
            db.session.add(monhoc)  
            db.session.commit()
    
    @staticmethod
    def check_mh_maso_exits(mh_ma):
        return MonHoc.query.filter_by(mh_ma=mh_ma).count() > 0
    
    
    @staticmethod
    def get_monhoc_by_id(mh_id):
        monhoc = db.session.query(MonHoc).get(mh_id)
        return monhoc
    
    @staticmethod
    def delete_monhoc_by_id(mh_id):
        monhoc = MonHoc.query.filter_by(mh_id=mh_id).first()
        if monhoc:
            db.session.delete(monhoc)
            db.session.commit()
            return True
        else:
            return False
    
    