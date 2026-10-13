


class CarFullInfoDTO:
    pass

class CarBaseInfoDTO:

    def __init__(self, id, brand_name, model_name, year, price, main_photo_tg_id, mileage, shifter_type_name, engine_type_id, engine_volume):
        self.id = id
        self.brand_name = brand_name
        self.model_name = model_name
        self.year = year
        self.price = price
        self.main_photo_tg_id = main_photo_tg_id
        self.mileage = mileage
        self.shifter_type_name = shifter_type_name
        self.engine_type_id = engine_type_id
        self.engine_volume = engine_volume


