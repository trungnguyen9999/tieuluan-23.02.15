
from flask import Flask, render_template, request, redirect, session, Response, jsonify
import cv2, json
from datetime import timedelta, datetime
import os, time
import numpy as np
from PIL import Image
import base64, ast
import dataprovider as dp
from model import CanBo,  SinhVien, ThoiKhoaBieu, CauHinh, LopHoc

from model.MonHoc import MonHoc
from model.Khoa import Khoa
from model.NganhHoc import NganhHoc
from model.DiemDanh import DiemDanh
from model.LopHoc import LopHoc
from database import db

app = Flask(__name__)
app.secret_key = 'ntnguyen'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/db_diemdanhsinhvien'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
# user = {"cb_maso": "10067", "cb_matkhau": "nguyen@cusc"}

CanBo = CanBo.CanBo()
objSinhVien = SinhVien.SinhVien()
sinhVien=None
objLopHoc = LopHoc
objThoiKhoaBieu = ThoiKhoaBieu.ThoiKhoaBieu()
recognizer = cv2.face.LBPHFaceRecognizer_create()
pathData = "../src/dataset/"

global_cam = 0
def set_global_cam(new_value):
    global global_cam
    global_cam = new_value

def setObjSinhVien(sv):
    global sinhVien   
    sinhVien = sv 

@app.route('/')
@app.route('/home')
def index():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        _cb = CanBo.get_canbo_by_maso(cbmaso)
        print(CauHinh.get_cauhinh(_cb.cb_id).value)
        if(CauHinh.get_cauhinh(_cb.cb_id).value != None):
            ch = CauHinh.get_cauhinh(_cb.cb_id).value.replace("'", "\"")
            data = ast.literal_eval(ch)
            set_global_cam(int(data['sdcamera']))
        else:
            data = ast.literal_eval("{'chid': '', 'cbid': '" + str(_cb.cb_id) + "', 'giovao': '07:30', 'giora': '11:00', 'biendotre': '30', 'checkin': '1', 'checkout': '1', 'sdcamera': '0', 'strip': ''}")
            CauHinh.save_cauhinh(data)
        return render_template('index.html', 
            cb=_cb, 
            timeline=dp.get_timeline(),
            name_page="index", tieude="Bảng điều khiển")
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
    CanBo.save_canbo(None, cbUsername, cbMatKhau, cbHoTen, cbNgaySinh, cbDiaChi, cbEmail, cbDienThoai, -1, datetime.now(), 1, False, '')
    if(request.args.get("dangky") == 'false'):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_canbo=CanBo.get_canbo_list(), 
            name_page="canbo", tieude="Quản lý cán bộ")
    return render_template('login.html')


@app.route('/can-bo')
def get_canbo():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_canbo=CanBo.get_canbo_list(), 
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
                cb=CanBo.get_canbo_by_maso(cbmaso), 
                sinhvien=_sv, 
                list_lophoc=_listlop,
                name_page="dulieukhuonmat", tieude="Nạp dữ liệu khuôn mặt")
        else:
            return render_template('index.html', 
                cb=CanBo.get_canbo_by_maso(cbmaso), 
                list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
                list_lophoc=_listlop,
                name_page="sinhvien", tieude="Quản lý sinh viên")
        
    return render_template('login.html')
 
@app.route('/sinh-vien')
def get_sinhvien():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list("-1")
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0]), 
            list_lophoc=_listlop,
            name_page="sinhvien", tieude="Quản lý sinh viên")
    return render_template('login.html')

@app.route('/sinh-vien',  methods=['POST'])
def capnhat_sinhvien():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        if(session['type-account'] == 2):
            _listlop = objLopHoc.get_lophoc_list("-1")
        else:
             _listlop = objLopHoc.get_lophoc_list("-1")
        _listSinhvien=objSinhVien.get_sinhvien_list(_listlop[0][0])
        if(request.method == 'POST'):
            if(request.args.get("change") == "1"):
                lopOption = request.form['lop']
                _listSinhvien=objSinhVien.get_sinhvien_list(lopOption)
                print(lopOption)
            else:
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
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_sinhvien=_listSinhvien, 
            list_lophoc=_listlop,
            name_page="sinhvien", tieude="Quản lý sinh viên")
    return render_template('login.html')

