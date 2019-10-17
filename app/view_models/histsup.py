class HistsupViewModel:
    @classmethod
    def re_data(cls, data, key):
        if data:
            re_view_type_single = cls.__cut_histsup(data, key)
        return re_view_type_single

    @classmethod
    def __cut_histsup(cls, data, key):
        histsup = {
            "id": data['id'],
            "lat": data['lat'],
            "lng": data['lng'],
            "building_name": data["building_name"],
            "floor_area": data["floor_area"],
            "plot_ratio": data["plot_ratio"],
            "building_address": data["building_address"],
            "region": data["region"],
            "nonsale_houses": data["nonsale_houses"],
            "sold_rate": (data["sold_rate"] * 100),
            "houses_average": data["houses_average"],
            "commercial_average": data["commercial_average"],
            "building_promotion_name": data["building_promotion_name"],
            "presale_license_number": data["presale_license_number"],
            "building_pic": data["building_pic"],
            "opening_date": data["opening_date"],
            key: data[key],
            "count": data[key]
        }
        return histsup

    @classmethod
    def histsearchbyid(cls, data):
        return dict(
            id=data.id,
            building_promotion_name=data.building_promotion_name,
            building_name=data.building_name,
            floor_area=data.floor_area,
            area=data.area,
            plot_ratio=data.plot_ratio,
            building_address=data.building_address,
            opening_date=data.opening_date,
            total_houses=data.total_houses,
            prop_man_comp=data.prop_man_comp,
            sold_houses=data.sold_houses,
            unsold_houses=data.unsold_houses,
            nonsale_houses=data.nonsale_houses,
            unsold_area=data.unsold_houses * data.huxing_area,
            sold_rate=data.sold_rate * 100,
            houses_average=data.houses_average,
            commercial_average=data.commercial_average,
            deal_area=data.sold_houses * data.huxing_area,
            building_pic=data.building_pic,
            presale_license_number=data.presale_license_number
        )

    @classmethod
    def histsearchbylatlng(cls, data):
        return dict(
            id=data.id,
            building_name=data.building_name,
            building_promotion_name=data.building_promotion_name,
            floor_area=data.floor_area,
            area=data.area,
            plot_ratio=data.plot_ratio,
            building_address=data.building_address,
            opening_date=data.opening_date,
            total_houses=data.total_houses,
            prop_man_comp=data.prop_man_comp,
            houses_average=data.houses_average,
            presale_license_number=data.presale_license_number
        )

    @classmethod
    def histsearchbylandid(cls, data):
        return dict(
            id=data.id,
            lat=data.lat,
            lng=data.lng,
            presale_license_number=data.presale_license_number
        )

    @classmethod
    def histsearch(cls, data, attri):
        return data[attri]
