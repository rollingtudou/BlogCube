from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import or_, extract, func

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    articles = db.relationship('Article', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='article', lazy=True)

@app.route('/')
def home():
    articles = Article.query.order_by(Article.created_at.desc()).all()
    return render_template('home.html', articles=articles)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('home'))
        flash('用户名或密码错误！', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash('两次输入的密码不一致！', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(username=request.form['username']).first():
            flash('用户名已存在！', 'error')
            return render_template('register.html')
            
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请登录。')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form.get('category', '')
        
        if not title or not content:
            flash('标题和内容不能为空！', 'error')
            return render_template('create.html')
        
        article = Article(
            title=title,
            content=content,
            category=category,
            author_id=current_user.id
        )
        db.session.add(article)
        db.session.commit()
        
        flash('文章发布成功！')
        return redirect(url_for('article', article_id=article.id))
    return render_template('create.html')

@app.route('/article/<int:article_id>')
def article(article_id):
    article = Article.query.get_or_404(article_id)
    article.views += 1
    db.session.commit()
    return render_template('article.html', article=article)

@app.route('/article/<int:article_id>/comment', methods=['POST'])
@login_required
def comment(article_id):
    content = request.form['content']
    
    if not content:
        flash('评论内容不能为空！', 'error')
        return redirect(url_for('article', article_id=article_id))
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        article_id=article_id
    )
    db.session.add(comment)
    db.session.commit()
    
    flash('评论发布成功！')
    return redirect(url_for('article', article_id=article_id))

@app.route('/article/<int:article_id>/delete', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    if article.author_id != current_user.id:
        flash('你没有权限删除这篇文章！', 'error')
        return redirect(url_for('article', article_id=article_id))
    
    # 删除文章的所有评论
    Comment.query.filter_by(article_id=article_id).delete()
    db.session.delete(article)
    db.session.commit()
    
    flash('文章已删除！')
    return redirect(url_for('home'))

@app.route('/article/<int:article_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    if article.author_id != current_user.id:
        flash('你没有权限编辑这篇文章！', 'error')
        return redirect(url_for('article', article_id=article_id))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            flash('标题和内容不能为空！', 'error')
            return render_template('edit_article.html', article=article)
        
        article.title = title
        article.content = content
        db.session.commit()
        
        flash('文章更新成功！')
        return redirect(url_for('article', article_id=article_id))
    
    return render_template('edit_article.html', article=article)

@app.route('/like/<int:article_id>', methods=['POST'])
@login_required
def like_article(article_id):
    article = Article.query.get_or_404(article_id)
    article.likes += 1
    db.session.commit()
    return jsonify({'likes': article.likes})

# 添加评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    user = db.relationship('User', backref='comments')

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.get_or_404(user_id)
    articles = Article.query.filter_by(author_id=user_id).order_by(Article.created_at.desc()).all()
    return render_template('profile.html', user=user, articles=articles)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    articles = Article.query.filter(
        or_(
            Article.title.contains(query),
            Article.content.contains(query)
        )
    ).all()
    return render_template('search.html', articles=articles, query=query)

@app.route('/archives')
def archives():
    articles = db.session.query(
        extract('year', Article.created_at).label('year'),
        extract('month', Article.created_at).label('month'),
        func.count(Article.id).label('count')
    ).group_by(
        extract('year', Article.created_at),
        extract('month', Article.created_at)
    ).order_by(
        extract('year', Article.created_at).desc(),
        extract('month', Article.created_at).desc()
    ).all()
    
    # 获取每个时间段的文章列表
    archive_data = []
    for year, month, count in articles:
        period_articles = Article.query.filter(
            extract('year', Article.created_at) == year,
            extract('month', Article.created_at) == month
        ).order_by(Article.created_at.desc()).all()
        
        archive_data.append({
            'year': int(year),
            'month': int(month),
            'count': count,
            'articles': period_articles
        })
    
    return render_template('archives.html', archives=archive_data)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(debug=True)