@app.route('/diem-danh', methods=['GET', 'POST'])
def diemdanhkhuonmat():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        cb = CanBo.get_canbo_by_maso(cbmaso)
        ch = CauHinh.get_cauhinh(cb.cb_id).value.replace("'", "\"")
        data = ast.literal_eval(ch)
        set_global_cam(int(data['sdcamera']))
        list_lich = dp.get_list_tkb_diemdanh(cb.cb_id)
        list_sv = None
        tkb_id = 0
        thoidiem_dd = None
        #Cập nhật điểm danh thủ công
        if(request.args.get('type') == '1'):
            print("Diem danh thu cong tkbid = " + request.args.get('tkbid'))
            data = request.get_json()
            thoidiem_dd = request.args.get("thoidiem_dd")
            print(thoidiem_dd)
            dd_giovao = False
            if(thoidiem_dd == '1'):
                dd_giovao = True
            for svid in data:
                timedd = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                DiemDanh.save_diemdanh(None, svid, request.args.get('tkbid'), timedd, 1, '', 1, dd_giovao)
                
        if( request.method == 'POST' and request.form.get("tkb_id") != None and request.form.get("thoidiem_dd") != None):
            tkb_id = request.form.get("tkb_id")
            thoidiem_dd = request.form.get("thoidiem_dd")
            dd_giovao = False
            if(thoidiem_dd == '1'):
                dd_giovao = True
            list_sv = enumerate(dp.get_sinhvien_by_tkb_id(tkb_id, dd_giovao), start=1)
            
        return render_template('index.html', 
            cb=cb, 
            tkbid=tkb_id,
            thoidiem_dd=thoidiem_dd,
            list_sinhvien=list_sv, 
            list_thoikhoabieu_diemdanh=list_lich, 
            url="static/assets/img/user.png",
            name_page="diemdanhkhuonmat", tieude="")
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
            cbmaso = session['user']
            _cb=CanBo.get_canbo_by_maso(cbmaso)
            ch=CauHinh.get_cauhinh(_cb.cb_id)
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

#================== Các chức năng trong profile ====================================================
@app.route('/profile')
def view_profile():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        _cb=CanBo.get_canbo_by_maso(cbmaso)
        ch=CauHinh.get_cauhinh(_cb.cb_id)
        if(ch.value != None):
            value_ch = json.loads(ch.value.replace('\'', '\"'))
        else:
            value_ch = ""
        return render_template('index.html', 
            cb=_cb,
            chid=ch.ch_id,
            cauhinh=value_ch,
            name_page="profile", tieude="Thông tin cá nhân")
    return render_template('login.html')

@app.route('/cau-hinh', methods=['GET', 'POST'])
def cauhinh():
    if(request.method == 'POST'):
        data = request.get_json()
        print(data)
        CauHinh.save_cauhinh(data)
        if('user' in session and 'type-account' in session):
            cbmaso = session['user']
            _cb=CanBo.get_canbo_by_maso(cbmaso)
            _ch = CauHinh.get_cauhinh(_cb.cb_id)
            print(_ch)
            return render_template('index.html', 
                cb=_cb,
                cauhinh=_ch,
                name_page="profile", tieude="Thông tin cá nhân")
    return render_template('login.html')

#================== Các chức năng trong profile ====================================================

def nap_data():
    camera = cv2.VideoCapture(int(global_cam))  # use 0 for web camera
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
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        trainningData()
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
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
    if('user' in session and 'type-account' in session):
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
                cb=CanBo.get_canbo_by_maso(cbmaso), 
                active_tab="phôtp",
                name_page="diemdanhkhuonmat", tieude="")
    return render_template('login.html')

def draw_rectangle(img, rect):
    '''Draw a rectangle on the image'''
    
def gen_frames():
    print( global_cam)
    camera = cv2.VideoCapture(int(global_cam))  # use 0 for web camera
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
                        #Kiểm tra nếu lần đầu hoặc mỗi lần điểm danh cách nhau 40p
                        print("True" in str(dp.is_ins_diemdanh(profile[9])))
                        if("True" in str(dp.is_ins_diemdanh(profile[9]))):
                            print("abc: " + str(profile[9]))
                            timedd = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            
                            dp.save_diemdanh(int(profile[9]), 0, timedd, 1, '', 2, True)
                        
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

@app.route('/diem-danh-chung')
def diem_danh_chung():
    print("diem_danh_chung")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_nap_data')
