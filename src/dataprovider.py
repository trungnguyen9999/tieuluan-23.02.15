import psycopg2
import dataprovider as dp

def connect():
    return psycopg2.connect(database="db_diemdanhsinhvien",
                            user="postgres",
                            password="1234567",
                            host="localhost", port="5432")

def login(cb_maso, cb_matkhau):
    try:
        loaitaikhoan = -1
        conn = connect()
        statement = "SELECT cb_quyentruycap from canbo WHERE cb_maso=%s AND cb_matkhau =%s and cb_trangthai;"
        cur = conn.cursor()
        query = cur.execute(statement,  (str(cb_maso), str(cb_matkhau)))
        isRecordExist = 0
        result_set = cur.fetchall()
        cur.close()
        conn.close()
        for row in result_set:
            loaitaikhoan = row[0]
            isRecordExist = 1
        if (isRecordExist == 0):
            return -1
        else:
            return loaitaikhoan
    except:
        print("Da co loi")
        
        
#START CANBO
def get_canbo_list(self, limit, offset):
    cur = self.conn.cursor()
    try:
        cur.execute("SELECT * FROM public.canbo LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        print("Can Bo List:")
        for row in rows:
            print(row)
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        self.conn.close()
        
def create(self):
    try:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO public.canbo (cb_maso, cb_matkhau, cb_hoten, cb_ngaysinh, cb_diachi, cb_email, cb_dienthoai, cb_id_tao, cb_ngaytao, cb_quyentruycap, cb_trangthai, cb_hinh) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai, self.cb_hinh))
        self.conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        self.conn.rollback()
        return False
    
def update(self, cb_id):
    try:
        cur = self.conn.cursor()
        cur.execute("UPDATE public.canbo SET cb_maso = %s, cb_matkhau = %s, cb_hoten = %s, cb_ngaysinh = %s, cb_diachi = %s, cb_email = %s, cb_dienthoai = %s, cb_id_tao = %s, cb_ngaytao = %s, cb_quyentruycap = %s, cb_trangthai = %s, cb_hinh = %s WHERE cb_id = %s", (self.cb_maso, self.cb_matkhau, self.cb_hoten, self.cb_ngaysinh, self.cb_diachi, self.cb_email, self.cb_dienthoai, self.cb_id_tao, self.cb_ngaytao, self.cb_quyentruycap, self.cb_trangthai, self.cb_hinh, cb_id))
        self.conn.commit()
        cur.close()
        return True
    except Exception as e:
        print(e)
        
def delete(self):
    cur = self.conn.cursor()
    try:
        cur.execute("DELETE FROM public.canbo WHERE cb_id=%s", (self.cb_id,))
        self.conn.commit()
        print("Deleted successfully!")
    except psycopg2.Error as e:
        self.conn.rollback()
        print("Error deleting row: ", e)
    finally:
        cur.close()
        self.conn.close()
#END CANBO

def get_timeline():
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select cb_hoten, lop_maso, giovao, giora from thoikhoabieu tkb\
            inner join canbo cb using (cb_id)\
            inner join lophoc using (lop_id)\
            where ngayhoc = current_date\
            order by ngayhoc desc, giovao desc\
            limit 10"
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None

def get_list_tkb_diemdanh(cb_id):
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select tkb_id, lop_maso || ' - ' || lop_ten, mh_maso || ' - ' || mh_ten, giovao || ' - ' || giora from  thoikhoabieu tkb\
        inner join lophoc lop on tkb.lop_id = lop.lop_id\
        inner join monhoc mh on tkb.mh_id = mh.mh_id\
        and cb_id = %s\
        and ngayhoc = current_date"
        cur.execute(query, (cb_id,))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None

def get_sinhvien_by_tkb_id(tkb_id, dd_giovao):
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select sv.sv_maso, sv.sv_hoten, dd.thoigiandiemdanh, dd.trangthai, sv.sv_id from thoikhoabieu tkb\
        inner join sinhvien sv on tkb.lop_id = sv.lop_id\
        left join diemdanh dd on tkb.tkb_id = dd.tkb_id and sv.sv_id = dd.sv_id and dd_giovao = %s\
        where tkb.tkb_id = %s"
        cur.execute(query, (dd_giovao, tkb_id))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None

