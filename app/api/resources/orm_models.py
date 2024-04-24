from sqlalchemy import Column, ForeignKey, Integer, String, Text, Float, Date, func, DateTime
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
    image = Column(Text, index=True)
    star = db.Column(db.Float(), nullable=False)

    orders = relationship("OrderModel", back_populates="cafe")
    coffee = relationship("CoffeeModel", back_populates="cafe")
    favorites = relationship("FavoriteModel", back_populates="cafe")
    ratings = relationship("RatingModel", back_populates="cafe")
    users = relationship("UserModel", back_populates='cafe')

    def calculate_average_rating(self):
        average_rating = db.session.query(func.avg(RatingModel.rating)).filter_by(cafe_id=self.id).scalar()
        return average_rating if average_rating is not None else 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'description': self.description,
            'image': self.image,
            'star': self.star
        }


class CoffeeModel(db.Model):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(45), index=True)
    description = Column(Text, index=True)
    image = Column(Text, index=True)

    cafe_id = Column(Integer, ForeignKey("cafe.id"))

    orders = relationship("OrderModel", back_populates="coffee")
    cafe = relationship("CafeModel", back_populates="coffee")


class OrderModel(db.Model):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String(45), index=True, default='waiting')
    name = Column(String(255), index=True)
    pick_up_time = Column(DateTime, index=True)
    time_order_made = Column(DateTime, index=True)

    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    coffee_id = Column(Integer, ForeignKey("coffee.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    cafe = relationship("CafeModel", back_populates="orders")
    coffee = relationship("CoffeeModel", back_populates="orders")
    user = relationship("UserModel", back_populates="orders")


class SubscriptionModel(db.Model):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, index=True)
    end_date = Column(Date, index=True)
    quantity = Column(Integer, index=True)

    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("UserModel", back_populates="subscriptions")


class UserModel(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), index=True, unique=True)
    password = Column(String(255), index=True)
    role = Column(String(45), index=True)
    smartphone_key = Column(String(255), index=True)
    cafe_id = Column(Integer, ForeignKey("cafe.id"))

    cafe = relationship("CafeModel", back_populates="users")

    favorites = relationship("FavoriteModel", back_populates="user")
    ratings = relationship("RatingModel", back_populates="user")
    orders = relationship("OrderModel", back_populates="user")
    subscriptions = relationship("SubscriptionModel", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role": self.role,
            "smartphone_key": self.smartphone_key,
            "cafe_id": self.cafe_id
        }


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
