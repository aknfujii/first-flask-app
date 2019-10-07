from flask import request,redirect,url_for,render_template,flash,session
from flask_blog import app,db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from flask import Blueprint

entry=Blueprint('entry',__name__)#そのほかの場所からBlueprintアプリをentryという名前で参照できる…　@entry.route

@entry.route('/')#URLにアクセスがあった時の処理　ここにアクセスあった時にメソッドが呼ばれる
@login_required
def show_entries():
    entries=Entry.query.order_by(Entry.id.desc()).all()#新しく記事がつくられた順に並べる
    return render_template('entries/index.html',entries=entries)#index.html内でentriesで参照できるようにする

@entry.route('/entries/new', methods=['GET'])
@login_required
def new_entry():
    return render_template('entries/new.html')

@entry.route('/entries', methods=['POST'])
@login_required
def add_entry():
    entry = Entry(
        title=request.form['title'],
        text=request.form['text']
    )
    db.session.add(entry)
    db.session.commit()
    flash('新しく記事が作成されました')
    return redirect(url_for('entry.show_entries'))

@entry.route('/entries/<int:id>', methods=['GET'])  #intじゃないとエラーにする
@login_required
def show_entry(id):
    entry = Entry.query.get(id)
    return render_template('entries/show.html',entry=entry)

@entry.route('/entries/<int:id>/edit', methods=['GET'])
@login_required
def edit_entry(id):
    entry=Entry.query.get(id)
    return render_template('entries/edit.html', entry=entry)
    
@entry.route('/entries/<int:id>/update', methods=['POST'])
@login_required
def update_entry(id):
    entry = Entry.query.get(id)
    entry.title = request.form['title']
    entry.text = request.form['text']
    db.session.merge(entry)
    db.session.commit()
    flash('記事が更新されました')
    return redirect(url_for('entry.show_entries'))

@entry.route('/entries/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    entry = Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('記事が削除されました')
    return redirect(url_for('entry.show_entries'))

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries=Entry.query.order_by(Entry.id.desc()).all()
    if query:
        return render_template('entires/search.html', entries=entries, query=query)
    # return render_template('entires/search.html')
    return redirect(url_for('entry.show_entries'))
