from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Flask app configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///household_services.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Database models
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='active')

    def __repr__(self):
        return f"<Customers {self.name}>"

class ServiceProfessional(db.Model):
    __tablename__ = 'service_professional'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    servicetype = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    desc = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')

    def __repr__(self):
        return f"<ServiceProfessional {self.username}>"

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    time_required = db.Column(db.Integer)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date_of_request = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default='requested')  # Default to 'requested'
    remarks = db.Column(db.String(200), nullable=True)
    professional_id = db.Column(db.Integer, nullable=True)
    customer = db.relationship('Customers', backref=db.backref('service_requests', lazy=True))
    service = db.relationship('Service', backref=db.backref('service_requests', lazy=True))

class ServiceHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('service_professional.id'), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    date_of_service = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customers', backref='service_histories')
    service = db.relationship('Service', backref='service_histories')
    professional = db.relationship('ServiceProfessional', backref='service_histories')

    def __repr__(self):
        return f"<ServiceHistory {self.id} - {self.service.name} for {self.customer.name}>"

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if email == "admin@admin.com" and password == "admin123":
            return redirect (url_for('admin_dashboard'))

        customer = Customers.query.filter_by(email=email).first()
        if customer and customer.password == password:
            if customer.status == 'blocked':
                flash('Your account is blocked. Please contact support.', 'danger')
                return redirect(url_for('home'))
            return redirect(url_for('customer_dashboard', customer_id=customer.id))

        professional = ServiceProfessional.query.filter_by(email=email).first()
        if professional and professional.password == password:
            if professional.status != 'approved':
                flash('Your account is not approved yet. Please wait for admin approval.', 'danger')
                return redirect(url_for('home'))
            return redirect(url_for('professional_dashboard', professional_id=professional.id))

        flash('Invalid email or password. Please register or try again.', 'danger')
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        if not name or not email or not password or not address:
            flash('All fields are required!', 'danger')
            return redirect(url_for('customer_register'))

        existing_customer = Customers.query.filter_by(email=email).first()
        if existing_customer:
            flash('Email already exists! Please use a different email.', 'danger')
            return redirect(url_for('customer_register'))

        new_customer = Customers(name=name, email=email, password=password, address=address, status='active')
        
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer registered successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('customer_register.html')

@app.route('/professional_register', methods=['GET', 'POST'])
def professional_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        servicetype = request.form['role']
        desc = request.form['desc']

        if not username or not email or not password or not servicetype or not desc:
            flash('All fields are required!', 'danger')
            return redirect(url_for('professional_register'))

        existing_professional = ServiceProfessional.query.filter_by(email=email).first()
        if existing_professional:
            flash('Email already exists! Please use a different email.', 'danger')
            return redirect(url_for('professional_register'))

        new_professional = ServiceProfessional(username=username, email=email, password=password, servicetype=servicetype, desc=desc, status='pending')

        db.session.add(new_professional)
        db.session.commit()
        flash('Professional registered successfully! Awaiting admin approval.', 'success')
        return redirect(url_for('home'))

    return render_template('professional_register.html')

@app.route('/service/create', methods=['POST'])
def create_service():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        time_required = request.form['time_required']
        description = request.form['description']
        new_service = Service(name=name, price=price, time_required=time_required, description=description)
        db.session.add(new_service)
        db.session.commit()
        flash('New service has been added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

@app.route('/service_request/create', methods=['POST'])
def create_service_request():
    if request.method == 'POST':
        service_id = request.form['service_id']
        customer_id = request.form['customer_id']

        new_request = ServiceRequest(service_id=service_id, customer_id=customer_id)

        db.session.add(new_request)
        db.session.commit()

        # Add to ServiceHistory
        service_history = ServiceHistory(
            customer_id=customer_id,
            service_id=service_id,
            status="requested"
        )
        db.session.add(service_history)
        db.session.commit()

        flash('Service request has been created successfully!', 'success')
        return redirect(url_for('customer_dashboard', customer_id=customer_id))

@app.route('/service_request/assign/<int:request_id>', methods=['GET', 'POST'])
def assign_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)

    if request.method == 'POST':
        professional_id = request.form['professional_id']
        
        if professional_id:
            service_request.professional_id = professional_id
            service_request.status = "assigned"

            existing_history = ServiceHistory.query.filter_by(service_id=service_request.service_id, customer_id=service_request.customer_id).first()

            if existing_history:
                existing_history.professional_id = professional_id
                existing_history.status = "assigned"
                existing_history.date_of_service = datetime.utcnow()  # Update the date if needed
            else:
                service_history = ServiceHistory(
                    customer_id=service_request.customer_id,
                    service_id=service_request.service_id,
                    professional_id=professional_id,
                    status="assigned",
                    date_of_service=datetime.utcnow()
                )
                db.session.add(service_history)

            db.session.commit()  # Commit the changes to the database
            flash('Service request has been assigned successfully!', 'success')
        else:
            flash('No professional assigned. Please select a professional.', 'error')

        return redirect(url_for('admin_dashboard'))

    professionals = ServiceProfessional.query.filter_by(servicetype=service_request.service.name).all()
    
    return render_template('assign_service.html', service_request=service_request, professionals=professionals)
