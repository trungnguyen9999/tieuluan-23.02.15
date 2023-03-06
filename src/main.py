
from flask import Flask, render_template, request, redirect, session, Response
import cv2
from datetime import timedelta, datetime
import dataprovider as dp
from model import CanBo as cb

app = Flask(__name__)
app.secret_key = 'ntnguyen'
camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
# user = {"cb_maso": "10067", "cb_matkhau": "nguyen@cusc"}

canbo = cb.CanBo()

@app.route('/')
@app.route('/home')
def index():
    if('user' in session and 'type-account' in session):
        cbmaso = session['user']
        return render_template('index.html', cb=canbo.get_canbo_by_maso(cbmaso), name_page="index", tieude="Bảng điều khiển")
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
    
    canBo = cb.CanBo(cbUsername, cbMatKhau, cbHoTen, cbNgaySinh, cbDiaChi, cbEmail, cbDienThoai, -1, datetime.now(), 0, False)
    if(canBo.create()):
        return render_template('login.html')
    else:
        return render_template('register.html')

@app.route('/can-bo')
def list_canbo():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', cb=canbo.get_canbo_by_maso(cbmaso), list_canbo=canbo.get_canbo_list(100,0), name_page="canbo", tieude="Quản lý cán bộ")
    return render_template('login.html')

@app.route('/diem-danh')
def diemdanhkhuonmat():
    if('user' in session and 'type-account' in session and session['type-account'] == 2):
        cbmaso = session['user']
        return render_template('index.html', cb=canbo.get_canbo_by_maso(cbmaso), name_page="diemdanhkhuonmat", tieude="Điểm danh sinh viên bằng nhận diện khuôn mặt")
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

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    if('user' in session):
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)