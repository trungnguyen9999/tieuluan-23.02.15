
from flask import Flask, render_template, request, redirect, session, Response
import cv2
from datetime import timedelta, datetime
import dataprovider as dp
from model import CanBo, SinhVien, LopHoc

app = Flask(__name__)
app.secret_key = 'ntnguyen'


#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
# user = {"cb_maso": "10067", "cb_matkhau": "nguyen@cusc"}

objCanBo = CanBo.CanBo()
objSinhVien = SinhVien.SinhVien()
objLopHoc = LopHoc.LopHoc()

@app.route('/')
@app.route('/home')
def index():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        return render_template('index.html', cb=objCanBo.get_canbo_by_maso(cbmaso), name_page="index", tieude="Bảng điều khiển")
    return render_template('login.html')

@app.route('/dang-ky')
def dangky():
    return render_template('register.html')

@app.route('/dang-ky', methods=['GET', 'POST'])
def actiondangky():
    print("action dang ky")
    cbHoTen = request.form.get('fullname')
    cbEmail = request.form.get('email')
    cbUsername = request.form.get('username')
    cbDienThoai = request.form.get('phonenumber')
    cbMatKhau = request.form.get('password')
    cbNgaySinh = request.form.get('birthdate')
    cbDiaChi = request.form.get('address')
    
    canBo = CanBo.CanBo(cbUsername, cbMatKhau, cbHoTen, cbNgaySinh, cbDiaChi, cbEmail, cbDienThoai, -1, datetime.now(), 0, False)
    if(canBo.create()):
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/can-bo')
def get_canbo():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_canbo=objCanBo.get_canbo_list(100,0), 
            name_page="canbo", tieude="Quản lý cán bộ")
    return render_template('login.html')
 
@app.route('/du-lieu-khuon-mat')
def get_Dulieu_Khuonmat():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        if(request.args.get("svid") != None):
            return render_template('index.html', 
                cb=objCanBo.get_canbo_by_maso(cbmaso), 
                sinhvien=objSinhVien.get_sinhvien_by_id(request.args.get("svid")), 
                list_lophoc=_listlop,
                name_page="dulieukhuonmat", tieude="Nạp dữ liệu khuôn mặt")
        else:
            return render_template('index.html', 
                cb=objCanBo.get_canbo_by_maso(cbmaso), 
                list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
                list_lophoc=_listlop,
                name_page="sinhvien", tieude="Quản lý sinh viên")
        
    return render_template('login.html')
 
@app.route('/sinh-vien')
def get_sinhvien():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        print("First ckass: " + _listlop[0][1])
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
            list_lophoc=_listlop,
            name_page="sinhvien", tieude="Quản lý sinh viên")
    return render_template('login.html')

@app.route('/sinh-vien',  methods=['GET', 'POST'])
def capnhat_sinhvien():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        #Lay du lieu tu form submit qua
        hoten = request.form.get('fullname')
        email = request.form.get('email')
        maso = request.form.get('maso')
        dienthoai = request.form.get('phonenumber')
        lop = request.form.get('lop')
        ngaysinh = request.form.get('birthdate')
        gioitinh = request.form.get('gridRadios')
        diachi = request.form.get('address')
        SinhVien.SinhVien(maso, hoten, ngaysinh, diachi, email, dienthoai, lop, gioitinh).create()
        #Luu vao CSDL
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
            list_lophoc=_listlop,
            name_page="sinhvien", tieude="Quản lý sinh viên")
    return render_template('login.html')

@app.route('/diem-danh')
def diemdanhkhuonmat():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
            list_lophoc=_listlop, 
            name_page="diemdanhkhuonmat", tieude="Điểm danh sinh viên bằng nhận diện khuôn mặt")
    return render_template('login.html')

@app.route('/dang-nhap', methods=['GET', 'POST'])
def dangnhap():     
    if(request.method == 'POST'): 
        username = request.form.get('cb_maso')   
        password = request.form.get('cb_matkhau') 
        remember = request.form.get('remember')    
        quyentruycap = dp.login(username, password)
        if quyentruycap != None and quyentruycap != -1:
            session['user'] = username
            session['type-account'] = quyentruycap
            session.permanent = True
            if(remember):
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                app.permanent_session_lifetime = timedelta(minutes=30) 
            return redirect('/home')
        return render_template("login.html")    #if the username or password does not matches 
    return render_template("login.html")

@app.route('/logout')
def dangxuat(): 
    session.clear()
    return render_template("login.html")

@app.route('/profile')
def view_profile():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_canbo=objCanBo.get_canbo_list(100,0), 
            name_page="profile", tieude="Thông tin cá nhân")
    return render_template('login.html')

def nap_data():
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('../recognizer/trainingdata.yml')
    while True: 
        success, frame = camera.read() 
        if not success: 
            break
        else:
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for(x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                faces = face_cascade.detectMultiScale(roi_gray, 1.1, 3)
                id, confidence = recognizer.predict(roi_gray)
                if confidence < 40:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                    cv2.putText(frame, "Tao biet thang nay", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
                    cv2.putText(frame, "Unknown", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames():
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('../recognizer/trainingdata.yml')
    while True: 
        success, frame = camera.read() 
        if not success: 
            break
        else:
            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            
            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            for(x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                faces = face_cascade.detectMultiScale(roi_gray, 1.1, 3)
                id, confidence = recognizer.predict(roi_gray)
                if confidence < 40:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                    cv2.putText(frame, "Tao biet thang nay", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
                else:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255), 2)
                    cv2.putText(frame, "Unknown", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if(cv2.waitKey(1) & 0xFF == ord('q')):
                break


@app.route('/video_feed')
def video_feed():
    if('user' in session):
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)