import re
import urllib.request
import csv
import codecs


def noAscii(string): 
    return ''.join([i if ord(i) < 128 else ' ' for i in string]).strip()

def array2file(arr, count):
    #print(count)
##    if (count == 0):
##        #print("START")
##        f = open("avatarScripts.csv", "w")
##    else:
##        f = open("avatarScripts.csv", "a")
##    writer = csv.writer(f)
    f = open("movie_lines.csv", "a")
    writer = csv.writer(f)
    for y in range(0, len(arr)-1):
        if (len(arr[y]) > 0 or len(arr[y+1]) > 0):
            writer.writerow([noAscii(arr[y]), noAscii(arr[y+1])])
    f.close()

def preprocessing(link):
    new_request = urllib.request.Request(str(link))
    response = urllib.request.urlopen(new_request)
    htmlLog = response.read()
    htmlText = htmlLog.decode(errors="replace")
    return htmlText

def webscrape(link, count):
    #print("-------------")
    htmlTxt = preprocessing(link)
    s = htmlTxt.find("world.")
    e = htmlTxt.find("<br>", s)
    ee = htmlTxt.find("<br>", e+4)
    line = htmlTxt[e:ee]
    s = ee
    dist2div = htmlTxt.find("</div>", ee) - ee
    epquotes = []
    while (dist2div > 15 and len(line) < 500):
        e = htmlTxt.find("<br>", s)
        ee = htmlTxt.find("<br>", e+4)
        line = htmlTxt[e+4:ee]
        dist2div = htmlTxt.find("</div>", ee) - ee
        epquotes.append(line)
        s = ee
    #print("COUNT: ", count)
    #print(len(epquotes))
    epquotes[len(epquotes)-1] = ""
    epquotes = [""] + epquotes
    array2file(epquotes, count)
    
    

    

def makelen2String(n):
    if (n < 10):
        return "0" + str(n)
    return str(n)
    



def scrapeItUp():
    seasons = ["01", "02", "03"]
    s1 = []
    s2 = []
    s3 = []



    for x in range(1, 21):
        s1.append(makelen2String(x))
    for y in range(1, 21):
        s2.append(makelen2String(y))
    for z in range(1, 22):
        s3.append(makelen2String(z))


    # https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=avatar-the-last-airbender&episode=s01e01
    season2ep = {"01": s1, "02": s2, "03": s3}
    #print(season2ep)


    count = 0
    for key in season2ep:
        eptitle = "https://www.springfieldspringfield.co.uk/view_episode_scripts.php?tv-show=avatar-the-last-airbender&episode=s" + key
        for ep in season2ep[key]:
            epnum = "e" + ep
            full_title = eptitle + epnum
            webscrape(full_title, count)
            count = count + 1


#sun = noAscii("â« Winter, spring, summer and fall.")
#print(sun)
scrapeItUp()


