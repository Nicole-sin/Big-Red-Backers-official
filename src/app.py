import json
from flask import Flask, request, render_template, send_from_directory
import db
from db import DatabaseDriver

DB = DatabaseDriver()

app = Flask(__name__)
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/setup", methods=["POST"])
def setup_data():
    import setup_test_data
    setup_test_data.run()
    return "Database initialized", 200


@app.route("/write_review.html")
def write_review():
    return render_template("write_review.html")

@app.route("/profile.html")
def profile():
    return render_template("profile.html")

@app.route("/favorites.html")
def favorites():
    return render_template("favorites.html")

@app.route("/dish")
def dish():
    return render_template("dish.html")


@app.route("/api/reviews/", methods=["GET"])
def get_all_reviews():
    reviews = DB.get_all_reviews()
    return json.dumps({"reviews": reviews}), 200

@app.route("/api/reviews/", methods=["POST"])
def post_review():
    body = json.loads(request.data)
    user_id = body.get("user_id")
    food_id = body.get("food_id")
    dining_hall_id = body.get("dining_hall_id")
    rating = body.get("rating")
    message = body.get("message", "")
    recommended_foods = body.get("recommended_foods", [])
    
    if not user_id or not food_id or not dining_hall_id or rating is None:
        return json.dumps({"error": "Missing required field(s)"}), 400
    
    review_id = DB.create_review(
        user_id=user_id,
        food_id=food_id,
        dining_hall_id=dining_hall_id,
        rating=rating,
        message=message
    )

    if recommended_foods and isinstance(recommended_foods, list):
        for food_id in recommended_foods:
            DB.add_recommended_food(review_id, food_id)
    
    return json.dumps({
        "id": review_id,
        "message": "Review created successfully"
    }), 201

@app.route("/api/reviews/<int:review_id>/", methods=["DELETE"])
def delete_review(review_id):
    review = DB.get_review(review_id)
    
    if not review:
        return json.dumps({"error": "Review not found"}), 404
    DB.delete_review(review_id)
    
    return json.dumps({"message": f"Review {review_id} deleted successfully"}), 200
@app.route("/api/dining-halls/", methods=["GET"])
def get_all_dining_halls():
    dining_halls = DB.get_all_dining_halls()
    return json.dumps({"dining_halls": dining_halls}), 200

@app.route("/api/users/<int:user_id>/reviews/", methods=["GET"])
def get_reviews_by_user(user_id):
    user = DB.get_user(user_id)
    if not user:
        return json.dumps({"error": "User not found"}), 404
    
    reviews = DB.get_reviews_by_user(user_id)
    return json.dumps({"reviews": reviews}), 200
@app.route("/api/users/", methods=["POST"])
def create_user():
    new_user_id = DB.create_user()
    
    return json.dumps({
        "id": new_user_id,
        "message": "User created successfully"
    }), 201

@app.route("/api/dining-halls/<int:hall_id>/food-items/", methods=["GET"])
def get_food_items_by_dining_hall(hall_id):
    hall = DB.get_dining_hall(hall_id)
    if not hall:
        return json.dumps({"error": "Dining hall not found"}), 404
    
    food_items = DB.get_food_items_by_dining_hall(hall_id)
    result = []
    
    for item in food_items:
        result.append({
            "id": item['id'],
            "name": item['name'],
            "image": item['image']
        })
    return json.dumps({"food_items": result}), 200

if __name__ == "__main__":
    # from src import setup_test_data
    # setup_test_data.run()
    app.run(host="0.0.0.0", port=5000, debug=True)