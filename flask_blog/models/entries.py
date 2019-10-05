from flask_blog import db
from datetime import datetime


class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),unique=True)#50文字,重複させない
    text = db.Column(db.Text)#大量のテキスト
    created_at = db.Column(db.DateTime)
    
    def __init__(self, title=None, text=None):#モデルが作成されたときの処理
        self.title = title
        self.text = text
        self.created_at = datetime.utcnow()

    def __repr__(self):#記事が参照されたときのコンソールでの出力形式
        return '<Entry id:{} title:{} text:{}>'.format(self.id,self.title,self.text)
        