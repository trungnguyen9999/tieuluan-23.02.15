
from flask import Flask, render_template, request, redirect, session, Response, jsonify
import cv2, json
from datetime import timedelta, datetime
import os, time
import numpy as np
from PIL import Image
import base64
import dataprovider as dp
from model import CanBo, NienKhoa, SinhVien, LopHoc, ThoiKhoaBieu, MonHoc as mh

app = Flask(__name__)
app.secret_key = 'ntnguyen'

#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
# user = {"cb_maso": "10067", "cb_matkhau": "nguyen@cusc"}

objCanBo = CanBo.CanBo()
objSinhVien = SinhVien.SinhVien()
sinhVien=None
objLopHoc = LopHoc.LopHoc()
objThoiKhoaBieu = ThoiKhoaBieu.ThoiKhoaBieu()
recognizer = cv2.face.LBPHFaceRecognizer_create()
pathData = "../src/dataset/"
cam = 0
monhoc = mh.MonHoc()

def setObjSinhVien(sv):
    global sinhVien   
    sinhVien = sv 

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
            list_canbo=objCanBo.get_canbo_list(), 
            name_page="canbo", tieude="Quản lý cán bộ")
    return render_template('login.html')
 
@app.route('/du-lieu-khuon-mat')
def get_Dulieu_Khuonmat():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        _sv = objSinhVien.get_sinhvien_by_id(request.args.get("svid"))
        setObjSinhVien(_sv)
        if(request.args.get("svid") != None):
            return render_template('index.html', 
                cb=objCanBo.get_canbo_by_maso(cbmaso), 
                sinhvien=_sv, 
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
            url="static/assets/img/user.png",
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
            name_page="profile", tieude="Thông tin cá nhân")
    return render_template('login.html')

def nap_data():
    camera = cv2.VideoCapture(cam)  # use 0 for web camera
    index = 0
    mssv = sinhVien[0]
    print("MSSV: " + mssv)
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
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 224, 19), 2)
                cv2.putText(frame, str(index) + " %", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)

                if not os.path.exists('../src/dataset/' + str(sinhVien[9]) + '.' + str(sinhVien[0])):
                    os.makedirs('dataset/' + str(sinhVien[9]) + '.' + str(sinhVien[0]))
                index += 1
                cv2.imwrite('../src/dataset/' + str(sinhVien[9]) + '.' + str(sinhVien[0]) + '/student_'+ str(sinhVien[9]) + '.' + str(sinhVien[0]) + '.' + str(index) + '.jpg', gray[y: y+h, x: x+w])
           
            
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes() 
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            if(index > 100):
                camera.release()
                break
            time.sleep(0.1)
    print("xong roi")
    return redirect('/sinh-vien')
    
@app.route('/train-data')
def train_data():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        trainningData()
        return render_template('index.html', 
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
            list_lophoc=_listlop,
            name_page="sinhvien", tieude="Quản lý sinh viên")
    return render_template('login.html')
def getImageWithMssv(pathData):
    sinhVienPaths = [os.path.join(pathData, f) for f in os.listdir(pathData)]
    print(sinhVienPaths)
    faces = []
    ids = []
    for sinhVienPath in sinhVienPaths:
        print(sinhVienPath)
        imagePaths = [os.path.join(sinhVienPath, f) for f in os.listdir(sinhVienPath)]
        
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            
            faces.append(faceNp)
            ids.append(int(sinhVienPath.split("/")[3].split(".")[0]))
    return faces, ids
    
def trainningData():
    print("Trainning...")
    _faces, _ids = getImageWithMssv(pathData)
    recognizer.train(_faces, np.array(_ids))

    if not os.path.exists('../src/recognizer'):
        os.makedirs('../src/recognizer')

    recognizer.save('../src/recognizer/trainingdata.yml')

