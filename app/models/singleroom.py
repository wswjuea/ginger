from sqlalchemy import Column, Integer, String, DECIMAL, orm, Date

from app.models.base import Base

class Singleroom(Base):
    id = Column(Integer, primary_key=True)
    presale_license_number = Column(String(255))
    building_name = Column(String(255))
    build_name = Column(String(255))
    room_number = Column(String(255))
    state = Column(String(255))
    overall_floorage = Column(DECIMAL(10, 2))
    sold_date = Column(Date)
    room_price = Column(DECIMAL(10, 2))
    building_promotion_name = Column(String(255))
    total_price =Column(Integer)
    type_design = Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['presale_license_number', 'building_name', 'build_name', 'room_number',
                       'state', 'overall_floorage', 'sold_date', 'room_price', 'building_promotion_name',
                       'total_price', 'type_design']