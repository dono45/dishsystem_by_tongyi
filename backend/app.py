from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask_cors import CORS
from models import db, User, Dish, CartItem, Order, OrderItem, Review, Category
from models import init_default_data  # 导入初始化数据函数
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'food-delivery-secret-key'

db.init_app(app)
jwt = JWTManager(app)
CORS(app)

# 管理员权限装饰器
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # 将字符串ID转换为整数
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid user ID in token'}), 422
            
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 用户权限装饰器（普通用户和管理员都可以）
def user_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        # 将字符串ID转换为整数
        try:
            user_id = int(current_user_id)
        except (ValueError, TypeError):
            return jsonify({'message': 'Invalid user ID in token'}), 422
            
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 403
        return f(*args, **kwargs)
    return decorated_function

# 创建表的函数
def create_tables():
    with app.app_context():
        db.create_all()
        
        # 创建一个默认管理员账户（用户名: admin, 密码: admin123）
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', email='admin@example.com', is_admin=True)
            admin_user.set_password('admin123')
            db.session.add(admin_user)
        
        # 初始化分类数据
        init_default_data()
        
        db.session.commit()

# 在应用启动时创建表
create_tables()

# 用户注册
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400
    
    # 创建新用户
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# 用户登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        # 将用户ID转换为字符串
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# 忘记密码（简化版，实际应该发送邮件）
@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    user = User.query.filter_by(email=email).first()
    
    if user:
        # 在实际应用中，这里应该发送重置链接到用户邮箱
        # 这里我们只是返回成功消息
        return jsonify({'message': 'Password reset instructions sent to your email'}), 200
    
    return jsonify({'message': 'Email not found'}), 404

# 获取菜品列表（无需登录）
@app.route('/api/dishes', methods=['GET'])
def get_dishes():
    dishes = Dish.query.all()
    
    # 为每个菜品计算平均评分
    dish_list = []
    for dish in dishes:
        reviews = Review.query.filter_by(dish_id=dish.id).all()
        if reviews:
            average_rating = sum(review.rating for review in reviews) / len(reviews)
            review_count = len(reviews)
        else:
            average_rating = 5.0  # 默认评分
            review_count = 0
            
        dish_data = {
            'id': dish.id,
            'name': dish.name,
            'description': dish.description,
            'price': dish.price,
            'image_url': dish.image_url,
            'rating': round(average_rating, 1),
            'reviewCount': review_count
        }
        
        # 添加分类信息
        if dish.category:
            dish_data['category'] = {
                'id': dish.category.id,
                'name': dish.category.name
            }
        
        dish_list.append(dish_data)
    
    return jsonify(dish_list), 200

# 获取单个菜品详情（无需登录）
@app.route('/api/dishes/<int:dish_id>', methods=['GET'])
def get_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    
    # 计算平均评分
    reviews = Review.query.filter_by(dish_id=dish_id).all()
    if reviews:
        average_rating = sum(review.rating for review in reviews) / len(reviews)
        review_count = len(reviews)
    else:
        average_rating = 5.0  # 默认评分
        review_count = 0
    
    return jsonify({
        'id': dish.id,
        'name': dish.name,
        'description': dish.description,
        'price': dish.price,
        'image_url': dish.image_url,
        'averageRating': round(average_rating, 1),
        'reviewCount': review_count
    }), 200

# 获取菜品评论（无需登录）
@app.route('/api/dishes/<int:dish_id>/reviews', methods=['GET'])
def get_dish_reviews(dish_id):
    reviews = Review.query.filter_by(dish_id=dish_id).all()
    return jsonify([{
        'id': review.id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at.isoformat() if review.created_at else None,
        'user': {
            'id': review.user.id,
            'username': review.user.username
        }
    } for review in reviews]), 200

