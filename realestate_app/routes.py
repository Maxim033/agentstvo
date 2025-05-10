from flask import (Blueprint, render_template, redirect,
                   url_for, flash, request, current_app)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from realestate_app import db
from realestate_app.models import Property, User
from realestate_app.forms import PropertyForm, LoginForm

bp = Blueprint('main', __name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 6

    filters = {
        'min_price': request.args.get('min_price', type=int),
        'max_price': request.args.get('max_price', type=int),
        'property_type': request.args.get('property_type'),
        'min_rooms': request.args.get('min_rooms', type=int),
        'search': request.args.get('search', '')
    }

    query = Property.query

    if filters['min_price']:
        query = query.filter(Property.price >= filters['min_price'])
    if filters['max_price']:
        query = query.filter(Property.price <= filters['max_price'])
    if filters['property_type']:
        query = query.filter(Property.property_type == filters['property_type'])
    if filters['min_rooms']:
        query = query.filter(Property.rooms >= filters['min_rooms'])
    if filters['search']:
        query = query.filter(
            Property.title.ilike(f"%{filters['search']}%") |
            Property.address.ilike(f"%{filters['search']}%")
        )

    properties = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('index.html', properties=properties, filters=filters)

@bp.route('/property/<int:id>')
def property(id):
    prop = Property.query.get_or_404(id)
    return render_template('property.html', property=prop)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename
                ))

        new_property = Property(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            address=form.address.data,
            rooms=form.rooms.data,
            area=form.area.data,
            property_type=form.property_type.data,
            image=filename,
            user_id=current_user.id
        )

        db.session.add(new_property)
        db.session.commit()
        flash('Объект успешно добавлен!', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_property.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_property(id):
    prop = Property.query.get_or_404(id)
    if prop.user_id != current_user.id:
        flash('У вас нет прав для редактирования этого объекта', 'danger')
        return redirect(url_for('main.index'))

    form = PropertyForm(obj=prop)

    if form.validate_on_submit():
        # Обработка изображения
        if form.image.data:
            # Удаляем старое изображение
            if prop.image:
                old_image = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    prop.image
                )
                if os.path.exists(old_image):
                    os.remove(old_image)

            # Сохраняем новое изображение
            file = form.image.data
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    filename
                ))
                prop.image = filename

        # Обновляем остальные поля
        form.populate_obj(prop)
        db.session.commit()
        flash('Объект успешно обновлен!', 'success')
        return redirect(url_for('main.property', id=prop.id))

    return render_template('edit_property.html', form=form, property=prop)


@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_property(id):
    prop = Property.query.get_or_404(id)
    if prop.user_id != current_user.id:
        flash('У вас нет прав для удаления этого объекта', 'danger')
        return redirect(url_for('main.index'))

    # Удаляем изображение
    if prop.image:
        image_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            prop.image
        )
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(prop)
    db.session.commit()
    flash('Объект успешно удален!', 'success')
    return redirect(url_for('main.index'))


# Маршруты для аутентификации
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('main.index'))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))