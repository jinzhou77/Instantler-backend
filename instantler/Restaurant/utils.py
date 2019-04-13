import uuid

def uuidToStr():
    return str(uuid.uuid4())

initPreferenceWeight = 20
ratePreferenceTable = {
    1:-2,
    2:-1,
    3:0,
    4:1,
    5:2
}
restaurantType = {"american", "seafood", "steak", "fast", "bar", "finedining", "chinese",  "japanese", "korean", "mexican", "pizza", "breakfast", "noodle", "italian", "mediterranean","french","vegetarian"}
