# app.py - Main Flask Application

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime
import folium


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key in production

# Data storage - in a real application, you would use a database
DATA_FILE = 'data/portfolio.json'

def load_data():
    """Load portfolio data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        
        # Return default data
        return {
            "personal_info": {
                "name": "Sverre Torp",
                "title": "Cybernetic/Data Engineer",
                "bio": "I'm a passionate developer with expertise in modern technologies.",
                "email": "anders.ullsfoss.torp@example.com",
                "phone": "+47 97736430",
                "location": "Oslo, NO",
                "social": {
                    "github": "https://github.com/gitders222",
                    "linkedin": "https://linkedin.com/in/yourusername",
                    "twitter": "https://twitter.com/yourusername"
                }
            },
            "projects": [
                {
                    "id": 1,
                    "title": "GIS-map",
                    "description": "A full-featured e-commerce platform with payment processing.",
                    "technologies": ["Python", "Flask", "JavaScript", "PostgreSQL"],
                    "image": "ecommerce.jpg",
                    "github_link": "https://github.com/yourusername/ecommerce",
                    "live_link": "https://ecommerce-demo.example.com",
                    "featured": True
                },
                {
                    "id": 2,
                    "title": "Task Management App",
                    "description": "A productivity app for managing daily tasks and projects.",
                    "technologies": ["Python", "Django", "React", "MongoDB"],
                    "image": "taskmanager.jpg",
                    "github_link": "https://github.com/yourusername/taskmanager",
                    "live_link": "https://taskmanager-demo.example.com",
                    "featured": True
                }
            ],
            "skills": [
                {"name": "Python", "level": 90},
                {"name": "JavaScript", "level": 85},
                {"name": "HTML/CSS", "level": 95},
                {"name": "Flask", "level": 80},
                {"name": "React", "level": 75},
                {"name": "SQL", "level": 70}
            ],
            "experience": [
                {
                    "company": "Tech Solutions Inc.",
                    "position": "Senior Web Developer",
                    "period": "2020 - Present",
                    "description": "Lead developer for client web applications."
                },
                {
                    "company": "Digital Agency",
                    "position": "Web Developer",
                    "period": "2018 - 2020",
                    "description": "Designed and implemented responsive websites for clients."
                }
            ],
            "education": [
                {
                    "institution": "University of Technology",
                    "degree": "B.S. Computer Science",
                    "year": "2018",
                    "description": "Graduated with honors. Specialized in web technologies."
                }
            ],
            "testimonials": [
                {
                    "name": "Jane Smith",
                    "position": "CEO, Tech Solutions",
                    "text": "An exceptional developer who delivers quality work on time."
                },
                {
                    "name": "John Doe",
                    "position": "Project Manager, Digital Agency",
                    "text": "Great attention to detail and excellent problem-solving skills."
                }
            ],
            "blog_posts": [
                {
                    "id": 1,
                    "title": "Getting Started with Flask",
                    "date": "2023-01-15",
                    "summary": "Learn how to build web applications with Flask.",
                    "content": "Flask is a lightweight WSGI web application framework in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications..."
                },
                {
                    "id": 2,
                    "title": "The Power of JavaScript ES6",
                    "date": "2023-02-20",
                    "summary": "Exploring the modern features of JavaScript ES6.",
                    "content": "ECMAScript 2015 or ES6 brought significant changes to the JavaScript language. Let's explore some of the most powerful features that make coding in JavaScript more efficient..."
                }
            ]
        }

def save_data(data):
    """Save portfolio data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Context processor to add current year to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# Routes
@app.route('/')
def home():
    data = load_data()
    featured_projects = [p for p in data['projects'] if p.get('featured', False)]
    return render_template('index.html', 
                           info=data['personal_info'], 
                           featured_projects=featured_projects,
                           skills=data['skills'][:6])  # Show top skills on homepage

@app.route('/about')
def about():
    data = load_data()
    return render_template('about.html', 
                           info=data['personal_info'],
                           skills=data['skills'],
                           experience=data['experience'],
                           education=data['education'])

@app.route('/projects')
def projects():
    data = load_data()
    return render_template('projects.html', 
                           info=data['personal_info'],
                           projects=data['projects'])

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    data = load_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if project:
        return render_template('project_detail.html', 
                               info=data['personal_info'],
                               project=project)
    return redirect(url_for('projects'))

@app.route('/blog')
def blog():
    data = load_data()
    posts = sorted(data['blog_posts'], key=lambda x: x['date'], reverse=True)
    return render_template('blog.html', 
                           info=data['personal_info'],
                           posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    data = load_data()
    post = next((p for p in data['blog_posts'] if p['id'] == post_id), None)
    if post:
        return render_template('blog_post.html', 
                               info=data['personal_info'],
                               post=post)
    return redirect(url_for('blog'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    data = load_data()
    if request.method == 'POST':
        # In a real application, you would process the form and send an email
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Here you would typically send an email with the form data
        # For this example, we'll just flash a success message
        flash(f'Thank you {name}! Your message has been sent.', 'success')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', info=data['personal_info'])

@app.route('/testimonials')
def testimonials():
    data = load_data()
    return render_template('testimonials.html', 
                           info=data['personal_info'],
                           testimonials=data['testimonials'])

@app.route('/gis')
def gis():
    # Create a Folium map centered at a location
    m = folium.Map(location=[59.9127, 10.7460], zoom_start=3)

    # List of GeoJSON URLs
    geojson_urls = [
        "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/USA.geo.json",
        "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/NOR.geo.json",
        "https://raw.githubusercontent.com/johan/world.geo.json/master/countries/DEU.geo.json"
    ]

    # Loop through URLs and add GeoJSON layers
    for url in geojson_urls:
        folium.GeoJson(
            url,
            name=f"GeoJSON Layer {url.split('/')[-1].split('.')[0]}",  # Extracts country code as name
            tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Country"])
        ).add_to(m)

    # Add a Layer Control to toggle layers
    folium.LayerControl().add_to(m)

    # Save map to an HTML file
    map_html = "static/map.html"
    m.save(map_html)
    data = load_data()

    return render_template('gis.html', map_file=map_html, info=data['personal_info'])



# Admin routes (basic implementation - would need proper authentication in production)
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # In a real application, you would implement proper authentication here
    data = load_data()
    if request.method == 'POST':
        # Simple update of personal info
        personal_info = data['personal_info']
        personal_info['name'] = request.form.get('name', personal_info['name'])
        personal_info['title'] = request.form.get('title', personal_info['title'])
        personal_info['bio'] = request.form.get('bio', personal_info['bio'])
        personal_info['email'] = request.form.get('email', personal_info['email'])
        personal_info['phone'] = request.form.get('phone', personal_info['phone'])
        personal_info['location'] = request.form.get('location', personal_info['location'])
        
        save_data(data)
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin'))
        
    return render_template('admin/dashboard.html', info=data['personal_info'], data=data)

@app.template_filter('format_date')
def format_date(value, format='%B %d, %Y'):
    """Format a date string from YYYY-MM-DD to a more readable format"""
    if value:
        date_obj = datetime.strptime(value, '%Y-%m-%d')
        return date_obj.strftime(format)
    return ''

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    data = load_data()
    return render_template('error.html', 
                           info=data['personal_info'],
                           error_code=404,
                           error_message="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    data = load_data()
    return render_template('error.html', 
                           info=data['personal_info'],
                           error_code=500,
                           error_message="Internal server error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)