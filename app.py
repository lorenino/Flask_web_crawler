from flask import Flask, request, render_template, jsonify, redirect, url_for
from urllib.parse import urlparse
from web_crawler import crawl_site, save_data
from forms import CrawlForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    crawl_form = CrawlForm()
    if crawl_form.validate_on_submit():
        start_url = crawl_form.start_url.data
        parsed_url = urlparse(start_url)
        base_domain = parsed_url.netloc
        visited_pages = crawl_site(start_url, base_domain, crawl_form.max_workers.data)
        save_data(visited_pages, crawl_form.output_dir.data, base_domain)
        return redirect(url_for('success', action='crawled', num_pages=len(visited_pages)))
    return render_template('index.html', form=crawl_form)

@app.route('/success/<action>/<int:num_pages>')
def success(action, num_pages):
    return render_template('success.html', action=action, num_pages=num_pages)

if __name__ == '__main__':
    app.run(debug=True)
