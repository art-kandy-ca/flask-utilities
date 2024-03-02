import sqlite3
from flask import Flask, render_template, request, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fksifjhajfoiwehfijvksdfilsnadfkjsdahijfvhnavli'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/frames_to_timecodes', methods=('GET', 'POST'))
def frames_to_timecodes():
	timecodes = ""
	if request.method == 'POST':		
		try:
			fps = float(request.form['fps'])
		except ValueError:
			fps = 0
			flash('FPS value is invalid!')
		
		if fps > 0:
			frames = request.form['frames']	
			frames = ''.join(frames)
			frames = frames.splitlines()
	
			if len(frames) > 0 and frames[0] != "0":
				frames.insert(0, 0)
	
			chapter = 1
			for frame in frames:
				try:
					frame = int(frame)
					sec_float = frame/fps
				except ValueError:
					flash("Frame {} value is invalid!".format(chapter))
					timecodes = ""
					break
			
				h = int(sec_float/60/60)
				sec_float -= h * 60 * 60
				m = int(sec_float/60)
				sec_float -= m * 60
				s = int(sec_float)
				sec_float -= s
				ms = int(sec_float * 1000)
				timecodes += "CHAPTER{chapter:02d}={h:02d}:{m:02d}:{s:02d}.{ms:03d}\r\nCHAPTER{chapter:02d}NAME=Chapter {chapter:d}\r\n".format(chapter=chapter,h=h,m=m,s=s,ms=ms)
				chapter+=1

	return render_template('frames_to_timecodes.html', timecodes=timecodes)