import psycopg2

def login(cb_maso, cb_matkhau):
    try:
        loaitaikhoan = -1
        conn = psycopg2.connect(database="db_diemdanhsinhvien",
                            user="postgres",
                            password="12345678",
                            host="localhost", port="5432")
        statement = "SELECT cb_quyentruycap from canbo WHERE cb_maso=%s AND cb_matkhau =%s and cb_trangthai;"
        cur = conn.cursor()
        query = cur.execute(statement,  (str(cb_maso), str(cb_matkhau)))
        isRecordExist = 0
        result_set = cur.fetchall()
        for row in result_set:
            loaitaikhoan = row[0]
            isRecordExist = 1
        if (isRecordExist == 0):
            return -1
        else:
            return loaitaikhoan
    except:
        print("Da co loi")