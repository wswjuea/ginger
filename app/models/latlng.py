from sqlalchemy import Column, Integer, String, DECIMAL, orm

from app.models.base import Base


# latlng模型
class Latlng(Base):
    id = Column(Integer, primary_key=True)
    project_name = Column(String(50))
    city = Column(String(50))
    address = Column(String(50))
    lat = Column(DECIMAL(9, 6))
    lng = Column(DECIMAL(9, 6))
    housing_price = Column(DECIMAL(10, 2))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['project_name', 'city', 'address', 'lat', 'lng', 'housing_price']


    # def keys(self):
    #     return ['project_name', 'city', 'address', 'lat', 'lng', 'housing_price']
    #
    # def to_json(self):
    #     dict = self.__dict__
    #     if "_sa_instance_state" in dict:
    #         del dict["_sa_instance_state"]
    #     keys = {'project_name', 'city', 'address', 'lat', 'lng', 'housing_price'}
    #     return {key: value for key, value in dict.items() if key in keys}