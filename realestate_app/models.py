from realestate_app import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    rooms = db.Column(db.Integer)
    area = db.Column(db.Float)
    property_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Property {self.title}>'