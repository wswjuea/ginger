class SechandhouseViewModel:
    @classmethod
    def secviewmodel(cls, data):
        return dict(
            title=data.title,
            total_price=str(data.total_price) + '万元',
            room_price=str(data.room_price) + '元',
            building_promotion_name=data.building_promotion_name,
            presale_license_number=data.presale_license_number,
            huxing=data.huxing,
            on_floor=data.on_floor,
            overall_floorage=data.overall_floorage,
            house_orientation=data.house_orientation,
            decoration=data.decoration,
            tier_house_ratio=data.tier_house_ratio,
            elevator=data.elevator,
            listing_date=data.listing_date,
            transaction_ownership=data.transaction_ownership,
            picture=data.picture
        )
    @classmethod
    def secdw(cls, data):
        return dict(
            title=data.title,
            building_promotion_name=data.building_promotion_name,
            huxing=data.huxing,
            on_floor=data.on_floor,
            overall_floorage=data.overall_floorage,
            house_orientation=data.house_orientation,
            decoration=data.decoration,
            tier_house_ratio=data.tier_house_ratio,
            elevator=data.elevator,
            listing_date=data.listing_date,
            transaction_ownership=data.transaction_ownership,
            room_price=data.room_price,
            total_price=data.total_price
        )