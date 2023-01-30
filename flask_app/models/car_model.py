from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Car:
    DB = "car_dealz"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.sold_to = data['sold_to']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller = None
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        cars = []
        for c in results:
            car = cls(c)
            car.seller = c['first_name']
            cars.append(car)
        return cars
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO cars ( user_id , price , model , make , year , description , created_at, updated_at ) VALUES ( %(user_id)s , %(price)s , %(model)s , %(make)s , %(year)s , %(description)s , NOW() , NOW() );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    @classmethod
    def get_one(cls, car_id):
        query = "SELECT * FROM cars WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, {'id':car_id})
        car = cls(results[0])
        return car
    
    @classmethod
    def get_by_user(cls,user_id):
        query = "SELECT * FROM cars WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.DB).query_db(query,{'user_id':user_id})
        return results
    
    @classmethod
    def update(cls, request_form_data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s, updated_at = NOW()  WHERE id = %(car_id)s"
        results = connectToMySQL(cls.DB).query_db(query, request_form_data)
        return results
    
    @classmethod
    def delete(cls, car_id):
        query ="DELETE from cars WHERE id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, {'id':car_id})
        return results
    
    
    @staticmethod
    def validate_car( car ):
        is_valid = True
        
        if len(car['price']) < 1:
            is_valid = False
            flash(u'Price required.','car')
        else:
            if int(car['price']) < 1:
                is_valid = False
                flash(u'Car price must be greater than $0.','car')
        
        if len(car['model']) < 1:
            is_valid = False
            flash(u'Model required.','car')
        
        if len(car['make']) < 1:
            is_valid = False
            flash(u'Make required.','car')
            
            
        if len(car['year']) < 1:
            is_valid = False
            flash(u'Year required.','car')
        else:
            if int(car['year']) < 1:
                is_valid = False
                flash(u'Car year must be greater than 0.','car')
        
        if len(car['description']) < 1:
            is_valid = False
            flash(u'Description required.','car')
            
        return is_valid
    
    @classmethod
    def buy(cls, data):
        query = "UPDATE cars SET sold_to = %(user_id)s, updated_at = NOW()  WHERE id = %(car_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def get_by_buyer(cls,user_id):
        query = "SELECT * FROM cars WHERE cars.sold_to = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,{'user_id':user_id})
        return results