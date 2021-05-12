import flask
from flask import Flask, render_template, Response
from faces import DetectEmotion
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine('postgresql://postgres:asifnadish@localhost:5432/emo', echo=True)
db=scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    obj=DetectEmotion()                                                               #Create object just to open webcam
    return render_template('index.html')


def gen(camera):
    #while True:
        frame = (camera.get_frame())[0]
        global emo 
        emo = (camera.get_frame())[1]
        print(f"Detected emotion is {emo}")

        
        return (b'--frame\r\n'                                                        #use yield in place of return in case while statement
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

       
        
@app.route('/show_list')
def show_list():
    song_list = db.execute("SELECT song_title,song_url,singer FROM songs WHERE song_type=(:emo)",{"emo":emo}).fetchall()
    db.commit()
    return render_template('fetch.html',songs_list=song_list,emotion=emo.capitalize()) 

 

    
@app.route('/video_feed')
def video_feed():
    return Response(gen(DetectEmotion()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#if __name__ == '__main__':
    #app.run(debug=True)