# 添加到购物车（需要登录）
@app.route('/api/cart', methods=['POST'])
@user_required
def add_to_cart():
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    try:
        current_user_id = int(current_user_id)
    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid user ID'}), 422
        
    data = request.get_json()
    
    # 检查数据是否存在
    if not data:
        return jsonify({'message': 'Missing JSON data'}), 400
    
    dish_id = data.get('dish_id')
    quantity = data.get('quantity', 1)
    specifications = data.get('specifications', '')
    
    # 验证参数
    if dish_id is None:
        return jsonify({'message': 'Dish ID is required'}), 400
    
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({'message': 'Quantity must be a positive integer'}), 400
    
    # 检查菜品是否存在
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'message': 'Dish not found'}), 404
    
    # 检查是否已经添加过同样的菜品和规格
    cart_item = CartItem.query.filter_by(
        user_id=current_user_id, 
        dish_id=dish_id,
        specifications=specifications
    ).first()
    
    if cart_item:
        # 如果已存在，增加数量
        cart_item.quantity += quantity
    else:
        # 否则创建新的购物车项
        cart_item = CartItem(
            user_id=current_user_id,
            dish_id=dish_id,
            quantity=quantity,
            specifications=specifications
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    return jsonify({'message': 'Item added to cart'}), 201

# 获取用户购物车（需要登录）
@app.route('/api/cart', methods=['GET'])
@user_required
def get_cart():
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([{
        'id': item.id,
        'dish': {
            'id': item.dish.id,
            'name': item.dish.name,
            'price': item.dish.price,
            'image_url': item.dish.image_url
        },
        'quantity': item.quantity,
        'specifications': item.specifications
    } for item in cart_items]), 200

# 更新购物车项数量（需要登录）
@app.route('/api/cart/<int:item_id>', methods=['PUT'])
@user_required
def update_cart_item(item_id):
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    data = request.get_json()
    quantity = data.get('quantity')
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user_id).first_or_404()
    
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    
    db.session.commit()
    
    return jsonify({'message': 'Cart updated'}), 200

# 删除购物车项（需要登录）
@app.route('/api/cart/<int:item_id>', methods=['DELETE'])
@user_required
def delete_cart_item(item_id):
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user_id).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart'}), 200

# 创建订单（需要登录）
@app.route('/api/orders', methods=['POST'])
@user_required
def create_order():
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    data = request.get_json()
    
    # 获取用户的购物车项
    cart_items = CartItem.query.filter_by(user_id=current_user_id).all()
    
    if not cart_items:
        return jsonify({'message': 'Cart is empty'}), 400
    
    # 计算总金额
    total_amount = sum(item.dish.price * item.quantity for item in cart_items)
    
    # 创建订单
    order = Order(user_id=current_user_id, total_amount=total_amount)
    db.session.add(order)
    db.session.flush()  # 获取order.id
    
    # 创建订单项
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            dish_id=item.dish_id,
            quantity=item.quantity,
            price=item.dish.price,
            specifications=item.specifications
        )
        db.session.add(order_item)
    
    # 清空购物车
    for item in cart_items:
        db.session.delete(item)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Order created successfully',
        'order_id': order.id
    }), 201

# 获取用户订单列表（需要登录）
@app.route('/api/orders', methods=['GET'])
@user_required
def get_orders():
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    orders = Order.query.filter_by(user_id=current_user_id).all()
    
    return jsonify([{
        'id': order.id,
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat() if order.created_at else None,
        'items': [{
            'dish': {
                'id': item.dish.id,
                'name': item.dish.name,
                'price': item.dish.price
            },
            'quantity': item.quantity,
            'price': item.price,
            'specifications': item.specifications
        } for item in order.order_items]
    } for order in orders]), 200

# 添加评论（需要登录）
@app.route('/api/dishes/<int:dish_id>/reviews', methods=['POST'])
@user_required
def add_review(dish_id):
    current_user_id = get_jwt_identity()
    # 将字符串ID转换为整数
    current_user_id = int(current_user_id)
    data = request.get_json()
    
    # 检查参数
    if not data:
        return jsonify({'message': 'Missing JSON data'}), 400
    
    rating = data.get('rating')
    comment = data.get('comment', '')  # 评论可以为空
    
    # 验证评分
    if rating is None:
        return jsonify({'message': 'Rating is required'}), 400
    
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'message': 'Rating must be an integer between 1 and 5'}), 400
    
    # 检查菜品是否存在
    dish = Dish.query.get(dish_id)
    if not dish:
        return jsonify({'message': 'Dish not found'}), 404
    
    # 创建评论
    review = Review(
        user_id=current_user_id,
        dish_id=dish_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'message': 'Review added successfully'}), 201

# 管理员：获取所有菜品
@app.route('/api/admin/dishes', methods=['GET'])
@admin_required
def admin_get_dishes():
    dishes = Dish.query.all()
    return jsonify([{
        'id': dish.id,
        'name': dish.name,
        'description': dish.description,
        'price': dish.price,
        'image_url': dish.image_url
    } for dish in dishes]), 200

