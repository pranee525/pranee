import os
from re import M
from flask import Flask,request, render_template,jsonify, Response
import threading
from get_full_live_data import *
import time

def start_scraping_thread(url,match_hours):
    
    print("hello from scraping. url=", url)

    print("hello from scraping. hours=", match_hours)
    frequency = 5
    hours =int(match_hours)
    iterations= int(hours*60*60/frequency)
    print(iterations)
    global app_cfg
    app_cfg.iterations = iterations
    app_cfg.frequency = frequency

    match_id = get_match_id(url)
    club_id = get_club_id(url)
    local_time  = time.localtime()
    local_time = time.strftime('%Y_%m_%d_%H_%M_%S', local_time)
    filename = 'match_'+match_id+'club_'+club_id+'_'+local_time+'.json'
    save_live_match_content(url,iterations,frequency,filename)
    return

class Config:
    gthread = None
    iterations = 0
    frequency = 1

app = Flask(__name__)
app_cfg = Config

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/join', methods=['GET','POST'])
def start_script():
    match_id = request.form['match_id']
    club_id = request.form['club_id']
    match_hours=request.form['hours']
    url = get_url(match_id=match_id, club_id=club_id)
    url_valid = check_url_valid(url)
    if url_valid:
        result = {'resp':'valid match_id, and club_id. starting collecting score..'}
        st=threading.Thread(target=start_scraping_thread, args=(url,match_hours))
        app_cfg.gthread = st

        st.start()
    else:
        result = {"resp":'match_id or club_id is invalid. Please check'}
    return jsonify(result=result)

@app.route('/progress', methods=['GET', 'POST'])
def progress():
    print("In progress function")
    def show_progress():
        iteration = 0
        while (1):
            val_dict = {}
            print("progress iteration..")
            global app_cfg
            val_dict['iteration'] = iteration
            val_dict['status'] = 'stopped'

            if (app_cfg.gthread):
                print("global thread assigned..")
                if(app_cfg.gthread.is_alive()):
                    print("global thread is alive")
                    val_dict['iteration'] = iteration
                    val_dict['status'] = 'running'
                    iteration = iteration + app_cfg.frequency

                else:
                    print("global thread is not alive")
                    val_dict['iteration'] = iteration
                    val_dict['status'] = 'stopped'

            else:
                print("global thread didn't start yet")

            val_dict['iterations'] = app_cfg.iterations
            ret_string = "data:" + json.dumps(val_dict) + "\n\n"
            print(ret_string)
            yield ret_string
            time.sleep(app_cfg.frequency)

    return Response(show_progress(), mimetype= 'text/event-stream')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host='0.0.0.0', port=port,threaded=True)
    #app.run(debug=True)
