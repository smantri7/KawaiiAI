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
            if ((enGen)-(firsGen+7) < 20):
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
    dual.append(remove_leftover_code(html_block[synopsisStart+4: synopsisEnd].strip()))
    #dual.append(html_block[synopsisStart+4: synopsisEnd].strip())
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
    preNum = "http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page="
    postNum =   "&ref_=adv_prv"
    #html_page = preprocessing("http://www.imdb.com/chart/top")
    for page in range(0,1):
        largeString = preNum + str(page+1) + postNum
        html_page = preprocessing(largeString)
        movList = get_movie_features(html_page)
    return movieDict
    

#removes unnecessary html tags for actors/actresses

def remove_leftover_code(codeblock):
    iteration = 1
    codeblock.replace("\'", "'")
    #codeblock.replace('"', '8')
    while(True):
        #print("--------------------------")
        #print("iteration: ", iteration)
        #print(codeblock)
        indexStart = codeblock.find("<a href")
        indexEnd = codeblock.find(">", indexStart)
        if (indexStart == -1 or indexEnd == -1):
            
            return codeblock
        editedblock = codeblock[0:indexStart] + codeblock[indexEnd+1:len(codeblock)]
        secondStart = editedblock.find("<")
        secondEnd = editedblock.find(">")
        finalEdit = editedblock[0:secondStart] + editedblock[secondEnd+1:len(editedblock)]
        codeblock = finalEdit
        iteration += 1
    
#print(testString)                                                                                                                       
#editedString = remove_leftover_code(testString)
#print(editedString)

def get_movie_features(codeblock):
    count = 1
    # 1. get movie name
    movList = []
    movie_to_summary = {}
    movie_links = re.findall(r'(/tt{1}[0-9]{7})+', codeblock)
    
    movie_list = []
    for m in movie_links:
        movie = "http://www.imdb.com/title" + m + "/"
        movie_list.append(movie)
    movSet = set(movie_list)
    print(movSet)
    return 0
    
    #print(len(movSet))
    for item in movSet:
        #print(count)
        if (count > 50):
            return movList
        preprocessed_movie_link = preprocessing(item)
        dual = findMovieFeatures(preprocessed_movie_link)
        #print(dual)
        movList.append(dual)
        count += 1
        #print(count)
    return movList
        



#testMovFeats = findMovieFeatures(preprocessing("http://www.imdb.com/title/tt0099429/"))
#print(testMovFeats)

topDictMovies = get_webscrape_top_movies()
#print(len(topDictMovies))
def get_movie_by_genre(movie_data):
    pass