def video_nap_data():
    print("video_nap_data")
    if('user' in session):
        return Response(nap_data(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')

@app.route('/thoi-khoa-bieu', methods=['POST', 'GET'])
def thoi_khoa_bieu():
    if(request.method == 'POST'): 
        title = request.form.get('txtTieuDe') 
        cbId = request.form.get('txtCanBo')   
        lopId = request.form.get('txtLop') 
        hpId = request.form.get('txtHocPhan') 
        ngayHoc = request.form.get('txtNgayHoc') 
        gioVao = request.form.get('txtGioVao') 
        gioRa = request.form.get('txtGioRa') 
        hinhThuc = request.form.get('rdHinhThuc')
        phongHoc = request.form.get('txtPhongHoc') 
        ghiChu = request.form.get('txtGhiChu') 
        
        thuchanh = False
        if(hinhThuc == '2'):
            thuchanh = True
        objThoiKhoaBieu.insert_data(cbId, lopId, hpId, ngayHoc, gioVao, gioRa, thuchanh, ghiChu, phongHoc, title)
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        typeaccount = session['type-account']
        
        _listcanbo = CanBo.get_canbo_list()
        if(typeaccount == 2):
            print("quan tri lay thong tin tkb")
            _listlop = objLopHoc.get_lophoc_list("-1")
            return render_template('index.html',
                cb=CanBo.get_canbo_by_maso(cbmaso), 
                list_canbo=_listcanbo, 
                list_lophoc=_listlop,
                list_hocphan=MonHoc.get_monhoc(),
                list_thoikhoabieu=objThoiKhoaBieu.get_tkb_full(),
                name_page="thoikhoabieu", tieude="Thời khóa biểu")
        _listlop = objLopHoc.get_lophoc_list(cbmaso)
        if(_listlop != None):
            data_tkb = objThoiKhoaBieu.get_tkb_list(CanBo.get_canbo_id_by_maso(cbmaso))
        else:
            data_tkb = None
        return render_template('index.html',
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_lophoc=_listlop,
            list_thoikhoabieu=data_tkb,
            name_page="thoikhoabieu", tieude="Thời khóa biểu")
    return render_template('login.html')

@app.route('/events')
def events():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        _listcanbo = CanBo.get_canbo_list()
        typeaccount = session['type-account']
        if(typeaccount == 2):
            list_thoikhoabieu=objThoiKhoaBieu.get_tkb_full()
            return jsonify(list_thoikhoabieu)
        
        list_thoikhoabieu=objThoiKhoaBieu.get_tkb_list(CanBo.get_canbo_id_by_maso(cbmaso))
        return jsonify(list_thoikhoabieu)
    
#*********************************************** Môn Học**************************************************

@app.route('/mon-hoc') 
def list_monhoc():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        ds_monhoc =  MonHoc.get_monhoc()
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            monhocs=ds_monhoc, name_page="monhoc", tieude="Quản lý môn học")
    return render_template('login.html')


@app.route('/save-mon-hoc', methods=['GET','POST'])
def actionSaveMonHoc():
    message = ""
    mhId = request.form.get('idMon')
    mhMa = request.form.get('maMon')
    mhTen = request.form.get('tenMon')
    mhTinChi = request.form.get('soTinChi')
    mhLyThuyet = request.form.get('lyThuyet')
    mhThucHanh = request.form.get('thucHanh')
    result = MonHoc.save_monhoc(mhId, mhMa, mhTen, mhTinChi, mhLyThuyet, mhThucHanh)

    if result == None:
        message = "Mã môn đã tồn tại"
    cbmaso = session['user']
    ds_monhoc = MonHoc.get_monhoc()
    return render_template('index.html', 
        cb=CanBo.get_canbo_by_maso(cbmaso), 
        monhocs=ds_monhoc, 
        name_page="monhoc", tieude="Quản lý môn học",mes =message)

@app.route('/delete-mon-hoc', methods=['POST'])
def actionDeletedMonHoc():
    mhId = request.form.get('monhoc_id')
    rs = MonHoc.delete_monhoc_by_id(mhId)
    if rs:
        message = "Xóa thành công"
    else:
        message = "Không thể xóa môn học"
    cbmaso = session['user']
    ds_monhoc = MonHoc.get_monhoc()
    return render_template('index.html', 
        cb=CanBo.get_canbo_by_maso(cbmaso), 
        monhocs=ds_monhoc, 
        name_page="monhoc", tieude="Quản lý môn học",mes =message)
    
@app.route('/khoa') 
def list_khoa():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_khoa=enumerate(Khoa.get_khoa_list(), start=1), 
            name_page="khoa", tieude="Quản lý khoa")
    return render_template('login.html')

@app.route('/save-khoa-hoc', methods=['GET','POST'])
def actionSaveKhoa():
    message = "" 
    
    khoa_id = request.form.get('idKhoa')
    khoa_ma = request.form.get('maKhoa')
    khoa_ten = request.form.get('tenKhoa')
    rs = Khoa.save_khoa(khoa_id, khoa_ma, khoa_ten)
             
    cbmaso = session['user']
    return render_template('index.html', 
        cb=CanBo.get_canbo_by_maso(cbmaso), 
        list_khoa=enumerate(Khoa.get_khoa_list(), start=1), 
        name_page="khoa", tieude="Quản lý Khoa",mes =message)

@app.route('/nganhhoc') 
def list_nganhhoc():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            list_khoa=Khoa.get_khoa_list(), 
            list_nganhhoc=enumerate(NganhHoc.get_nganhhoc_list(), start=1),
            name_page="nganhhoc", tieude="Quản lý ngành học") 
    return render_template('login.html')

