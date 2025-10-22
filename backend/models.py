from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    # 规格信息可以存储为JSON字符串
    specifications = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('cart_items', lazy=True))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, delivered
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # 下单时的价格
    specifications = db.Column(db.Text)
    
    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('order_items', lazy=True))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 评分 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    dish = db.relationship('Dish', backref=db.backref('reviews', lazy=True))

# 初始化默认数据
def init_default_data():
    # 检查是否已有数据
    if Category.query.first() is not None:
        return
    
    # 创建分类
    categories_data = [
        {'id': 1, 'name': '川菜'},
        {'id': 2, 'name': '粤菜'},
        {'id': 3, 'name': '湘菜'},
        {'id': 4, 'name': '鲁菜'},
        {'id': 5, 'name': '苏菜'},
        {'id': 6, 'name': '浙菜'},
        {'id': 7, 'name': '闽菜'},
        {'id': 8, 'name': '徽菜'}
    ]
    
    for cat_data in categories_data:
        category = Category(id=cat_data['id'], name=cat_data['name'])
        db.session.add(category)
    
    # 创建菜品
    dishes_data = [
        # 川菜 (分类ID: 1)
        {'id': 1, 'name': '麻婆豆腐', 'price': 18.8, 'description': '嫩滑豆腐配麻辣肉末，口感丰富，下饭佳品', 'category_id': 1, 'image_url': 'https://cdn.pixabay.com/photo/2017/08/08/17/53/mapo-tofu-2612654_960_720.jpg'},
        {'id': 2, 'name': '宫保鸡丁', 'price': 28.8, 'description': '经典川菜，花生米搭配鸡肉丁，酸甜微辣', 'category_id': 1, 'image_url': 'https://cdn.pixabay.com/photo/2014/11/23/08/48/kung-pao-chicken-542444_960_720.jpg'},
        {'id': 3, 'name': '水煮鱼', 'price': 48.8, 'description': '鲜嫩鱼片配豆芽菜，麻辣鲜香，川菜代表', 'category_id': 1, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/35/fish-3581277_960_720.jpg'},
        {'id': 4, 'name': '回锅肉', 'price': 32.8, 'description': '肥瘦相间的经典川菜，豆瓣酱炒制香气扑鼻', 'category_id': 1, 'image_url': 'https://cdn.pixabay.com/photo/2018/03/18/17/36/stir-fry-3237699_960_720.jpg'},
        {'id': 5, 'name': '夫妻肺片', 'price': 26.8, 'description': '牛肉牛杂凉拌菜，麻辣鲜香，口感丰富', 'category_id': 1, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/36/pork-3581278_960_720.jpg'},
        
        # 粤菜 (分类ID: 2)
        {'id': 6, 'name': '白切鸡', 'price': 35.8, 'description': '皮爽肉滑，原汁原味，配姜葱蘸料', 'category_id': 2, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/37/chicken-3581279_960_720.jpg'},
        {'id': 7, 'name': '叉烧肉', 'price': 38.8, 'description': '蜜汁烤制猪肉，色泽红亮，香甜可口', 'category_id': 2, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/38/pork-3581280_960_720.jpg'},
        {'id': 8, 'name': '虾饺', 'price': 22.8, 'description': '晶莹剔透的虾仁饺子，广式茶点代表', 'category_id': 2, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/39/dim-sum-3581281_960_720.jpg'},
        {'id': 9, 'name': '煲仔饭', 'price': 29.8, 'description': '砂锅烹制米饭配腊味，锅巴香脆', 'category_id': 2, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/40/clay-pot-3581282_960_720.jpg'},
        {'id': 10, 'name': '清蒸鲈鱼', 'price': 45.8, 'description': '新鲜鲈鱼清蒸，肉质鲜嫩，原汁原味', 'category_id': 2, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/41/fish-3581283_960_720.jpg'},
        
        # 湘菜 (分类ID: 3)
        {'id': 11, 'name': '剁椒鱼头', 'price': 52.8, 'description': '大鱼头配剁椒蒸制，鲜辣开胃', 'category_id': 3, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/42/fish-head-3581284_960_720.jpg'},
        {'id': 12, 'name': '辣椒炒肉', 'price': 26.8, 'description': '湖南特色家常菜，辣椒配五花肉', 'category_id': 3, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/43/pork-3581285_960_720.jpg'},
        {'id': 13, 'name': '口味虾', 'price': 38.8, 'description': '小龙虾配香辣酱料，湖南夜宵经典', 'category_id': 3, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/44/crayfish-3581286_960_720.jpg'},
        {'id': 14, 'name': '腊味合蒸', 'price': 36.8, 'description': '湖南腊肉腊鱼合蒸，香气扑鼻', 'category_id': 3, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/45/sausage-3581287_960_720.jpg'},
        {'id': 15, 'name': '糖油粑粑', 'price': 12.8, 'description': '湖南传统小吃，甜糯可口', 'category_id': 3, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/46/dessert-3581288_960_720.jpg'},
        
        # 鲁菜 (分类ID: 4)
        {'id': 16, 'name': '糖醋鲤鱼', 'price': 42.8, 'description': '整鱼炸制后浇糖醋汁，外酥里嫩', 'category_id': 4, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/47/fish-3581289_960_720.jpg'},
        {'id': 17, 'name': '九转大肠', 'price': 36.8, 'description': '猪大肠经多道工序烹制，酸甜苦辣咸五味俱全', 'category_id': 4, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/48/tripe-3581290_960_720.jpg'},
        {'id': 18, 'name': '油爆双脆', 'price': 48.8, 'description': '鸡胗猪肚爆炒，口感爽脆', 'category_id': 4, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/49/offal-3581291_960_720.jpg'},
        
        # 苏菜 (分类ID: 5)
        {'id': 19, 'name': '松鼠桂鱼', 'price': 58.8, 'description': '造型美观，酸甜适口，苏帮菜代表', 'category_id': 5, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/50/fish-3581292_960_720.jpg'},
        {'id': 20, 'name': '盐水鸭', 'price': 32.8, 'description': '南京特产，皮白肉嫩，咸鲜适口', 'category_id': 5, 'image_url': 'https://cdn.pixabay.com/photo/2018/08/04/14/51/duck-3581293_960_720.jpg'}
    ]
    
    for dish_data in dishes_data:
        dish = Dish(
            id=dish_data['id'],
            name=dish_data['name'],
            price=dish_data['price'],
            description=dish_data['description'],
            category_id=dish_data['category_id'],
            image_url=dish_data['image_url']
        )
        db.session.add(dish)
    
    # 创建默认评论
    comments_data = [
        {'dish_id': 1, 'username': '张三', 'content': '味道很棒，花生米很香脆！', 'rating': 5, 'date': datetime(2023, 5, 15)},
        {'dish_id': 1, 'username': '李四', 'content': '辣度刚好，下次还会点', 'rating': 4, 'date': datetime(2023, 5, 10)},
        {'dish_id': 2, 'username': '王五', 'content': '豆腐很嫩，就是稍微有点咸', 'rating': 4, 'date': datetime(2023, 5, 12)},
        {'dish_id': 3, 'username': '赵六', 'content': '肥而不腻，入口即化，太好吃了！', 'rating': 5, 'date': datetime(2023, 5, 14)}
    ]
    
    for comment_data in comments_data:
        comment = Comment(
            dish_id=comment_data['dish_id'],
            username=comment_data['username'],
            content=comment_data['content'],
            rating=comment_data['rating'],
            date=comment_data['date']
        )
        db.session.add(comment)
    
    db.session.commit()