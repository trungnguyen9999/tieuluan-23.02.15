
from flask import Flask, render_template, request, redirect, session, Response
import cv2
from datetime import timedelta
import dataprovider as dp

app = Flask(__name__)
app.secret_key = 'ntnguyen'
camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)
user = {"cb_maso": "10067", "cb_matkhau": "nguyen@cusc"}


@app.route('/')
@app.route('/home')
def index():
    if('user' in session):
        return render_template('index.html')
    return render_template('login.html')

# @app.route('/khoa')
# def khoa():
    # conn = psycopg2.connect(database="db_diemdanhsinhvien",
    #                         user="postgres",
    #                         password="1234567",
    #                         host="localhost", port="5432")
    # cur = conn.cursor()
    # cur.execute('''SELECT * FROM khoa''')
    # data = cur.fetchall()
    # cur.close()
    # conn.close()
    # return render_template('khoa.html', data=data)

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


@app.route('/diem-danh')
def diemdanh():
    if('user' in session):
        return render_template('diemdanh.html')
    return render_template('login.html')
    

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            
            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    if('user' in session):
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)