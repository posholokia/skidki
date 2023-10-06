from skidkoman.models import Product, ProductHistory
from skidkoman.models import Category, Brand, Shop


class DataUpdate:
    """
    Класс DataUpdate используется для обновления и добавления продуктов в базу данных, включая проверку существования
    продукта и добавление истории обновлений цен.
    """

    def __init__(self, title, current_price, url, shop, description, old_price, image, brand, category):
        self.title = title
        self.shop = shop
        self.description = description
        self.old_price = old_price
        self.current_price = current_price
        self.url = url
        self.image = image
        self.brand = brand
        self.category = category

    def check_product_table(self):
        """
        Функция проверяет, существует ли продукт в таблице продуктов по заданному URL-адресу.

        :return: логическое значение.

        Он проверяет, есть ли в таблице базы данных какой-либо продукт, имеющий тот же URL-адрес,
        что и предоставленный. Если есть соответствующий продукт, он вернет True.
        В противном случае он вернет False.
        """
        return bool(Product.objects.filter(url=self.url))

    def check_product_history_table(self):
        return bool(ProductHistory.objects.filter(product_id=self.url))

    def add_product_history(self):
        """
        Функция add_product_history проверяет, существует ли таблица истории продукта, и если да,
        то обновляет цену продукта и создает новую запись в таблице истории продукта, если цена изменилась.
        """
        if self.check_product_history_table():
            exist = ProductHistory.objects.filter(product_id=self.url).last()
            if exist.updated_price == self.current_price:
                pass
            else:
                ProductHistory.objects.create(product_id=exist.product_id, updated_price=self.current_price)
                Product.objects.filter(pk=self.url).update(current_price=self.current_price)
        else:
            pass

    def add_product(self):
        """
        Функция добавляет продукт в базу данных и создает запись истории продукта с текущей ценой.
        """
        if self.check_product_table():
            self.add_product_history()
        else:
            obj = Product.objects.create(title=self.title,
                                         shop=self.shop,
                                         description=self.description,
                                         old_price=self.old_price,
                                         current_price=self.current_price,
                                         url=self.url,
                                         image=self.image,
                                         brand=self.brand,
                                         category=self.category)

            ProductHistory.objects.create(product_id=obj, updated_price=self.current_price)

            filter_obj = Filter(category=self.category, brand=self.brand, shop=self.shop)
            filter_obj.filter_all()


class Filter:
    """
    Класс Filter используется для фильтрации и создания объектов в моделях «Категория», «Бренд» и «Магазин» на основе
    указанных категорий, брендов и названий магазинов.
    """

    def __init__(self, category="", brand="", shop=""):
        self.category = category.lower()
        self.brand = brand.lower()
        self.shop = shop.lower()

    def db_category(self):
        return bool(Category.objects.filter(name=self.category))

    def db_brand(self):
        return bool(Brand.objects.filter(name=self.brand))

    def db_shop(self):
        return bool(Shop.objects.filter(name=self.shop))

    def filter_category(self):
        if self.db_category():
            pass
        else:
            Category.objects.create(name=self.category)

    def filter_brand(self):
        if self.db_brand():
            pass
        else:
            Brand.objects.create(name=self.brand)

    def filter_shop(self):
        if self.db_shop():
            pass
        else:
            Shop.objects.create(name=self.shop)

    def filter_all(self):
        self.filter_category()
        self.filter_brand()
        self.filter_shop()