# 管理员：创建菜品
@app.route('/api/admin/dishes', methods=['POST'])
@admin_required
def admin_create_dish():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')
    category_id = data.get('category_id')
    
    dish = Dish(
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        category_id=category_id
    )
    
    db.session.add(dish)
    db.session.commit()
    
    # 获取分类信息
    category_info = None
    if dish.category:
        category_info = {
            'id': dish.category.id,
            'name': dish.category.name
        }
    
    return jsonify({
        'message': 'Dish created successfully',
        'dish': {
            'id': dish.id,
            'name': dish.name,
            'description': dish.description,
            'price': dish.price,
            'image_url': dish.image_url,
            'category': category_info
        }
    }), 201

# 管理员：更新菜品
@app.route('/api/admin/dishes/<int:dish_id>', methods=['PUT'])
@admin_required
def admin_update_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    data = request.get_json()
    
    dish.name = data.get('name', dish.name)
    dish.description = data.get('description', dish.description)
    dish.price = data.get('price', dish.price)
    dish.image_url = data.get('image_url', dish.image_url)
    dish.category_id = data.get('category_id', dish.category_id)
    
    db.session.commit()
    
    # 获取分类信息
    category_info = None
    if dish.category:
        category_info = {
            'id': dish.category.id,
            'name': dish.category.name
        }
    
    return jsonify({
        'message': 'Dish updated successfully',
        'dish': {
            'id': dish.id,
            'name': dish.name,
            'description': dish.description,
            'price': dish.price,
            'image_url': dish.image_url,
            'category': category_info
        }
    }), 200

# 管理员：删除菜品
@app.route('/api/admin/dishes/<int:dish_id>', methods=['DELETE'])
@admin_required
def admin_delete_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    
    # 删除相关的购物车项、订单项和评论
    CartItem.query.filter_by(dish_id=dish_id).delete()
    OrderItem.query.filter_by(dish_id=dish_id).delete()
    Review.query.filter_by(dish_id=dish_id).delete()
    
    db.session.delete(dish)
    db.session.commit()
    
    return jsonify({'message': 'Dish deleted successfully'}), 200

# 管理员：获取所有订单
@app.route('/api/admin/orders', methods=['GET'])
@admin_required
def admin_get_orders():
    orders = Order.query.all()
    
    return jsonify([{
        'id': order.id,
        'user': {
            'id': order.user.id,
            'username': order.user.username
        },
        'total_amount': order.total_amount,
        'status': order.status,
        'created_at': order.created_at.isoformat() if order.created_at else None,
        'items': [{
            'dish': {
                'id': item.dish.id,
                'name': item.dish.name,
                'price': item.dish.price
            },
            'quantity': item.quantity,
            'price': item.price,
            'specifications': item.specifications
        } for item in order.order_items]
    } for order in orders]), 200

# 管理员：更新订单状态
@app.route('/api/admin/orders/<int:order_id>/status', methods=['PUT'])
@admin_required
def admin_update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    status = data.get('status')
    
    if status in ['pending', 'confirmed', 'delivered']:
        order.status = status
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'}), 200
    else:
        return jsonify({'message': 'Invalid status'}), 400

# 管理员：获取所有菜品分类
@app.route('/api/admin/categories', methods=['GET'])
@admin_required
def admin_get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories]), 200

# 管理员：创建菜品分类
@app.route('/api/admin/categories', methods=['POST'])
@admin_required
def admin_create_category():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')
    
    # 检查分类是否已存在
    if Category.query.filter_by(name=name).first():
        return jsonify({'message': '分类名称已存在'}), 400
    
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'message': '分类创建成功',
        'category': {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }
    }), 201

# 管理员：更新菜品分类
@app.route('/api/admin/categories/<int:category_id>', methods=['PUT'])
@admin_required
def admin_update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    # 检查分类名称是否已存在（排除自己）
    name = data.get('name')
    if name and name != category.name:
        if Category.query.filter_by(name=name).first():
            return jsonify({'message': '分类名称已存在'}), 400
    
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    
    db.session.commit()
    
    return jsonify({
        'message': '分类更新成功',
        'category': {
            'id': category.id,
            'name': category.name,
            'description': category.description
        }
    }), 200

# 管理员：删除菜品分类
@app.route('/api/admin/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def admin_delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    
    # 检查是否有菜品关联到该分类
    dish_count = Dish.query.filter_by(category_id=category_id).count()
    if dish_count > 0:
        return jsonify({'message': f'无法删除分类，还有{dish_count}个菜品关联到该分类'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': '分类删除成功'}), 200

if __name__ == '__main__':
    app.run(debug=True)