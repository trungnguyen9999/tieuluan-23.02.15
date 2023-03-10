import psycopg2
import dataprovider as dp

class MonHoc:
    def __init__(self,  mh_maso=None, mh_ten=None, mh_sotinchi=None, mh_lythuyet=None, mh_thuchanh=None):
        self.mh_maso = mh_maso
        self.mh_ten = mh_ten
        self.mh_sotinchi = mh_sotinchi
        self.mh_lythuyet = mh_lythuyet
        self.mh_thuchanh = mh_thuchanh

    def get_monhoc_list(self, limit, offset):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM public.monhoc LIMIT %s OFFSET %s", (limit, offset))
            rows = cur.fetchall()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return rows
    
    def get_canbo_by_maso(self, mh_maso):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            query = "Select mh_id, mh_maso, mh_ten, mh_sotinchi, mh_lythuyet, mh_thuchanh from monhoc where mh_maso = %s"
            cur.execute(query, (mh_maso, ))
            monhoc = cur.fetchone()
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()
        return monhoc
    
    def create(self):
        try:
            conn = dp.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO public.monhoc (mh_maso, mh_ten, mh_sotinchi, mh_lythuyet, mh_thuchanh) \
                        VALUES (%s, %s, %s, %s, %s)", (self.mh_maso, self.mh_ten, self.mh_sotinchi, self.mh_lythuyet, self.mh_thuchanh))
            conn.commit()
            cur.close()
            return         
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        
    def checkExitByMaMon(self):
        try:
            conn = dp.connect()
            cur = conn.cursor()
            cur.execute("SELECT EXISTS (SELECT 1 FROM monhoc WHERE mh_maso = %s);", (self.mh_maso,))
            result = cur.fetchone()[0]
            conn.commit()
            cur.close()
            return result
            
        except Exception as e:
            print(e)
            conn.rollback()
            return False
        
        
    def update(self, mh_id):
        try:
            conn = dp.connect()
            cur = conn.cursor()
            cur.execute("UPDATE public.monhoc SET mh_maso = %s, mh_ten = %s, mh_sotinchi = %s, mh_lythuyet = %s, mh_thuchanh = %s WHERE mh_id = %s", (self.mh_maso, self.mh_ten, self.mh_sotinchi, self.mh_lythuyet, self.mh_thuchanh))
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print(e)
            self
            
    def delete(self):
        conn = dp.connect()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM public.monhoc WHERE mh_id = %s", (self.mh_id))
            conn.commit()
            print("Deleted successfully!")
        except psycopg2.Error as e:
            conn.rollback()
            print("Error deleting row: ", e)
        finally:
            cur.close()
            conn.close()