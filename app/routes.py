from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import User, Anime, UserAnimeStatus
from .api import search_anime, get_anime_details

bp = Blueprint('main', __name__)

# Hardcoded default user ID for demo purposes
DEFAULT_USER_ID = 1

@bp.route('/')
def index():
    # Show random some anime or just all from DB
    animes = Anime.query.limit(20).all()
    return render_template('index.html', animes=animes)

@bp.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if query:
            # Query Jikan API
            api_results = search_anime(query)
            
            # Store in DB if not exists and map to list of anime objects
            for api_anime in api_results:
                anime = Anime.query.filter_by(mal_id=api_anime['mal_id']).first()
                if not anime:
                    anime = Anime(
                        mal_id=api_anime['mal_id'],
                        title=api_anime['title'],
                        synopsis=api_anime['synopsis'],
                        image_url=api_anime['image_url'],
                        rating=api_anime['rating']
                    )
                    db.session.add(anime)
                # Only add if we have an instance (should always be true here)
                if anime:
                    results.append(anime)
            db.session.commit()
            
    return render_template('search.html', results=results, query=query)

@bp.route('/anime/<int:anime_id>')
def detail(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    # Check if user has it in list
    status = UserAnimeStatus.query.filter_by(user_id=DEFAULT_USER_ID, anime_id=anime.id).first()
    return render_template('detail.html', anime=anime, status=status)

@bp.route('/rate/<int:anime_id>', methods=['POST'])
def rate(anime_id):
    anime = Anime.query.get_or_404(anime_id)
    new_status = request.form.get('status')
    
    if new_status in ['watching', 'completed', 'plan', 'remove']:
        status_record = UserAnimeStatus.query.filter_by(user_id=DEFAULT_USER_ID, anime_id=anime.id).first()
        if new_status == 'remove':
            if status_record:
                db.session.delete(status_record)
        else:
            if status_record:
                status_record.status = new_status
            else:
                status_record = UserAnimeStatus(user_id=DEFAULT_USER_ID, anime_id=anime.id, status=new_status)
                db.session.add(status_record)
        db.session.commit()
        
    return redirect(url_for('main.detail', anime_id=anime.id))

@bp.route('/profile')
def profile():
    user = User.query.get(DEFAULT_USER_ID)
    statuses = UserAnimeStatus.query.filter_by(user_id=DEFAULT_USER_ID).all()
    
    lists = {
        'watching': [],
        'completed': [],
        'plan': []
    }
    
    for s in statuses:
        if s.status in lists:
            lists[s.status].append(s.anime)
            
    return render_template('profile.html', user=user, lists=lists)

@bp.route('/login')
def login():
    return render_template('login.html')
