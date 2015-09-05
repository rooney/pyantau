import sys
from classifier import classify
from tagger import tagger
from flask import Flask, request, render_template, json
app = Flask(__name__)

@app.route("/parse", methods=['GET', 'POST'])
def parse():
    if request.method == 'POST':
        input = request.form['input']
        tagged_words = tagger.tag(input.split(' '))
        commodities = classify(tagged_words)
        result = json.dumps([commodity.serialize() for commodity in commodities])
    else:
        input = result = ''
    return render_template('./parse_test.html', input=input, result=result)

if __name__ == "__main__":
    try:
        debug = sys.argv[1] == 'dev'
    except IndexError:
        debug = False
    app.config["JSON_SORT_KEYS"] = False
    app.run(debug=debug)
