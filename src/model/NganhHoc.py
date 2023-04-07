from database import db

class NganhHoc(db.Model):
    __tablename__ = 'nganhhoc'
    nh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nh_ma = db.Column(db.String(20), nullable=False)
    nh_ten = db.Column(db.Text, nullable=False)
    khoa_id = db.Column(db.Integer, nullable=False)


    def get_nganhhoc_list():
        nhs = NganhHoc.query.order_by(NganhHoc.nh_id.desc()).all()
        return nhs

    @staticmethod
    def save_nganhhoc(nh_id, nh_ma, nh_ten, khoa_id):
        print("---------- Saving khoa -------------")
        existing_nganhhoc = NganhHoc.query.filter_by(nh_ma=nh_ma).first()
        if existing_nganhhoc and (str(existing_nganhhoc.nh_id) != str(nh_id)):
            existing_nganhhoc.nh_id = nh_id
            existing_nganhhoc.nh_ma = nh_ma
            existing_nganhhoc.nh_ten = nh_ten
            existing_nganhhoc.khoa_id = khoa_id
            db.session.commit()
        else:
            print("có thể saved")
            nh = NganhHoc.query.filter_by(nh_id = nh_id).first() or NganhHoc()
            nh.nh_id = nh_id
            nh.nh_ma = nh_ma
            nh.nh_ten = nh_ten
            nh.khoa_id = khoa_id
            db.session.add(nh)  
            db.session.commit()