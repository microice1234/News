from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, logging,flash
import requests
from newspaper import Article
#import nltk
#import datetime
import pymysql
from passlib.hash import sha256_crypt

app = Flask(__name__, static_folder='static')

jso = None
jsohome = None
articlePageList = []

@app.route("/", methods=['GET','POST'])
def index():

    global jsohome
    global articlePageList
    articlePageList = []

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=5&page=1&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=science&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=sports&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=technology&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=entertainment&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=business&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    url1 = 'https://newsapi.org/v2/top-headlines?country=in&pageSize=15&page=1&category=health&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
    r = requests.get(url1)
    articlePageList.append(r.json()['articles'])

    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        country = request.form['examplecountry']
        contactNo = request.form['examplecontact']

        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor() as cur:
            sql = "INSERT INTO person (first_name, last_name, email, password, country, contactNo) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (first_name, last_name, email, password, country, contactNo))
        connection.commit()

        cur.close()

    return render_template('index.html', jsohome1=articlePageList)

@app.route("/category/<string:categ>/<string:pg>/")
def category(categ,pg):
    inserter = 'category=' + categ + '&page=' + pg + '&'
    prevpage = int(pg) - 1
    nextpage = int(pg) + 1

    url = 'https://newsapi.org/v2/top-headlines?'+inserter+'from=2018-09-12&country=in&sortBy=publishedAt&apiKey=097f0f6fb89b43539cbaa31372c3f92d'

    r = requests.get(url)

    global jso
    global articlePageList
    articlePageList = []
    jso = r.json()
    articlePageList.append(r.json()['articles'])
    # session['req'] = 'yes'
    lastpage = int(jso['totalResults'] / 20 + 1)
    return render_template('results.html', jso=jso, articlePageList=articlePageList, pg=pg, userReq=categ, prevpage=prevpage, nextpage=nextpage, lastpage=str(lastpage))


@app.route("/search/<string:pg>/", methods=['GET'])
def search(pg):
    userReq = request.args.get('query')
    inserter = 'q='+userReq+'&page='+pg+'&'
    prevpage = int(pg) - 1
    nextpage = int(pg) + 1

    url = 'https://newsapi.org/v2/everything?'+inserter+'from=2018-09-12&sortBy=publishedAt&language=en&apiKey=097f0f6fb89b43539cbaa31372c3f92d'

    r = requests.get(url)

    global jso
    global articlePageList
    articlePageList = []
    jso = r.json()
    articlePageList.append(r.json()['articles'])
    #session['req'] = 'yes'
    lastpage = int(jso['totalResults']/20 + 1)

    return render_template('results.html', jso=jso, articlePageList=articlePageList, pg=pg, userReq=userReq, prevpage=prevpage, nextpage=nextpage, lastpage=str(lastpage))

@app.route("/article/<string:title>")
def article(title):
    global articlePageList
    neededUrl = ''
    neededImgUrl = ''
    indexOfArticleCategory = 0
    flag = 0
    for articleList in articlePageList:
        for item in articleList:
            if item['title']== title:
                neededUrl = item['url']
                neededImgUrl = item['urlToImage']
                flag = 1
                break
        if flag == 1:
            break
        indexOfArticleCategory+=1
    #nltk.download('punkt')
    url = neededUrl
    article = Article(url)
    article.download()
    try:
        article.parse()
    except:
        neededImgUrl = "url_for('static',filename='img/something-went-wrong.gif')"


    article.nlp()
    summary = article.summary
    movies = article.movies
    publishDate = article.publish_date
    if publishDate != None:
        dateStr = publishDate.strftime('%d, %B %Y')
    else:
        dateStr = '-'

    if movies == []:
        movies = ''

    if neededImgUrl == None:
        neededImgUrl = "url_for('static',filename='img/something-went-wrong.gif')"

    print(neededImgUrl)
    return render_template('article.html',summary=summary, title = title,  neededImgUrl = neededImgUrl, movies=movies, date = dateStr, articleUrl = url, jso = articlePageList, index=indexOfArticleCategory)

'''
@app.route("/dbtest")
def dbtest():
    connection = pymysql.connect(host='localhost',user='root',password='',db='allinonenews')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM person")
        all1 = cursor.fetchall()
        print(all1)
    return "success"
'''
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    uid = session['uid']
    listofpreff = []
    #TO update
    if request.method == 'POST':
        email = request.form['editEmail']
        password = request.form['editPassword']
        contactNo = request.form['editContactNo']
        preffList = request.form.getlist('prefflist')
        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor() as cur:
            sql = "UPDATE person SET email = %s, password = %s, contactNo = %s WHERE id = %s"
            cur.execute(sql, (email, password, contactNo, uid))
        connection.commit()

        cur.close()
        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor() as cur:
            sql = "DELETE FROM prefferences WHERE id = %s"
            cur.execute(sql, (uid))
            for categ in preffList:
                sql = "INSERT into prefferences (id, category) VALUES (%s,%s)"
                cur.execute(sql, (uid, categ))
        connection.commit()

        cur.close()

    #to display
    connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
    with connection.cursor(pymysql.cursors.DictCursor) as cur:
        sql = "SELECT * FROM person WHERE id = %s"
        result = cur.execute(sql, (uid))
    connection.commit()

    if result > 0:
        # Get stored hash
        data = cur.fetchone()
        password = data['password']
        fname = data['first_name']
        lname = data['last_name']
        email = data['email']
        country = data['country']
        contactNo = data['contactNo']

    with connection.cursor(pymysql.cursors.DictCursor) as cur:
        sql = "SELECT * FROM prefferences WHERE id = %s"
        result = cur.execute(sql, (uid))
    connection.commit()
    if result > 0:
        # Get stored hash
        preff = cur.fetchall()
        listofpreff = []
        for i in preff:
           listofpreff = listofpreff + [i['category']]
    cur.close()
    return render_template('profile.html',fname=fname,lname=lname,email=email,country=country,contactNo=contactNo, password=password, listofpreff=listofpreff)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        emailid = request.form['emailid']
        password_candidate = request.form['password']
        checkvalue = request.form.get('remember')

        # Create cursor
        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = "SELECT * FROM person WHERE email = %s"
            result = cur.execute(sql, (emailid))
        connection.commit()

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            passwordDb = data['password']
            uid = data['id']
            # Compare Passwords
            if password_candidate == passwordDb:
                # Passed
                session['logged_in'] = True
                session['uid'] = uid

                flash('You are now logged in', 'success')
                '''
                if checkvalue:
                    resp = make_response(render_template('login.html'))
                    resp.set_cookie('emailid', 'emailid', max_age = 86400)
                    resp.set_cookie('password', 'password_candidate', max_age=86400)
                '''
                cur.close()
                return redirect(url_for('index'))

            else:
                error = 'Invalid login'
                cur.close()
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            cur.close()
            return render_template('login.html', error=error)

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run(debug=True)

