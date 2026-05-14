from flask import Flask, jsonify, render_template_string, request as freq
import numpy as np
import pandas as pd

app = Flask(__name__)

print("Loading dataset...")
recipes = pd.read_csv("data/RecipeNLG_dataset.csv", usecols=[1, 4])
recipes.columns = ["title", "link"]
recipes["link"] = recipes["link"].fillna("")
titles = recipes["title"].to_numpy()
links = recipes["link"].to_numpy()
TOTAL = len(titles)






HTML = open("templates/index.html").read()

@app.route("/")
def index():
    return render_template_string(HTML, total=TOTAL)

@app.route("/api/window")
def window():
    center = freq.args.get("center", None)
    if center is not None:
        center = int(center)
        start = max(0, center - 150)
        if start + 300 > TOTAL:
            start = max(0, TOTAL - 300)
    else:
        start = np.random.randint(0, max(1, TOTAL - 300))
        center = start + 150

    end = min(start + 300, TOTAL)
    chunk = [
        {
            "title": str(titles[j]),
            "link": str(links[j]) if str(links[j]).startswith("http") else ""
        }
        for j in range(start, end)
    ]
    landing = center - start

    return jsonify({
        "recipes": chunk,
        "start": int(start),
        "total": TOTAL,
        "landing": int(landing)
    })

@app.route("/api/recipe/<int:idx>")
def get_recipe(idx):
    idx = max(0, min(idx, TOTAL - 1))
    link = str(links[idx])
    return jsonify({
        "title": str(titles[idx]),
        "link": link if link.startswith("http") else "",
        "index": idx,
        "total": TOTAL
    })

if __name__ == "__main__":
    app.run(debug=False, port=5000)