@app.route('/save-nganh-hoc', methods=['GET','POST'])
def actionSaveNganhHoc():
    print("hello...")
    
    nhId = request.form.get('idNganhHoc')
    nhMa = request.form.get('maNganhHoc')
    nhTen = request.form.get('tenNganhHoc')
    khoaId = request.form.get('khoa')
    rs = NganhHoc.save_nganhhoc(nhId, nhMa, nhTen, khoaId)
    cbmaso = session['user']
    return render_template('index.html', 
        cb=CanBo.get_canbo_by_maso(cbmaso), 
        list_khoa=Khoa.get_khoa_list(), 
        list_nganhhoc=enumerate(NganhHoc.get_nganhhoc_list(), start=1),
        name_page="nganhhoc", tieude="Quản lý ngành học")

#==================================Bảng điểm danh ====================
@app.route('/bang-diem-danh', methods=['GET','POST'])
def bang_diem_danh():
    if('user' in session):
        cbmaso = session['user']
        cb=CanBo.get_canbo_by_maso(cbmaso)
        list_col = None
        data_diemdanh = None
        if(request.method == 'POST'): 
            lop = request.form.get('lophoc') 
            mon = request.form.get('monhoc')   
            print("lop = " + lop + " - mon = " + mon + " - cbid = " + str(cb.cb_id))
            list_col = dp.get_column_diemdanh(lop, mon, cb.cb_id)
            print(str(list_col))
            if(len(list_col) > 0):
                data_diemdanh = dp.get_data_diemdanh(lop, list_col)
            
        return render_template('index.html', 
            cb=cb, 
            list_col = list_col,
            data_diemdanh = data_diemdanh,
            ds_monhoc = MonHoc.get_monhoc(),
            list_lophoc = objLopHoc.get_lophoc_list(cbmaso),
            name_page="bangdiemdanh", tieude="Bảng điểm danh sinh viên")
    return render_template('login.html')

#======================= só buổi vắng ====================
@app.route('/so-buoi-vang', methods=['GET','POST'])
def so_buoi_vang():
    if('user' in session):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            ds_monhoc = MonHoc.get_monhoc(),
            list_lophoc = objLopHoc.get_lophoc_list(cbmaso),
            name_page="sobuoivang", tieude="Thống kê số buổi vắng")
    return render_template('login.html')

#======================= giờ dạy ====================
@app.route('/gio-day', methods=['GET','POST'])
def gio_day():
    if('user' in session):
        cbmaso = session['user']
        return render_template('index.html', 
            cb=CanBo.get_canbo_by_maso(cbmaso), 
            ds_monhoc = MonHoc.get_monhoc(),
            list_lophoc = objLopHoc.get_lophoc_list(cbmaso),
            name_page="gioday", tieude="Thống kê số giờ dạy")
    return render_template('login.html')


#*********************************************** Lớp học **************************************************
@app.route('/lop-hoc') 
def list_lophoc():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        ds_lophoc = LopHoc.get_lop()
        return render_template('index.html', cb=CanBo.get_canbo_by_maso(cbmaso), lophocs=ds_lophoc, name_page="lophoc", tieude="Quản lý lớp học")
    return render_template('login.html')

@app.route('/save-lop-hoc', methods=['GET','POST'])
def actionSaveLopHoc():
    message = ""
    lopId = request.form.get('idLop')
    lopMa = request.form.get('maLop')
    lopTen = request.form.get('tenLop')
    soLuongSV = request.form.get('soLuongSV')
    coVanId = request.form.get('coVan')
    nhId = request.form.get('nganhHoc')
    nienKhoa = request.form.get('nienkhoa')
    result = LopHoc.save_lophoc(lopId, lopMa, lopTen, soLuongSV, coVanId, nhId, nienKhoa)
    
    if result == None:
       message = "Mã lớp đã tồn tại"
    #    print("-------> " + message)   
       
    cbmaso = session['user']
    ds_lophoc = LopHoc.get_lop()
    return render_template('index.html', cb=CanBo.get_canbo_by_maso(cbmaso), lophocs=ds_lophoc, name_page="lophoc", tieude="Quản lý lớp học",mes =message)
@app.route('/delete-lop-hoc', methods=['POST'])
def actionDeletedLopHoc():
    
    lopId = request.form.get('lop_id')
    print("---------Xóa lớp học" + str(lopId))
    rs = LopHoc.delete_lophoc_by_id(lopId)
    if rs:
        message = "Xóa thành công"
    else:
        message = "Không thể xóa lớp học"
        
    cbmaso = session['user']
    ds_lophoc = LopHoc.get_lop()
    return render_template('index.html', cb=CanBo.get_canbo_by_maso(cbmaso), lophocs=ds_lophoc, name_page="lophoc", tieude="Quản lý lớp học",mes =message)



if __name__ == '__main__':
    app.run(debug=True)