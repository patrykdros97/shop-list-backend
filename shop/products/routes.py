from flask import redirect, render_template, url_for, flash, request
from shop import db, app
from .models import Shopping
from .forms import Addproducts
from .models import Post


@app.route('/')
def admin():
    shop_lists = Shopping.query.all()
    return render_template('admin/show_lists.html', lists=shop_lists)


@app.route('/<shop>', methods=['POST', 'GET'])
def view_list(shop):
    shop_list = Shopping.query.filter_by(name=shop).first()
    products = Post.query.filter_by(shopping_id=shop_list.id)
    
    return render_template('admin/index.html', products=products, shop_list=shop_list)


@app.route('/checkbox/<shop>', methods=['GET', 'POST'])
def checkbox(shop):
    if request.method == 'POST':
        for product_id in request.form.getlist('marked'):
            product = Post.query.get_or_404(int(product_id))
            product.marked = True
            db.session.commit()
    return redirect(url_for('view_list', shop=shop))


@app.route('/add-shop-list', methods=['GET', 'POST'])
def add_shop_list():
    if request.method == 'POST':
        get_list = request.form.get('list')
        list = Shopping(name=get_list)
        db.session.add(list)
        flash(f'The Shop list {get_list} was added to database', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('products/add_list.html', list='list')


@app.route('/add-product', methods=['POST', 'GET'])
def add_product():
    shop_lists = Shopping.query.all()
    form = Addproducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        shop_list = request.form.get('list')
        addpro = Post(name=name, marked=False, shopping_id=shop_list)
        db.session.add(addpro)
        flash(f'The product {name} was added to list {shop_list}')
        db.session.commit()
        shop = Shopping.query.get(shop_list)
        return redirect(url_for('view_list', shop=shop.name))
    return render_template('products/addproduct.html', title='Add product', form=form, lists=shop_lists)


@app.route('/update-shop-list/<int:id>', methods=['GET', 'POST'])
def update_shop_list(id):
    update_list = Shopping.query.get_or_404(id)
    shop = request.form.get('shop')
    if request.method == 'POST':
        update_list.name = shop
        flash(f'Your shop list has beem updated', 'success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/update_shop.html', title='Update shop name', update_list=update_list)


@app.route('/update-product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Post.query.get_or_404(id)
    shop = Shopping.query.get(product.shopping_id)
    form = Addproducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        db.session.commit()
        flash(f'Your product has been updated', 'success')
        return redirect(url_for('view_list', shop=shop.name))
    product.name = form.name.data
    return render_template('products/update_product.html', form=form, list=shop, product=product)

 
@app.route('/delete-list/<int:id>', methods=['POST'])
def delete_list(id):
    shop_list = Shopping.query.get_or_404(id)
    Post.query.filter(Post.shopping_id == id).delete()
    if request.method == 'POST':
        db.session.delete(shop_list)
        db.session.commit()
        flash(f'The shop list {shop_list.name} was deleted from database', 'succes')
        return redirect(url_for('admin'))
    flash(f'The shop list {shop_list.name} cannot be deleted from database', 'succes')
    return redirect(url_for('admin'))


@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Post.query.get(id)
    if request.method == 'POST':
        Post.query.filter(Post.id == id).delete()
        db.session.commit()
        flash(f'The product {product.name} was deleted from database', 'succes')
        return redirect(url_for('admin'))
    flash(f'The shop list {product.name} cannot be deleted from database', 'succes')
    return redirect(url_for('admin'))


@app.route('/delete-multiple-lists', methods=['GET', 'POST'])
def delete_multiple():
    if request.method == 'POST':
        check_all = request.form.getlist('checkall')
        if check_all:
            checked_items = list(map(lambda x: x.id, Shopping.query.all()))
        else:
            checked_items = request.form.getlist('mycheckbox')
        names = []
        for element in checked_items:
            names.append(Shopping.query.get(int(element)).name)
            Shopping.query.filter(Shopping.id == int(element)).delete()
            db.session.commit()
        flash(f'The shop lists {" ".join(list(map(lambda x: x, names)))} were deleted from database', 'success')
        return redirect(url_for('admin'))
