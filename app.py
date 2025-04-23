from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from urllib.parse import urlparse

from config import Config
from models import db, User, Resource, Request, Allocation
from algorithms import allocate_resources

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create tables within app context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    resources = Resource.query.filter(
        Resource.available_to >= datetime.utcnow()
    ).order_by(Resource.created_at.desc()).limit(5).all()

    return render_template('index.html', resources=resources)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first() is not None:
            flash('Username already taken')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first() is not None:
            flash('Email already registered')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=request.form.get('remember_me'))
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/resources')
def resources():
    category = request.args.get('category')
    if category:
        resources = Resource.query.filter_by(category=category).all()
    else:
        resources = Resource.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/resources/add', methods=['GET', 'POST'])
@login_required
def add_resource():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        available_from = datetime.strptime(request.form.get('available_from'), '%Y-%m-%dT%H:%M')
        available_to = datetime.strptime(request.form.get('available_to'), '%Y-%m-%dT%H:%M')

        resource = Resource(
            name=name,
            description=description,
            category=category,
            available_from=available_from,
            available_to=available_to,
            owner=current_user
        )

        db.session.add(resource)
        db.session.commit()

        flash('Resource added successfully!')
        return redirect(url_for('resources'))

    return render_template('add_resource.html')

@app.route('/requests')
@login_required
def view_requests():
    user_requests = Request.query.filter_by(requester=current_user).all()
    return render_template('requests.html', requests=user_requests)

@app.route('/requests/add', methods=['GET', 'POST'])
@login_required
def add_request():
    if request.method == 'POST':
        resource_type = request.form.get('resource_type')
        needed_from = datetime.strptime(request.form.get('needed_from'), '%Y-%m-%dT%H:%M')
        needed_to = datetime.strptime(request.form.get('needed_to'), '%Y-%m-%dT%H:%M')
        priority = int(request.form.get('priority'))

        new_request = Request(
            resource_type=resource_type,
            needed_from=needed_from,
            needed_to=needed_to,
            priority=priority,
            requester=current_user
        )

        db.session.add(new_request)
        db.session.commit()

        flash('Request added successfully!')
        return redirect(url_for('view_requests'))

    return render_template('add_request.html')

@app.route('/allocate')
@login_required
def run_allocation():
    # Get all active resources and pending requests
    active_resources = Resource.query.filter(
        Resource.available_to >= datetime.utcnow()
    ).all()

    pending_requests = Request.query.filter_by(status='pending').all()

    # Run the allocation algorithm
    allocations = allocate_resources(active_resources, pending_requests)

    # Create allocation records
    for resource_id, request_id in allocations:
        resource = Resource.query.get(resource_id)
        req = Request.query.get(request_id)

        # Create overlap of time windows
        from_time = max(resource.available_from, req.needed_from)
        to_time = min(resource.available_to, req.needed_to)

        allocation = Allocation(
            resource_id=resource_id,
            request_id=request_id,
            allocated_from=from_time,
            allocated_to=to_time
        )

        # Update request status
        req.status = 'allocated'

        db.session.add(allocation)

    db.session.commit()

    flash(f'Allocation complete! {len(allocations)} resources allocated.')
    return redirect(url_for('view_allocations'))

@app.route('/allocations')
@login_required
def view_allocations():
    # Get allocations where current user is either resource owner or requester
    resource_ids = [r.id for r in current_user.resources]

    owned_allocations = Allocation.query.filter(
        Allocation.resource_id.in_(resource_ids)
    ).all() if resource_ids else []

    requested_allocations = Allocation.query.join(Request).filter(
        Request.requester_id == current_user.id
    ).all()

    return render_template(
        'allocations.html',
        owned_allocations=owned_allocations,
        requested_allocations=requested_allocations
    )

if __name__ == '__main__':
    app.run(debug=True)
