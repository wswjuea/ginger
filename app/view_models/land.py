
class LandViewModel:
    @classmethod
    def landviewmodel(cls, data, key):
        return dict(
            id=data.id,
            lat=data.lat,
            lng=data.lng,
            plotnum=data.plotnum,
            block_name=data.block_name,
            block_location=data.block_location,
            land_usage=data.land_usage,
            listing_start_date=data.listing_start_date,
            price=data.price,
            competitive_unit=data.competitive_unit,
            deal_date=data.deal_date,
            deal_price=data.deal_price,
            region=data.region,
            total_land_area=data.total_land_area,
            block_status=data.block_status,
            listing_floor_price=data.listing_floor_price,
            transfer_floor_price=data.transfer_floor_price,
            count=data[key],
            premium_rate=data.premium_rate
        )

    @classmethod
    def landsearchbyid(cls, data):
        return dict(
            id=data.id,
            block_name=data.block_name,
            block_status=data.block_status,
            region=data.region,
            plotnum=data.plotnum,
            block_location=data.block_location,
            land_usage=data.land_usage,
            listing_start_date=data.listing_start_date,
            listing_deadline=data.listing_deadline,
            terminal_date=data.terminal_date,
            deal_date=data.deal_date,
            competitive_unit=data.competitive_unit,
            area_covered=str(data.total_land_area) + "平方米 (" + str(round(data.total_land_area/2000*3, 1)) + "亩)",
            plot_ratio_detail=data.plot_ratio_detail,
            house_area=data.house_area,
            commercial_area=data.commercial_area,
            overall_floorage=data.overall_floorage,
            price=data.price,
            deal_price=data.deal_price,
            building_density=data.building_density,
            greening_rate=data.greening_rate,
            listing_floor_price=data.listing_floor_price,
            transfer_floor_price=data.transfer_floor_price,
            land_pic=data.land_pic,
            premium_rate=data.premium_rate
        )
    @classmethod
    def landsearchbylatlng(cls, data):
        return dict(
            id=data.id,
            plotnum=data.plotnum,
            listing_start_date=data.listing_start_date,
            block_name=data.block_name,
            block_location=data.block_location,
            terminal_date=data.terminal_date,
            margin_deadline=data.margin_deadline,
            price=data.price,
            bond=data.bond,
            block_status=data.block_status,
            deal_date=data.deal_date,
            deal_price=data.deal_price,
            transfer_floor_price=data.transfer_floor_price,
            competitive_unit=data.competitive_unit,
            premium_rate=data.premium_rate
        )

    @classmethod
    def landsearch(cls, data, attri):
        return data[attri]
