#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import time
import re
import shutil
import json 

# In[ ]:


from bs4 import BeautifulSoup


# In[ ]:

def get_url(match_id, club_id):
    url = "https://cricclubs.com/ballbyball.do?&matchId="+str(match_id)+"&clubId="+str(club_id)
    print("URL:", url)
    return url

def get_match_content(url):
    
    r = requests.get(url)
    if r.ok:
        soup = BeautifulSoup(r.text)
        content = soup.find_all('div', class_='ball-by-ball-section')
    else:
        content = None
        print("Something went wrong in fetching the content")
        print("Request details:")
        print(r.content)
        print("request status_code: ", r.status_code)
        
    
    return content


# In[ ]:


def get_live_commentary_lines(contents):
    commentary_lines = []
    innings  =0
    for content in contents:
        innings = innings + 1
        balls = content.find_all('ul', class_="list-inline bbb-row")
        for ball in balls:
        #for ball in balls[10:20]:
            ball_no = None
            score = 0
            #print('-------------------')
            #print(ball)
            binfo = ball.find_all('li',class_="col3")
            if len(binfo) >0:
                commentary = binfo[0].text.strip()
            tss = ball.find_all('span')
            time_stamp = " "
            for ts in tss:
                found = re.search("^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", ts.text.strip())
                if found:
                    time_stamp = found.group()
                    break


            col2 = ball.find_all('li',class_="col2")
            if len(col2) > 0:
            # col2 will have either one or two spans.
                spans = col2[0].find_all('span')
            else:
                spans = []
            

            # if there are two spans then, span[0] is score span, second one is ball span
            if len(spans) == 2:
                score = spans[0].text.strip()
                ball_no = spans[1].text.strip()
                row = [innings, time_stamp, score, ball_no, commentary]
                #print(row)
                commentary_lines.append(row)

            #else:
                # if this is only one, it could be empty or..?
                # it seems like we don't need to worry about this case
                #assert(len(spans)==1)
                #score = spans[0].text.strip()
            #print(time,over_ball)
            
    return commentary_lines  



def get_live_end_of_over_details(contents):
    over_details = []
    innings = 0
    for content in contents:
        innings = innings + 1
        end_overs = content.find_all('div', class_='end-over')
        for eo in end_overs:
            #print('---')
            #print(eo)
            row = []
            row.append(innings)
            eo_text = eo.find('h4').text
            row.append(eo_text)
            details=eo.find_all('p')
            for detail in details:
                text = detail.text
                #text.split()
                if text is None:
                    text  = ''
                row.append(text)

            over_details.append(row)
    return over_details


def append_to_json(filename, content):
    # check if 'old_filename' exists. if not, save current file to old_file
    # save the contents in the file
    shutil.copyfile(filename, 'old_'+filename)
    with open(filename, 'w') as f:
        json.dump(content, f)
    
    return
    
def save_live_match_content(url, iterations, frequency, filename='match.json'):
    outfile = open(filename, 'a')
    seconds = 0
    old_commentary_len= 0
    old_eov_len = 0
    full_info = []

    while seconds < iterations:
        print("At iteration:", seconds, " out of", iterations)
        content = get_match_content(url)
        if content is None:
            print("Issue in fetching content from CC")
            break

        over_details = get_live_end_of_over_details(content)

        commentary_lines = get_live_commentary_lines(content)        
        new_commentary_len = len(commentary_lines)
        print("Length of new commentary:",new_commentary_len) 
        print("Length of old commentary:",old_commentary_len) 
        #print("New commentary details here..", commentary_lines[0])
        if new_commentary_len != old_commentary_len:
            print("New commentary details here..")
            local_time  = time.localtime()
            local_time = time.strftime('%Y_%m_%d_%H:%M:%S', local_time)
            info = {}
            info['timestamp'] = local_time
            info['ball_info']=commentary_lines
            #commentary_lines.insert(0, local_time)
            full_info.append(info)
            append_to_json(filename, full_info)
            old_commentary_len= new_commentary_len


        new_eov_len = len(over_details)
        if new_eov_len != old_eov_len:
            print("new end of over details..")
            local_time  = time.localtime()
            local_time = time.strftime('%Y_%m_%d_%H:%M:%S', local_time)
            info = {}
            info['timestamp'] = local_time
            info['eov_info']=over_details
            #commentary_lines.insert(0, local_time)
            full_info.append(info)
            append_to_json(filename, full_info)
            old_eov_len= new_eov_len

        seconds = seconds + 1
        if seconds % 10 == 0:
            outfile.flush()
        time.sleep(frequency)
    outfile.close()
    print("Exited..")


# In[ ]:


# In[ ]:

def check_url_valid(url):
    print('url=', url)
    try:
        r = requests.head(url)
        print(r.status_code)
        # prints the int of the status code. Find more at httpstatusrappers.com :)
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

def get_match_id(url):
    ms = url.split('matchId=')
    ms =ms[1].split('&')
    return ms[0]

def get_club_id(url):
    ms = url.split('clubId=')
    ms =ms[1].split('&')
    return ms[0]

# innings is an array of dictionaries. It is organized as follows:
# len(innings) : should be 2, one for each innings
# Each innings element is a dictionary.
#     innings['commentary'] is an array of ball by ball commentary with time stamps
#     innings['overs'] is an array of end of over information
#     innings['team'] is the team that batted in this innings
#  
if __name__ == "__main__":
    match_id = 146
#    match_id=123
    club_id = 198
#    club_id=123
    frequency = 5
    hours = 5
    iterations= int(hours*60*60/frequency)
    #https://cricclubs.com/viewScorecard.do?&matchId=59&clubId=702
    local_time  = time.localtime()
    local_time = time.strftime('%Y_%m_%d_%H_%M_%S', local_time)
    fname = "match"+str(match_id)+"_club"+str(club_id)+"_"+local_time+".json"
    url = get_url(match_id, club_id)
    check_url_valid(url)
    save_live_match_content(url, iterations, frequency, filename=fname)
