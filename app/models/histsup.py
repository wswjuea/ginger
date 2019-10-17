from sqlalchemy import Column, Integer, String, DECIMAL, orm, Date

from app.models.base import Base

class Histsup(Base):
    id = Column(Integer, primary_key=True)
    presale_license_number = Column(String(255))
    region = Column(String(255))
    area = Column(DECIMAL(10, 2))
    building_name = Column(String(255))
    building_address = Column(String(255))
    opening_date = Column(Date)
    total_houses = Column(Integer)
    unsold_houses = Column(Integer)
    nonsale_houses = Column(Integer)
    sold_houses = Column(Integer)
    sold_rate = Column(DECIMAL(10, 4))
    lat = Column(DECIMAL(9, 6))
    lng = Column(DECIMAL(9, 6))
    huxing_area = Column(DECIMAL(10, 2))
    houses_average = Column(DECIMAL(10, 2))
    commercial_average = Column(DECIMAL(10, 2))
    building_promotion_name = Column(String(255))
    completion_date = Column(Date)
    prop_man_comp = Column(String(255))
    floor_area = Column(DECIMAL(15, 3))
    total_building_volume = Column(String(1000))
    plot_ratio = Column(String(255))
    greening_rate = Column(String(255))
    presale_type = Column(String(255))
    type_design = Column(String(255))
    building_pic = Column(String(255))
    plotnum = Column(String(255))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['presale_license_number', 'region', 'area', 'building_name', 'building_address', 'opening_date',
                       'total_houses', 'unsold_houses', 'nonsale_houses', 'sold_houses', 'sold_rate', 'lat', 'lng',
                       'huxing_area', 'houses_average', 'commercial_average', 'building_promotion_name',
                       'completion_date', 'prop_man_comp', 'floor_area', 'total_building_volume', 'plot_ratio',
                       'greening_rate', 'presale_type', 'type_design', 'building_pic', 'id', 'plotnum']
