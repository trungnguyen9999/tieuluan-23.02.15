from database import db

class Khoa(db.Model):
    __tablename__ = 'khoa'
    khoa_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    khoa_ma = db.Column(db.String(20), nullable=False)
    khoa_ten = db.Column(db.Text, nullable=False)

    @staticmethod
    def get_khoa_list():
        khoas = Khoa.query.order_by(Khoa.khoa_id.desc()).all()
        return khoas
    
    @staticmethod
    def save_khoa(khoa_id, khoa_ma, khoa_ten):
        print("---------- Saving khoa -------------")
        existing_khoa = Khoa.query.filter_by(khoa_ma=khoa_ma).first()
        if existing_khoa and (str(existing_khoa.khoa_id) != str(khoa_id)):
            existing_khoa.khoa_id = khoa_id
            existing_khoa.khoa_ma = khoa_ma
            existing_khoa.khoa_ten = khoa_ten
            db.session.commit()
        else:
            print("có thể saved")
            khoa = Khoa.query.filter_by(khoa_id = khoa_id).first() or Khoa()
            khoa.khoa_id = khoa_id
            khoa.khoa_ma = khoa_ma
            khoa.khoa_ten = khoa_ten
            db.session.add(khoa)  
            db.session.commit()
            
    @staticmethod
    def checkExitByKhoaMa(khoa_ma):
        return Khoa.query.filter_by(Khoa_ma=khoa_ma).count() > 0   
     
    @staticmethod
    def checkExitByKhoaTen(khoa_ten):
        return Khoa.query.filter_by(Khoa_ten=khoa_ten).count() > 0
    
    @staticmethod  
    def delete(khoa_id):
        khoa = Khoa.query.filter_by(khoa_id=khoa_id).first()
        if khoa:
            db.session.delete(khoa)
            db.session.commit()
            return True
        else:
            return False


            