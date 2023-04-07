from database import db

class CauHinh(db.Model):
    __tablename__ = 'cauhinh'
    ch_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cb_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Text, nullable=False)

@staticmethod
def get_cauhinh(cbId):
    cauhinh = CauHinh.query.filter_by(cb_id=cbId).first()
    if(cauhinh == None):
        cauhinh = CauHinh()
    return cauhinh

@staticmethod
def save_cauhinh(value):
    print("---------- Saving cauhinh -------------")
    if(value['cbid'] == ''):
        id = -1
    else:
        id = int(value['cbid'])
    existing_ch_id = CauHinh.query.filter_by(cb_id=id).first()

    if existing_ch_id:
        existing_ch_id.cb_id = int(value['cbid'])
        del value['chid']
        del value['cbid']
        existing_ch_id.value = str(value)
        db.session.commit()
    else:
        print("có thể saved")
        cauhinh = CauHinh.query.filter_by(ch_id = -1).first() or CauHinh()
        cauhinh.cb_id = int(value['cbid'])
        del value['chid']
        del value['cbid']
        cauhinh.value = str(value)
        print(cauhinh)
        db.session.add(cauhinh)  
        db.session.commit()