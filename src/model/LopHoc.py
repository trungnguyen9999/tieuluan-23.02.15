from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('postgresql://postges:1234567@localhost:5432/db_diemdanhsinhvien')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class LopHoc(Base):
    __tablename__ = 'lophoc'
    lop_id = Column(Integer, primary_key=True)
    lop_maso = Column(String(15))
    lop_ten = Column(String(15))
    lop_soluong_sv = Column(Integer)
    lop_convan = Column(Integer)
    nh_id = Column(Integer)
    nienkhoa = Column(Integer)
    
    def __init__(self, lop_maso, lop_ten, lop_soluong_sv, lop_convan, nh_id, nienkhoa):
        self.lop_maso = lop_maso
        self.lop_ten = lop_ten
        self.lop_soluong_sv = lop_soluong_sv
        self.lop_convan = lop_convan
        self.nh_id = nh_id
        self.nienkhoa = nienkhoa
        
    @classmethod
    def get_all(cls):
        return session.query(cls).all()
    
    def create(self):
        # Thêm một sinh viên mới
        new_lop = LopHoc(lop_maso ='dc1896', lop_ten='DC1896N1', soluong_sv = 200, lop_covan = 1, nh_id = 1, nienkhoa = 1,)
        session.add(new_lop)
        session.commit()
    
    # def __init__(self, lop_maso, lop_ten, lop_soluong_sv, lop_convan, nh_id, nienkhoa):
    #     self.lop_id = None
    #     self.lop_maso = lop_maso
    #     self.lop_ten = lop_ten
    #     self.lop_soluong_sv = lop_soluong_sv
    #     self.lop_convan = lop_convan
    #     self.nh_id = nh_id
    #     self.nienkhoa = nienkhoa