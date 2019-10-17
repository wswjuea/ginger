from sqlalchemy import Column, Integer, String, DECIMAL, orm, Date, Text

from app.models.base import Base

class Land(Base):
    id = Column(Integer, primary_key=True)
    lat = Column(DECIMAL(9, 6))
    lng = Column(DECIMAL(9, 6))
    plotnum = Column(String(255))
    title = Column(String(255))
    order_title = Column(Integer)
    block_name = Column(String(255))
    block_location = Column(String(255))
    land_usage = Column(String(255))
    auction_start_date = Column(Date)
    listing_start_date = Column(Date)
    listing_deadline = Column(Date)
    margin_deadline = Column(Date)
    price = Column(DECIMAL(11, 2))
    bond = Column(DECIMAL(11, 2))
    competitive_unit = Column(String(255))
    end_date = Column(Date)
    terminal_date = Column(Date)
    deal_date = Column(Date)
    deal_price = Column(DECIMAL(11, 2))
    plot_ratio_detail = Column(String(255))
    granting_area = Column(DECIMAL(11, 2))
    region = Column(String(255))
    age_limit = Column(String(255))
    floor_pirce = Column(String(255))
    range_bidding_increase = Column(DECIMAL(11, 2))
    price_ceiling = Column(DECIMAL(11, 2))
    comple_house_area = Column(DECIMAL(11, 2))
    match_house_area = Column(DECIMAL(11, 2))
    highest_quotation = Column(DECIMAL(11, 2))
    highest_quotation_unit = Column(String(255))
    register_auction_start_date = Column(Date)
    register_auction_deadline = Column(Date)
    bidder_conditions = Column(Text)
    contacts = Column(String(255))
    contacts_phone = Column(String(255))
    state = Column(String(255))
    plot_ratio = Column(DECIMAL(11, 2))
    total_land_area = Column(DECIMAL(11, 2))
    allocated_area = Column(DECIMAL(11, 2))
    house_area = Column(DECIMAL(11, 2))
    commercial_area = Column(DECIMAL(11, 2))
    office_area = Column(DECIMAL(11, 2))
    other_area = Column(DECIMAL(11, 2))
    building_density = Column(DECIMAL(11, 2))
    building_height = Column(DECIMAL(11, 2))
    greening_rate = Column(DECIMAL(11, 2))
    remarks = Column(String(255))
    overall_floorage = Column(DECIMAL(11, 2))
    comprehensive_floor_price = Column(DECIMAL(11, 2))
    block_status = Column(String(255))
    listing_floor_price = Column(DECIMAL(11, 2))
    transfer_floor_price = Column(DECIMAL(11, 2))
    land_pic = Column(String(255))
    premium_rate = Column(DECIMAL(7, 4))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['plotnum', 'title', 'block_name', 'block_location', 'land_usage', 'auction_start_date',
                       'listing_start_date', 'listing_deadline', 'margin_deadline', 'price', 'bond',
                       'competitive_unit', 'end_date', 'terminal_date', 'deal_date', 'deal_price',
                       'plot_ratio_detail', 'granting_area', 'region', 'age_limit', 'floor_pirce',
                       'range_bidding_increase', 'price_ceiling', 'comple_house_area', 'match_house_area',
                       'highest_quotation', 'highest_quotation_unit', 'register_auction_start_date',
                       'register_auction_deadline', 'bidder_conditions', 'contacts', 'contacts_phone',
                       'state', 'plot_ratio', 'total_land_area', 'allocated_area', 'house_area', 'commercial_area',
                       'office_area', 'other_area', 'building_density', 'building_height', 'greening_rate',
                       'remarks', 'overall_floorage', 'comprehensive_floor_price', 'block_status',
                       'listing_floor_price', 'transfer_floor_price', 'lat', 'lng', 'order_title', 'land_pic',
                       'premium_rate']

