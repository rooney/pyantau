import sys
from classifier import classify
from tagger import tagger
from flask import Flask, request, render_template, json, Response
app = Flask(__name__)


def parse(input):
    tagged_words = tagger.tag(input.strip().lower().split(' '))
    commodities = classify(tagged_words)
    return [commodity.serialize() for commodity in commodities]


@app.route("/nlparse.json", methods=['POST'])
def parse_json():
    input = request.form['input']
    resp = Response(json.dumps(parse(input)))
    resp.headers['Content-Type'] = 'application/json'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route("/nlparse.test", methods=['GET', 'POST'])
def parse_test():
    if request.method == 'POST':
        input = request.form['input']
        result = json.dumps(parse(input))
    else:
        input = result = ''
    return render_template('./parse_test.html', input=input, result=result)

if __name__ == "__main__":
    try:
        debug = sys.argv[1] == 'dev'
    except IndexError:
        debug = False
    app.config["JSON_SORT_KEYS"] = False
    app.run(host='0.0.0.0', debug=debug)
