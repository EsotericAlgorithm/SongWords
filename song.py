from flask import Flask
from flask import render_template, g
import os
import sqlite3
import tswift

app = Flask(__name__)

DATABASE=os.path.join(app.root_path, 'songs.db')


@app.route('/')
def show_songs():
    db = get_db();
    cursor = db.execute('SELECT id, title, artist, metro, youtube from songs')
    entries = cursor.fetchall()
    return render_template('index.html', songs=entries)

@app.route('/song/<song_id>')
def show_single_song(song_id):
    db = get_db();
    cursor = db.execute('SELECT title, artist, metro, youtube FROM songs WHERE id=?', song_id)
    entries = cursor.fetchall()[0] # take just the first result

    # Follows ordering of SQL statement, fragile
    title, artist, metro, youtube = entries

    # Fetch lyrics
    song = tswift.Song(url=metro)
    song.load()

    # Format Youtube link for embedding
 
    return render_template('song.html', title=title, artist=artist, metro=metro, youtube=youtube, lyrics=song.lyrics)

def connect_db():
    rv = sqlite3.connect(DATABASE)
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, DATABASE):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



@app.template_filter('youtube_link')
def youtube_link_filter(s):
    link = """https://www.youtube.com/watch?v={}"""
    return link.format(s)

@app.template_filter('youtube_embed')
def youtube_embed_filter(s):
    embed_link = """<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" frameborder="0" allowfullscreen></iframe>"""
    return embed_link.format(s)

@app.template_filter('newline_format')
def newline_format(s):
    return s.replace("\n", "<br>\n")
