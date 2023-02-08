from requests import get
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup as bs


def getVideoMetaDataFromURL(url: str):
    try:
        res = get(url).text
        soup = bs(res, 'html.parser')

        duration_meta = soup.find("meta", {"itemprop": "duration"})
        duration_string = duration_meta["content"].replace("PT", "")
        h = m = s = "0"
        if len(duration_string.split('H')) == 1:
            # no hour
            if len(duration_string.split('M')) == 1:
                # no minute
                # seconds only
                s = duration_string.split('S')[0]
            else:
                # yes minute
                m = duration_string.split('M')[0]
                s = duration_string.split('M')[1].split('S')[0]
        else:
            h = duration_string.split('H')[0]
            m = duration_string.split('H')[1].split('M')[0]
            s = duration_string.split('H')[1].split('M')[1].split('S')[0]
        duration = {"hour": h, "minute": m, "second": s}
        name_meta = soup.find("meta", {"itemprop": "name"})
        name = name_meta["content"]

        return {"name": name, "duration": duration}
    except:
        return {"error": "invalid url? maybe"}


app = Flask(__name__)
app.config["ENV"] = "production"


@app.route("/", methods=["POST"])
def receive_url():
    url = request.json.get("url")
    if url:
        return jsonify(getVideoMetaDataFromURL(url)), 200
    else:
        return jsonify({""}), 400


if __name__ == "__main__":
    app.run()
