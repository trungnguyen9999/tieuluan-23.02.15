import psycopg2, json
from flask import jsonify
import dataprovider as dp

class ThoiKhoaBieu:
    def __init__(self, gv_id=None, lop_id=None, mh_id=None, ngayhoc=None, giovao=None, giora=None, thuchanh=False, ghichu=None, phonghoc=None):
        self.tkb_id = None
        self.gv_id = gv_id
        self.lop_id = lop_id
        self.mh_id = mh_id
        self.ngayhoc = ngayhoc
        self.giovao = giovao
        self.giora = giora
        self.thuchanh = thuchanh
        self.ghichu = ghichu
        self.phonghoc = phonghoc
    
    def get_tkb_list(self, cbid):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            query = "SELECT * FROM public.thoikhoabieu WHERE cb_id = %s"
            cur.execute(query, (cbid, ))
            rows = cur.fetchall()
            result = []
            for row in rows:
                obj = {
                    "title": row[10],
                    "tkb_id": row[0],
                    "cb_id": row[1],
                    "lop_id": row[2],
                    "mh_id": row[3],
                    "start": str(row[4])+"T"+str(row[5]),
                    "end": str(row[4])+"T"+str(row[6]),
                    "thuchanh": str(row[7]),
                    "ghichu": row[8],
                    "phonghoc": row[9]
                }
                result.append(obj)
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return result