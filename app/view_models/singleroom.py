class SingleroomViewModel:
    @classmethod
    def singleroomviewmodel(cls, data):
        return dict(
            presale_license_number=data.presale_license_number,
            build_name=data.build_name,
            room_number=data.room_number,
            state=data.state,
            overall_floorage=data.overall_floorage,
            sold_date=data.sold_date,
            room_price=data.room_price,
            total_price=data.total_price
        )

    @classmethod
    def singleroomdw(cls, data):
        return dict(
            presale_license_number=data.presale_license_number,
            building_promotion_name=data.building_promotion_name,
            building_name=data.building_name,
            build_name=data.build_name,
            room_number=data.room_number,
            state=data.state,
            overall_floorage=data.overall_floorage,
            sold_date=data.sold_date,
            room_price=data.room_price,
            total_price=data.total_price
        )