import urllib.request
import re

#Created by Ishan Waykul


#Parameters:
 # @link: a movie/tv show's URL
#Returns:
 # * htmlText: the html code for respective work of art
def preprocessing(link):
    new_request = urllib.request.Request(str(link))
    response = urllib.request.urlopen(new_request)
    htmlLog = response.read()
    htmlText = htmlLog.decode(errors="replace")
    return htmlText

def findMovieFeatures(html_block):
    dual = []
    titleStart = html_block.find("<title>")
    titleEnd = html_block.find("</title>")
    endOfName = html_block.find("(", titleStart)
    movie = html_block[titleStart+7: endOfName].strip()
    #print(movie)
    plotSumTag = html_block.find("Storyline")
    descriptionStart = html_block.find('div class="inline canwrap"', plotSumTag)
    synopsisStart = html_block.find("<p>", descriptionStart)
    synopsisEnd = html_block.find("<em", synopsisStart)
    imdbRatingStart = html_block.find("strong title=")
    imdbRatingEnd = html_block.find(" b", imdbRatingStart)
    genreStart = html_block.find('Genres:')
    genreEnd = html_block.find("</div>", genreStart)
    currIndex = genreStart
    sourceCode = html_block[genreStart:genreEnd]
    genreList = []
    while (currIndex != -1):
        firsGen = html_block.find("gnr", currIndex)
        currIndex = firsGen
        enGen = html_block.find("<", currIndex)
        currIndex = enGen
        if (firsGen != enGen):
            genreList.append(html_block[firsGen+7:enGen])
        #print("~~~~~")

    #current = genreStart
    #genreList = []
    #current = genreStart
    #find = 0

    genreIndex = sourceCode.find("</a>")
    curr = genreIndex
    start = 0
    #print(sourceCode)
    #print(genreIndex)
    dual.append(movie)
    dual.append(float(html_block[imdbRatingStart+14:imdbRatingEnd]))
    dual.append(genreList)
    dual.append(html_block[synopsisStart+4: synopsisEnd].strip())
    #print(dual)
    #print("~~~~~~")
    return dual



def ret_movie_set():
    movieList = []
    link = "http://www.imdb.com/search/title?genres=drama&groups=top_250&sort=user_rating,desc"
    htmlScript = preprocessing(link)
    findID = re.findall(r'a href="/title/tt[0-9]*/[?=\w]*', htmlScript)
    #print(findID[0][7:len(findID[0])])
    for movLink in findID:
        movLink = movLink[7:len(movLink)]
        if "vote" not in movLink:
            movieList.append(movLink)
    return set(movieList)



def ret_movie_dict(movString):
    movie2summary = {}
    movieSet = ret_movie_set()
    #preString = "http://www.imdb.com"
    # http://www.imdb.com/title/tt0095327/?ref_=adv_li_i
    #concatenate_link = preString + movie[1: len(movie)]
    #curr_movie_link = preprocessing(concatenate_link)
    dual = findMovieFeatures(movString)
    movie2summary[dual[0]] = dual[1]
    return movie2summary

def get_webscrape_top_movies():
    movieDict = {}
    page_links = []
    features = []    #(Name, Score, Genre, Summary)
    preNum = "http://www.imdb.com/search/title?groups=top_250&sort=user_rating,desc&view=advanced&page="
    postNum =   "&ref_=adv_prv"
    html_page = preprocessing("http://www.imdb.com/chart/top")
    return get_movie_features(html_page)


def get_movie_features(codeblock):

    # 1. get movie name
    movList = []
    movie_to_summary = {}
    movie_links = re.findall(r'(/tt{1}[0-9]{7})+', codeblock)
    movie_list = []
    for m in movie_links:
        movie = "http://www.imdb.com/title" + m + "/"
        movie_list.append(movie)
    movSet = set(movie_list)
    count = 1
    #print(len(movSet))
    for item in movSet:
        print(count)
        preprocessed_movie_link = preprocessing(item)
        dual = findMovieFeatures(preprocessed_movie_link)
        movie_to_summary[count] = dual
        count += 1
    return movie_to_summary

#testMovFeats = findMovieFeatures(preprocessing("http://www.imdb.com/title/tt0099429/"))
#print(testMovFeats)
get_webscrape_top_movies()
