import json
from flask import Flask, render_template

app = Flask(__name__)

def extract_menu(data):
    days = []
    for date, day_data in data["menu"].items():
        meals = []
        for meal_name, meal in day_data["meals"].items():
            items = []
            for item in meal["items"]:
                name = item["name"] if isinstance(item, dict) else item
                tags = item.get("tags", []) if isinstance(item, dict) else []
                items.append({"name": name, "tags": tags})
            meals.append({
                "meal_name": meal_name,
                "display_name": meal["name"],
                "start_time": meal["startTime"],
                "end_time": meal["endTime"],
                "items": items,
            })
        days.append({"date": date, "day_name": day_data["day"], "meals": meals})

    days.sort(key=lambda d: d["date"])
    return days


@app.route("/")
def home():
    with open("menu.json") as f:
        data = json.load(f)

    days = extract_menu(data)
    return render_template("index.html", days=days)


if __name__ == "__main__":
    app.run(debug=True)