def is_ins_diemdanh(sv_id):
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select (max(thoigiandiemdanh) is null \
        or ((EXTRACT(EPOCH FROM (now() - max(thoigiandiemdanh))) / 60) > 30\
        and (select (current_time > giovao and current_time < giogiua ) \
        or (current_time < giora and current_time > giogiua and now() > thoigiandiemdanh)\
        from\
        (select giovao, giovao + (giora - giovao) / 2 as giogiua, giora, thoigiandiemdanh from thoikhoabieu tkb\
        inner join sinhvien sv on sv.lop_id = tkb.lop_id\
        left join diemdanh dd on sv.sv_id = dd.sv_id\
        where ngayhoc = current_date\
        and sv.sv_id = 1) as a limit 1)))\
        from diemdanh dd\
        where sv_id = 1 and cast(thoigiandiemdanh as date) = current_date"
        cur.execute(query, (sv_id, ))
        rows = cur.fetchone()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None

def save_diemdanh(sv_id, tkb_id, thoigiandiemdanh, trangthai, ghichu, hinhthuc, dd_giovao):
    conn = dp.connect()
    cur = conn.cursor()
    #Dựa vào thời gian điểm danh và thời gian vào/ ra để xác định tkb_id
    
    try:
        query = "insert into diemdanh (sv_id, tkb_id, thoigiandiemdanh, trangthai, ghichu, hinhthuc, dd_giovao)\
            values (%s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (sv_id, tkb_id, thoigiandiemdanh, trangthai, ghichu, hinhthuc, dd_giovao))
        conn.commit()
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
        
#================================== Bảng điểm danh =============================
def get_list_tkb_diemdanh_all(cb_id):
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select tkb_id, lop_maso || ' - ' || lop_ten, mh_maso || ' - ' || mh_ten, giovao || ' - ' || giora from  thoikhoabieu tkb\
        inner join lophoc lop on tkb.lop_id = lop.lop_id\
        inner join monhoc mh on tkb.mh_id = mh.mh_id\
        and cb_id = %s"
        cur.execute(query, (cb_id,))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None

def get_column_diemdanh(lopid, monid, cbid):
    conn = dp.connect()
    cur = conn.cursor()
    try:
        query = "select tkb_id, ngayhoc from thoikhoabieu where lop_id = %s and mh_id = %s and cb_id = %s"
        cur.execute(query, (lopid, monid, cbid))
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        print("Error selecting rows: ", e)
    finally:
        cur.close()
        conn.close()
    return None


def get_data_diemdanh(lopid, l_tkbid):
    conn = dp.connect()
    cur = conn.cursor()
    print("get_data_diemdanh: lop = " + lopid + " - l_tkb = " + str(l_tkbid[0][0]))
    query = ""
    if len(l_tkbid) > 1:
        print("length > 1")
        query = "select sv_maso, sv_hoten, "
        idx = 0
        for i in l_tkbid:
            print(str(i[0]))
            query += " (select cast(thoigiandiemdanh as text) <> '' from diemdanh dd where dd.sv_id = sv.sv_id and tkb_id in (" + str(i[0]) + "))"
            idx+=1
            
            print(str(idx))
            if(idx < len(l_tkbid)):
                query += ", "
        query += " from sinhvien sv where lop_id = " + str(lopid)    
        print(query)    
        cur.execute(query)
        rows = cur.fetchall()
        print(rows[0])
        return rows
                
    else:
        print("length <= 1")
        try:
            query = "select sv_maso, sv_hoten, (case when thoigiandiemdanh isnull then 'A' else '' end) as diemdanh from sinhvien sv\
                left join diemdanh dd on sv.sv_id = dd.sv_id and tkb_id = %s\
                where lop_id = %s"
            cur.execute(query, (lopid, l_tkbid[0][0]))
            rows = cur.fetchall()
            return rows
        except psycopg2.Error as e:
            print("Error selecting rows: ", e)
        finally:
            cur.close()
            conn.close()