@app.route('/new_service', methods=['GET'])
def new_service():
    """Render the new service form."""
    return render_template ('new_service.html')
@app.route('/service_request/accept/<int:request_id>', methods=['POST'])
def accept_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = "accepted"
    db.session.commit()
    flash('Service request accepted successfully!', 'success')
    return redirect(url_for('professional_dashboard', professional_id=service_request.professional_id))

@app.route('/service_request/reject/<int:request_id>', methods=['POST'])
def reject_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = "rejected"
    db.session.commit()
    flash('Service request rejected successfully!', 'danger')
    return redirect(url_for('professional_dashboard', professional_id=service_request.professional_id))

@app.route('/service_request/complete/<int:request_id>', methods=['POST'])
def complete_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = "completed"
    db.session.commit()
    flash('Service request marked as completed!', 'success')
    return redirect(url_for('professional_dashboard', professional_id=service_request.professional_id))

@app.route('/service_request/close/<int:request_id>', methods=['POST'])
def close_service_request(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    service_request.status = "closed"
    db.session.commit()
    flash('Service request has been closed!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin')
def admin_dashboard():
    services = Service.query.all()
    customers = Customers.query.all()
    professionals = ServiceProfessional.query.all()
    service_requests = ServiceRequest.query.all()

    return render_template(
        'admin_dashboard.html',
        services=services,
        customers=customers,
        professionals=professionals,
        service_requests=service_requests
    )

@app.route('/customer_dashboard/<int:customer_id>')
def customer_dashboard(customer_id):
    customer = Customers.query.get_or_404(customer_id)
    services = Service.query.all()
    requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    history = ServiceHistory.query.filter_by(customer_id=customer_id).all()  # Fetch service history

    return render_template('customer_dashboard.html', customer=customer, services=services, requests=requests, history=history)

@app.route('/professional_dashboard/<int:professional_id>')
def professional_dashboard(professional_id):
    professional = ServiceProfessional.query.get_or_404(professional_id)
    all_requests = ServiceRequest.query.filter_by(professional_id=professional_id).all()

    return render_template('professional_dashboard.html', professional=professional, all_requests=all_requests)

@app.route('/delete_database', methods=['POST'])
def delete_database():
    Customers.query.delete()
    ServiceProfessional.query.delete()
    Service.query.delete()
    ServiceRequest.query.delete()
    ServiceHistory.query.delete()

    db.session.commit()
    flash('All data has been deleted successfully!', 'success')

    return redirect(url_for('admin_dashboard'))

@app.route('/confirm_delete')
def confirm_delete():
    return render_template('confirm_delete.html')

@app.route('/update_customer_status/<int:customer_id>', methods=['POST'])
def update_customer_status(customer_id):
    customer = Customers.query.get_or_404(customer_id)
    new_status = request.form.get('status')

    if new_status:
        customer.status = new_status
        db.session.commit()
        flash(f'Customer status updated to {new_status}.', 'success')
    else:
        flash('No status provided.', 'danger')

    return redirect(url_for('admin_dashboard'))

@app.route('/update_professional_status/<int:professional_id>', methods=['POST'])
def update_professional_status(professional_id):
    professional = ServiceProfessional.query.get_or_404(professional_id)
    new_status = request.form.get('status')

    if new_status:
        professional.status = new_status
        db.session.commit()
        flash(f'Professional status updated to {new_status}.', 'success')
    else:
        flash ('No status provided.', 'danger')

    return redirect(url_for('admin_dashboard'))

@app.route('/edit_service/<int:service_id>', methods=['POST'])
def edit_service(service_id):
    data = request.get_json()
    service = Service.query.get_or_404(service_id)

    service.name = data['name']
    service.price = data['price']
    service.time_required = data['time_required']
    service.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Service updated successfully!'}), 200

@app.route('/delete_service/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully!'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create the new ServiceHistory table as well
    app.run(debug=True)