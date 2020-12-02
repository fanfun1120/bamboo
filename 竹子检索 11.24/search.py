from flask import Flask, render_template, request, url_for, redirect, flash

import pymysql
global Id, b_name, rod, leaf, sheath, othinfo, proposal
app = Flask(__name__)
app.secret_key = 'secret'

# 连接数据库
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='',
    db='bamboo',
    charset='utf8'
)
cur = conn.cursor()


def insert(content):
    global Id, b_name, rod, leaf, sheath, othinfo, proposal
    Id = content[0][0]
    b_name = content[0][1]
    rod = content[0][2] + content[0][3] + content[0][4]
    leaf = content[0][5]
    sheath = content[0][6]
    othinfo = content[0][7]
    proposal = content[0][8]
    return


def insert_2(content):
    global Id, b_name, rod, leaf, sheath, othinfo, proposal
    Id = content[0][9]
    b_name = content[0][10]
    rod = content[0][11] + content[0][12] + content[0][13]
    leaf = content[0][14]
    sheath = content[0][15]
    othinfo = content[0][16]
    proposal = content[0][17]
    return


# 连接前端与操作
@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/')
def first():
    return render_template('first.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    global Id, b_name, rod, leaf, sheath, othinfo, proposal
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        sql = f"select * from tbl_bamboo join tbl_bamboo_english on" \
              f" tbl_bamboo.id = tbl_bamboo_english.No where" \
              f" (tbl_bamboo.name = '{search}' or tbl_bamboo_english.name = '{search}')"
        cur.execute(sql)
        content = cur.fetchall()
        if len(content) > 0:
            insert(content)
            return redirect(url_for('retrieve'))
        else:
            flash(u'未找到此竹子')
    return redirect(url_for('first'))


@app.route('/retrieve/bamboo_picture_path/<int:Id>')
def bamboo_picture_path(Id):
    sql = f"select path from picture where id = '{Id}'"
    cur.execute(sql)
    content = cur.fetchall()
    path = content[0][0].split(';')
    prefix = '/static/picture'
    for i in range(len(path)):
        path[i] = prefix + path[i]
    return ";".join(path)


@app.route('/retrieve/<language>', methods=["GET", "POST"])
def language_conversion(language):
    global Id, b_name, rod, leaf, sheath, othinfo, proposal
    if request.method == 'GET':
        before = request.args.get('before')
        flag = before != language
        if language == 'chinese' and flag:
            sql = f"select * from tbl_bamboo where id = " \
                  f"(select No from tbl_bamboo_english where name = '{b_name}')"
            language = ''
        elif language == 'english' and flag:
            sql = f"select * from tbl_bamboo_english where No = " \
                  f"(select id from tbl_bamboo where name = '{b_name}')"
            language = '_' + language
        if flag:
            cur.execute(sql)
            content = cur.fetchall()
            insert(content)
        else:
            if language == 'chinese':
                language = ''
            else:
                language = '_' + language
        return render_template(f'retrieve{language}.html', Id=Id, b_name=b_name, rod=rod, leaf=leaf, sheath=sheath, othinfo=othinfo,
                               proposal=proposal)
    else:
        search = request.form.get('search')
        sql = f"select * from tbl_bamboo join tbl_bamboo_english on" \
              f" tbl_bamboo.id = tbl_bamboo_english.No where" \
              f" (tbl_bamboo.name = '{search}' or tbl_bamboo_english.name = '{search}')"
        cur.execute(sql)
        content = cur.fetchall()
        print(content)
        if len(content) > 0:
            if language == 'chinese':
                language = ''
                insert(content)
            else:
                language = '_' + language
                insert_2(content)
            return render_template(f'retrieve{language}.html', Id=Id, b_name=b_name, rod=rod, leaf=leaf, sheath=sheath,
                                   othinfo=othinfo,
                                   proposal=proposal)
        else:
            if language == 'chinese':
                flash('未找到此竹子')
            elif language == 'english':
                flash('No bamboo was found')
            if language == 'chinese':
                language = ''
            else:
                language = '_' + language
            return render_template(f'retrieve{language}.html')


@app.route('/retrieve')
def retrieve():
    return render_template('retrieve.html', Id=Id, b_name=b_name, rod=rod, leaf=leaf, sheath=sheath, othinfo=othinfo,
                           proposal=proposal)


@app.route('/retrieve', methods=['GET', 'POST'])
def ser_index():
    if request.method == 'POST':
        search = request.form.get('search')
        print(search)
        sql = f"select * from tbl_bamboo join tbl_bamboo_english on" \
              f" tbl_bamboo.id = tbl_bamboo_english.No where" \
              f" (tbl_bamboo.name = '{search}' or tbl_bamboo_english.name = '{search}')"
        cur.execute(sql)
        content = cur.fetchall()
        if len(content) > 0:
            insert(content)
            return render_template('retrieve.html', Id=Id, b_name=b_name, rod=rod, leaf=leaf, sheath=sheath, othinfo=othinfo,
                                   proposal=proposal)
        else:
            flash('未找到此竹子')
    return render_template('retrieve.html')


if __name__ == '__main__':
    app.run(debug=True)
