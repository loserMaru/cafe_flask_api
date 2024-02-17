from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float
from sqlalchemy.orm import relationship

from app.database import db


# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()

class CafeModel(db.Model):
    __tablename__ = "cafe"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    address = Column(String(255), index=True)
    description = Column(Text, index=True)

    drinks = relationship("DrinksModel", back_populates="cafe")
    orders = relationship("OrderModel", back_populates="cafe")
    products = relationship("ProductsModel", back_populates="cafe")
    favorites = relationship("FavoriteModel", back_populates="cafe")
    ratings = relationship("RatingModel", back_populates="cafe")


class CoffeeModel(db.Model):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    description = Column(Text, index=True)
    location = Column(String(255), index=True)

    weights = relationship("WeightModel", back_populates="coffee")
    orders = relationship("OrderModel", back_populates="coffee")
    products = relationship("ProductsModel", back_populates="coffee")


class DrinksModel(db.Model):
    __tablename__ = "drinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    description = Column(Text, index=True)

    cafe_id = Column(Integer, ForeignKey("cafe.id"))

    cafe = relationship("CafeModel", back_populates="drinks")
    weights = relationship("WeightModel", back_populates="drinks")
    orders = relationship("OrderModel", back_populates="drinks")
    products = relationship("ProductsModel", back_populates="drinks")


class DessertModel(db.Model):
    __tablename__ = "dessert"

    id = Column(Integer, primary_key=True, index=True)
    products = relationship("ProductsModel", back_populates="dessert")


class WeightModel(db.Model):
    __tablename__ = "weight"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(String(45), index=True)
    price = Column(Integer, index=True)

    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    drinks_id = Column(Integer, ForeignKey("drinks.id"))

    coffee = relationship("CoffeeModel", back_populates="weights")
    drinks = relationship("DrinksModel", back_populates="weights")
    orders = relationship("OrderModel", back_populates="weight")


class OrderModel(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(45), index=True)
    total_price = Column(Float, index=True)
    count = Column(Integer, index=True)
    drink_type = Column(String(45), index=True)

    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    drinks_id = Column(Integer, ForeignKey("drinks.id"))
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    weight_id = Column(Integer, ForeignKey("weight.id"))

    cafe = relationship("CafeModel", back_populates="orders")
    drinks = relationship("DrinksModel", back_populates="orders")
    coffee = relationship("CoffeeModel", back_populates="orders")
    weight = relationship("WeightModel", back_populates="orders")


class ProductsModel(db.Model):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    drinks_id = Column(Integer, ForeignKey("drinks.id"))
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    dessert_id = Column(Integer, ForeignKey("dessert.id"))

    cafe = relationship("CafeModel", back_populates="products")
    drinks = relationship("DrinksModel", back_populates="products")
    coffee = relationship("CoffeeModel", back_populates="products")
    dessert = relationship("DessertModel", back_populates="products")


class UserModel(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True)
    password = Column(String(255), index=True)
    role = Column(String(45), index=True)

    favorites = relationship("FavoriteModel", back_populates="user")
    ratings = relationship("RatingModel", back_populates="user")


class FavoriteModel(db.Model):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    cafe = relationship("CafeModel", back_populates="favorites")
    user = relationship("UserModel", back_populates="favorites")


class RatingModel(db.Model):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, index=True)
    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    cafe = relationship("CafeModel", back_populates="ratings")
    user = relationship("UserModel", back_populates="ratings")

# Base.metadata.create_all(bind=engine)
