from flask import Blueprint, render_template, redirect, url_for, flash, request
from realestate_app.models import Property
from realestate_app.forms import PropertyForm
from realestate_app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    properties = Property.query.all()
    return render_template('index.html', properties=properties)

@bp.route('/property/<int:id>')
def property(id):
    property = Property.query.get_or_404(id)
    return render_template('property.html', property=property)

@bp.route('/add', methods=['GET', 'POST'])
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            address=form.address.data,
            rooms=form.rooms.data,
            area=form.area.data,
            property_type=form.property_type.data
        )
        db.session.add(property)
        db.session.commit()
        flash('Объект недвижимости успешно добавлен!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_property.html', form=form)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_property(id):
    property = Property.query.get_or_404(id)
    form = PropertyForm(obj=property)
    if form.validate_on_submit():
        property.title = form.title.data
        property.description = form.description.data
        property.price = form.price.data
        property.address = form.address.data
        property.rooms = form.rooms.data
        property.area = form.area.data
        property.property_type = form.property_type.data
        db.session.commit()
        flash('Объект недвижимости успешно обновлен!', 'success')
        return redirect(url_for('main.property', id=property.id))
    return render_template('edit_property.html', form=form, property=property)

@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_property(id):
    property = Property.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(property)
        db.session.commit()
        flash('Объект недвижимости успешно удален!', 'success')
        return redirect(url_for('main.index'))
    return render_template('delete_property.html', property=property)