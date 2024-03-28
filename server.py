from flask import Flask, render_template, request, redirect, url_for
import requests


app = Flask(__name__)

api_resp = requests.get('https://v6.exchangerate-api.com/v6/a894066b037cbd847c20ddf9/latest/USD').json()
currencies = api_resp.get('conversion_rates')


@app.route('/')
def index():
    return render_template('pages/index.html', context={
        'currencies': currencies
    })


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    if request.method == 'GET':
        return render_template('pages/index.html', context={
            'currencies': currencies.keys()
    })

    elif request.method == 'POST':
        resp = request.form
        if resp['fromCurrency'] == resp['toCurrency']:
            res = resp['amount']
            fromCurrency = resp['fromCurrency']
            toCurrency = resp['toCurrency']

        else:
            res = round((currencies[resp['toCurrency']] / currencies[resp['fromCurrency']]) * float(resp['amount']), 2)

            if isinstance(res, requests.exceptions.ConnectionError):
                return redirect(url_for('error'))
            else:
                fromCurrency = resp['fromCurrency']
                toCurrency = resp['toCurrency']

        return render_template('pages/index.html', context={
            'currencies': currencies,
            'amount': resp['amount'],
            'fromCurrency': fromCurrency,
            'toCurrency': toCurrency,
            'res': res
        })


@app.route('/error')
def error():
    return render_template('pages/error.html')


if __name__ == '__main__':
    app.run(debug=True)

