from flask import Flask, redirect, url_for, render_template, request
from find_stocks import stock_list
app = Flask(__name__, static_folder="static")

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        ppt = request.form["nm"]
        if ppt:
            return redirect(url_for("stocks", prompt=ppt))
        else:
            return render_template("index.html")
    else:
        return render_template("index.html")

@app.route("/stocks.html")
def stocks():
    prompt = request.args.get("prompt")
    a=['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL', 'META', 'NVDA', 'NFLX', 'ADBE']
    #a = stock_list(prompt)
    return render_template("stocks.html", x=a)

@app.route("/results.html")
def results():
    return render_template("results.html")

if __name__ == "__main__":
    app.run(port=1234, debug=True)