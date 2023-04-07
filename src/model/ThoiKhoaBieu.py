import psycopg2, json
from flask import jsonify
import dataprovider as dp

class ThoiKhoaBieu:
    def __init__(self, gv_id=None, lop_id=None, mh_id=None, ngayhoc=None, giovao=None, giora=None, thuchanh=False, ghichu=None, phonghoc=None, title=None):
        self.gv_id = gv_id
        self.lop_id = lop_id
        self.mh_id = mh_id
        self.ngayhoc = ngayhoc
        self.giovao = giovao
        self.giora = giora
        self.thuchanh = thuchanh
        self.ghichu = ghichu
        self.phonghoc = phonghoc
        self.title = title
    
    def get_tkb_list(self, cbid):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT tkb.*, mh.mh_ten, cb_hoten FROM thoikhoabieu tkb "
            " left join monhoc mh on tkb.mh_id = mh.mh_id "
            " inner join canbo cb on cb.cb_id = tkb.cb_id  "
            " WHERE cb.cb_id = %s", (cbid, ))
            rows = cur.fetchall()
            result = []
            for row in rows:
                obj = {
                    "title": row[10],
                    "tkb_id": row[0],
                    "cb_id": row[1],
                    "lop_id": row[2],
                    "mh_ten": row[11],
                    "cb_ten": row[12],
                    "start": str(row[4])+"T"+str(row[5]),
                    "end": str(row[4])+"T"+str(row[6]),
                    "thuchanh": str(row[7]),
                    "ghichu": row[8],
                    "phonghoc": row[9]
                }
                result.append(obj)
            return result
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return None
    
    def get_tkb_full(self):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT tkb.*, mh.mh_ten, cb_hoten FROM thoikhoabieu tkb "
            " left join monhoc mh on tkb.mh_id = mh.mh_id "
            " inner join canbo cb on cb.cb_id = tkb.cb_id ")
            rows = cur.fetchall()
            result = []
            for row in rows:
                obj = {
                    "title": row[10],
                    "tkb_id": row[0],
                    "cb_id": row[1],
                    "lop_id": row[2],
                    "mh_ten": row[11],
                    "cb_ten": row[12],
                    "start": str(row[4])+"T"+str(row[5]),
                    "end": str(row[4])+"T"+str(row[6]),
                    "thuchanh": str(row[7]),
                    "ghichu": row[8],
                    "phonghoc": row[9]
                }
                result.append(obj)
            return result
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return None
    
    def insert_data(self, cb_id, lop_id, mh_id, ngayhoc, giovao, giora, thuchanh, ghichu, phonghoc, title):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute(
            "INSERT INTO public.thoikhoabieu (cb_id, lop_id, mh_id, ngayhoc, giovao, giora, thuchanh, ghichu, phonghoc, title) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (cb_id, lop_id, mh_id, ngayhoc, giovao, giora, thuchanh, ghichu, phonghoc, title)
            )
            conn.commit()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()

    




