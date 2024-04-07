import os

import pymongo
from fastapi import FastAPI, Response

app = FastAPI()

my_client = pymongo.MongoClient(os.getenv("MongoClient"))
my_db = my_client["lab1"]
users = my_db.Users
couriers = my_db.Couriers
delivery = my_db.Delivery


@app.get("/find_user")
def find_user(response: Response, id: str):
    user = users.find_one({"id": id})
    if user is None:
        response.status_code = 404
        return {"message": "user not found", "code": response.status_code}
    response.status_code = 200
    return {"name": user['name'], 'address': user['address'], "code": response.status_code}


@app.get("/find_courier")
def find_courier(response: Response, id: str):
    courier = couriers.find_one({"id": id})
    if courier is None:
        response.status_code = 404
        return {"message": "courier not found", "code": response.status_code}
    response.status_code = 200
    return {"name": courier['name'], "code": response.status_code}


@app.post("/user")
def create_user(response: Response, name: str, address: str):
    id_u = int(users.find().sort('_id', -1).limit(1)[0]['id'])
    users.insert_one({"id": str(id_u + 1), "name": name, "address": address})
    response.status_code = 200
    return {"message": "ok", "code": response.status_code}


@app.post("/courier")
def create_courier(response: Response, name: str):
    id_c = int(couriers.find().sort('_id', -1).limit(1)[0]['id'])
    couriers.insert_one({"id": str(id_c + 1), "name": name})
    response.status_code = 200
    return {"message": "ok", "code": response.status_code}


@app.post("/order")
def create_order(response: Response, id_u: str, id_c: str):
    id_o = int(delivery.find().sort('_id', -1).limit(1)[0]['id'])
    user = users.find_one({"id": id_u})
    if user is None:
        response.status_code = 404
        return {"message": "user not found", "code": response.status_code}
    courier = couriers.find_one({"id": id_c})
    if courier is None:
        response.status_code = 404
        return {"message": "courier not found", "code": response.status_code}
    delivery.insert_one({"id": id_o, "user_id": user['_id'], "courier_id": courier['_id']})
    response.status_code = 200
    return {"message": "ok", "code": response.status_code}


@app.delete("/remove_user")
def delete_user(response: Response, id: str):
    users.delete_one({"id": id})
    response.status_code = 200
    return {"message": f"removed user with id = {id}", "code": response.status_code}


@app.delete("/remove_courier")
def delete_courier(response: Response, id: str):
    couriers.delete_one({"id": id})
    response.status_code = 200
    return {"message": f"removed courier with id = {id}", "code": response.status_code}


@app.delete("/remove_order")
def delete_order(response: Response, id: str):
    delivery.delete_one({"id": id})
    response.status_code = 200
    return {"message": f"removed order with id = {id}", "code": response.status_code}


@app.put("/update_user")
def update_user(response: Response, id: str, name: str, address: str):
    user = users.find_one({"id": id})
    if user is None:
        response.status_code = 404
        return {"message": "user not found", "code": response.status_code}
    users.update_one({"id": id}, {"$set": {"name": name, "address": address}})
    response.status_code = 200
    return {"message": "user info updated", "code": response.status_code}


@app.put("/update_courier")
def update_courier(response: Response, id: str, name: str):
    courier = couriers.find_one({"id": id})
    if courier is None:
        response.status_code = 404
        return {"message": "courier not found", "code": response.status_code}
    couriers.update_one({"id": id}, {"$set": {"name": name}})
    response.status_code = 200
    return {"message": "courier info updated", "code": response.status_code}


@app.put("/update_order")
def update_order(response: Response, id: str, id_u: str, id_c: str):
    order = delivery.find_one({"id": id})
    if order is None:
        response.status_code = 404
        return {"message": "delivery not found", "code": response.status_code}
    user = users.find_one({"id": id_u})
    if user is None:
        response.status_code = 404
        return {"message": "user not found", "code": response.status_code}
    courier = couriers.find_one({"id": id_c})
    if courier is None:
        response.status_code = 404
        return {"message": "courier not found", "code": response.status_code}
    delivery.update_one({"id": id}, {"$set": {"user_id": user['_id'], "courier_id": courier['_id']}})
    response.status_code = 200
    return {"message": "Delivery updated", "code": response.status_code}
