from database import db

class MonHoc(db.Model):
    __tablename__ = 'monhoc'

    mh_id = db.Column(db.Integer, primary_key=True)
    mh_maso = db.Column(db.String(20), nullable=False)
    mh_ten = db.Column(db.Text, nullable=False)
    mh_sotinchi = db.Column(db.Integer, nullable=False)
    mh_lythuyet = db.Column(db.Integer, nullable=False)
    mh_thuchanh = db.Column(db.Integer, nullable=False)