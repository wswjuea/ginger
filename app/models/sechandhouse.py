from sqlalchemy import Column, Integer, String, DECIMAL, orm, Date

from app.models.base import Base

class Sechandhouse(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    total_price = Column(DECIMAL(10, 2))
    room_price = Column(DECIMAL(10, 2))
    building_promotion_name = Column(String(255))
    presale_license_number = Column(String(255))
    huxing = Column(String(255))
    on_floor = Column(String(255))
    overall_floorage = Column(DECIMAL(10, 2))
    house_orientation = Column(String(255))
    decoration = Column(String(255))
    tier_house_ratio = Column(String(255))
    elevator = Column(String(255))
    listing_date = Column(Date)
    transaction_ownership = Column(String(255))
    picture = Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['title', 'total_price', 'room_price', 'building_promotion_name',
                       'presale_license_number', 'huxing', 'on_floor', 'overall_floorage', 'house_orientation',
                       'decoration', 'tier_house_ratio', 'elevator', 'listing_date', 'transaction_ownership',
                       'picture']