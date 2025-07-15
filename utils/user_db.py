import os
from pymongo import MongoClient
from datetime import datetime

mongo = MongoClient(os.getenv('MONGODB_URI'))
db = mongo['FaceSwapBot']
users = db['users']

def add_or_update_user(user):
    found = users.find_one({"user_id": user.id})
    if not found:
        users.insert_one({
            "user_id": user.id,
            "username": user.username,
            "premium": False,
            "requests": [],
            "joined": datetime.utcnow()
        })
    else:
        users.update_one(
            {"user_id": user.id},
            {"$set": {"username": user.username}}
        )

def check_limit(user_id, daily_limit=3):
    user = users.find_one({"user_id": user_id})
    today = datetime.utcnow().date()
    used = sum(1 for x in user.get('requests', []) if x['date'].date() == today)
    return used < daily_limit

def record_usage(user_id):
    users.update_one(
        {"user_id": user_id},
        {"$push": {"requests": {"date": datetime.utcnow()}}}
    )

def is_premium(user_id):
    user = users.find_one({"user_id": user_id})
    return user and user.get('premium', False)

def user_stats():
    return users.count_documents({})

def db_size():
    stats = db.command("dbstats")
    return stats.get('storageSize', 0) // 1024

def broadcast_all(context, msg):
    all_users = users.find({})
    sent = 0
    for u in all_users:
        try:
            context.bot.send_message(u['user_id'], msg)
            sent += 1
        except:
            continue
    return sent