@app.route('/upload-img', methods=['POST'])
def detect_img():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        file = request.files['image']
        # Đọc hình ảnh và chuyển đổi sang định dạng Grayscale
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Nhận diện khuôn mặt bằng phương pháp Haar Cascade
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)
        if len(img.shape) == 2:
            # convert the grayscale image to RGB
            gray = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        else:
            # the input image is already in RGB format
            gray = img
        # Trả về danh sách tọa độ khuôn mặt
        result = []
        for i in range(0, len(faces)):
            (x, y, w, h) = faces[i]
            face_dict = {}
            face_dict['face'] = gray[y:y + w, x:x + h]
            face_dict['rect'] = faces[i]
            result.append(face_dict)
        
        for item in result:
            (x, y, w, h) = item['rect']
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
            # roi_gray = gray[y:y+h, x:x+w]
            # faces = face_cascade.detectMultiScale(roi_gray, 1.1, 3)
            # id, confidence = recognizer.predict(roi_gray)
            # if confidence < 40:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 224, 19), 2)
            #     profile = objSinhVien.get_sinhvien_by_id(id)
            #     cv2.putText(img, "" + str(profile[0]), (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
            #     if(profile != None):
            #         print(profile)
            # else:
            #     cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 2)
            #     cv2.putText(img, "Unknown", (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)    
        
        image_content = cv2.imencode('.jpg', img)[1].tostring()
        encoded_image = base64.encodebytes(image_content)
        to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
        print("encoded_image")
        return render_template('index.html', 
                faceDetected=True, num_faces=len(result), image_to_show=to_send, init=True,
                cb=objCanBo.get_canbo_by_maso(cbmaso), 
                list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
                list_lophoc=_listlop, 
                name_page="diemdanhkhuonmat", tieude="Điểm danh sinh viên bằng nhận diện khuôn mặt")
    return render_template('login.html')

def draw_rectangle(img, rect):
    '''Draw a rectangle on the image'''
    
def gen_frames():
    camera = cv2.VideoCapture(cam)  # use 0 for web camera
    recognizer.read('../src/recognizer/trainingdata.yml')
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
                    profile = objSinhVien.get_sinhvien_by_id(id)
                    cv2.putText(frame, str(profile[0]), (x+10, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 224, 19), 2)
                    if(profile != None):
                        print(profile)
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
    print("video_feed")
    if('user' in session):
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')

@app.route('/video_nap_data')
def video_nap_data():
    print("video_nap_data")
    if('user' in session):
        return Response(nap_data(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')

@app.route('/thoi-khoa-bieu')
def thoi_khoa_bieu():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        typeaccount = session['type-account']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        _listcanbo = objCanBo.get_canbo_list()
        if(typeaccount == 2):
            return render_template('index.html',
                cb=objCanBo.get_canbo_by_maso(cbmaso), 
                list_canbo=_listcanbo, 
                list_lophoc=_listlop,
                list_hocphan="",
                list_thoikhoabieu=objThoiKhoaBieu.get_tkb_list(_listcanbo[0][0]),
                name_page="thoikhoabieu", tieude="Thời khóa biểu")
        return render_template('index.html',
            cb=objCanBo.get_canbo_by_maso(cbmaso), 
            list_lophoc=_listlop,
            list_thoikhoabieu=objThoiKhoaBieu.get_tkb_list(objCanBo.get_canbo_id_by_maso(cbmaso)),
            name_page="thoikhoabieu", tieude="Thời khóa biểu")
    return render_template('login.html')

@app.route('/events')
def events():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        _listcanbo = objCanBo.get_canbo_list()
        typeaccount = session['type-account']
        if(typeaccount == 2):
            list_thoikhoabieu=objThoiKhoaBieu.get_tkb_list("2")
            print(list_thoikhoabieu)
            return jsonify(list_thoikhoabieu)
        list_thoikhoabieu=objThoiKhoaBieu.get_tkb_list(objCanBo.get_canbo_id_by_maso(cbmaso))
        print(list_thoikhoabieu)
        return jsonify(list_thoikhoabieu)
#*********************************************** Môn Học**************************************************


@app.route('/mon-hoc') 
def list_monhoc():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', cb=objCanBo.get_canbo_by_maso(cbmaso), list_monhoc=monhoc.get_monhoc_list(100,0), name_page="monhoc", tieude="Quản lý môn học")
    return render_template('login.html')

@app.route('/create-mon-hoc', methods=['GET','POST'])
def actionCreateMonHoc():
    message = ""
    mhMa = request.form.get('maMon')
    mhTen = request.form.get('tenMon')
    mhTinChi = request.form.get('soTinChi')
    mhLyThuyet = request.form.get('lyThuyet')
    mhThucHanh = request.form.get('thucHanh')    
    monhoc = mh.MonHoc(mhMa, mhTen, mhTinChi, mhLyThuyet, mhThucHanh)
    
    if(monhoc.checkExitByMaMon()):
       message = "Mã môn đã tồn tại"
    else:
        print("mã số không trùng")
        monhoc.create()
    
    cbmaso = session['user']
    return render_template('index.html', cb=objCanBo.get_canbo_by_maso(cbmaso), list_monhoc=monhoc.get_monhoc_list(100,0), name_page="monhoc", tieude="Quản lý môn học",mes =message)
if __name__ == '__main__':
    app.run(debug=True)