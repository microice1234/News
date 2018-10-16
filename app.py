from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for, logging,flash,make_response
import requests
from newspaper import Article
#import nltk
#import datetime
import pymysql
from functools import wraps
import itertools

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

    return render_template('index.html', jsohome1=articlePageList)

@app.route("/category/<string:categ>/<string:pg>/")
def category(categ,pg):
    inserter = 'category=' + categ + '&page=' + pg + '&'
    prevpage = int(pg) - 1
    nextpage = int(pg) + 1

    url = 'https://newsapi.org/v2/top-headlines?'+inserter+'country=in&sortBy=publishedAt&apiKey=097f0f6fb89b43539cbaa31372c3f92d'

    r = requests.get(url)

    global jso
    global articlePageList
    articlePageList = []
    jso = r.json()
    articlePageList.append(r.json()['articles'])
    lastpage = int(jso['totalResults'] / 20 + 1)
    return render_template('results.html', jso=jso, articlePageList=articlePageList, pg=pg, userReq=categ, prevpage=prevpage, nextpage=nextpage, lastpage=str(lastpage))


@app.route("/search/<string:pg>/", methods=['GET'])
def search(pg):
    userReq = request.args.get('query')
    inserter = 'q='+userReq+'&page='+pg+'&'
    prevpage = int(pg) - 1
    nextpage = int(pg) + 1

    url = 'https://newsapi.org/v2/everything?'+inserter+'sortBy=publishedAt&language=en&apiKey=097f0f6fb89b43539cbaa31372c3f92d'

    r = requests.get(url)

    global jso
    global articlePageList
    articlePageList = []
    jso = r.json()
    print(jso)
    articlePageList.append(r.json()['articles'])
    lastpage = int(jso['totalResults']/20 + 1)

    return render_template('results.html', jso=jso, articlePageList=articlePageList, pg=pg, userReq=userReq, prevpage=prevpage, nextpage=nextpage, lastpage=str(lastpage))

@app.route("/article/<string:title>")
def article(title):
    global articlePageList
    neededUrl = ''
    neededImgUrl = ''
    indexOfArticleCategory = 0
    flag = 0
    categoryCount = 0
    for articleList in articlePageList:
        categoryCount+=1
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
        neededImgUrl = "notPresent"


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
        neededImgUrl = "notPresent"

    ### Recommendations ###
    listofpreff = []
    articlePageListRec = []
    global zipper
    if session['logged_in'] == True:
        uid = session['uid']

        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = "SELECT * FROM prefferences WHERE id = %s"
            result = cur.execute(sql, (uid))
        connection.commit()

        if result > 0:
            # Get stored hash
            preff = cur.fetchall()
            for i in preff:
                listofpreff = listofpreff + [i['category']]

            for prefference in listofpreff:
                url = 'https://newsapi.org/v2/everything?language=en&pageSize=3&page=1&q=' + prefference + '&apiKey=097f0f6fb89b43539cbaa31372c3f92d'
                r = requests.get(url)
                articlePageListRec.append(r.json()['articles'])
        cur.close()
    zipper = zip(articlePageListRec, listofpreff)

    return render_template('article.html',summary=summary, title = title, index=indexOfArticleCategory,  neededImgUrl = neededImgUrl, movies=movies, date = dateStr, articleUrl = url, jso = articlePageList, zipper=zipper)

#Check if logged out
def is_logged_out(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

@app.route("/register", methods=['GET', 'POST'])
@is_logged_out
def register():
    if request.method == 'POST':
        first_name = request.form['fname']
        last_name = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        country = request.form['examplecountry']
        contactNo = request.form['examplecontact']

        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor(pymysql.cursors.DictCursor) as cur:
            sql = "SELECT * FROM person WHERE email = %s"
            result = cur.execute(sql, (email))
        connection.commit()

        if result == 0:
            connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
            with connection.cursor() as cur:
                sql = "INSERT INTO person (first_name, last_name, email, password, country, contactNo) VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (first_name, last_name, email, password, country, contactNo))
            connection.commit()
            cur.close()
            flash('You have successfully registered.', 'success')

            return redirect(url_for('login'))
        else:
            error = 'An account with this email id already exists'
            cur.close()
            return render_template('register.html', error=error)

    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
@is_logged_out
def login():
    remember = request.cookies.get('uid')
    print('remember=',remember)
    if request.method == 'POST':
        # Get Form Fields
        emailid = request.form['emailid']
        password_candidate = request.form['password']
        checkvalue = request.form.getlist('remember')
        print('check=',checkvalue)

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

                if checkvalue:
                    resp = make_response(redirect(url_for('index')))
                    resp.set_cookie('uid', str(uid), max_age = 86400)
                    cur.close()
                    return resp

                cur.close()
                return redirect(url_for('index'))

            else:
                error = 'Password incorrect'
                cur.close()
                return render_template('login.html', error=error)

        else:
            error = 'No account with this Email exists.'
            cur.close()
            return render_template('login.html', error=error)

    remembered = request.cookies.get('uid')
    print('rem = ', remembered)
    if remembered:
        session['logged_in'] = True
        session['uid'] = remembered

        flash('You are now logged in', 'success')
        resp = make_response(redirect(url_for('index')))
        resp.set_cookie('uid', str(remembered), max_age=86400)
        return resp

    return render_template('login.html')


#Check if logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You must login to view this page!', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('uid', '', max_age=86400)
    flash('You are now logged out', 'success')
    return resp

@app.route("/profile", methods=['GET', 'POST'])
@is_logged_in
def profile():
    uid = session['uid']
    listofpreff = []
    #TO update
    if request.method == 'POST':
        email = request.form['editEmail']
        password = request.form['editPassword']
        contactNo = request.form['editContactNo']
        preffList = request.form.getlist('prefflist')
        customCateg = request.form['customCategory']
        connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
        with connection.cursor() as cur:
            sql = "UPDATE person SET email = %s, password = %s, contactNo = %s WHERE id = %s"
            cur.execute(sql, (email, password, contactNo, uid))
        connection.commit()

        cur.close()

        if customCateg!='':
            connection = pymysql.connect(host='localhost', user='root', password='', db='allinonenews')
            with connection.cursor() as cur:
                sql = "INSERT into recommendations VALUES (%s)"
                cur.execute(sql, (customCateg))
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

    with connection.cursor(pymysql.cursors.DictCursor) as cur:
        sql = "SELECT * FROM recommendations"
        result = cur.execute(sql)
    connection.commit()
    if result > 0:
        # Get stored hash
        recom = cur.fetchall()
        listofrecom = []
        for i in recom:
           listofrecom = listofrecom + [i['categories']]
    cur.close()
    print(listofrecom)
    return render_template('profile.html',fname=fname,lname=lname,email=email,country=country,contactNo=contactNo, password=password, listofpreff=listofpreff, listofrecom=listofrecom)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
    app.run(debug=True)

