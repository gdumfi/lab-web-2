from flask import Flask, render_template, request, make_response

app = Flask(__name__)
application = app

@app.route('/')
def index():
    url = request.url
    return render_template('index.html', url=url)

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if 'username' in request.cookies:
        response.delete_cookie(key='username')
    else:
        response.set_cookie('username', 'student')
    if 'password' in request.cookies:
        response.delete_cookie(key='password')
    else:
        response.set_cookie('password', '12345678')
    return response

@app.route('/form', methods=['get',"post"])
def form():
    return render_template('form.html')

@app.route('/calculate', methods=['get',"post"])
def calculate():
    res = ""
    if request.method == "POST":
        if not(request.form["number1"].isdigit()):
            msg = "Первое значение должно быть числом!"
            return render_template('calculate.html', msg=msg)
        if not(request.form["number2"].isdigit()):
            msg = "Второе значение должно быть числом!"
            return render_template('calculate.html', msg=msg)
        a = int(request.form["number1"])
        b = int(request.form["number2"])
        operator = request.form["operator"]
        if operator == "+":
            res = a+b
        elif operator == "-":
            res = a-b
        elif operator == "*":
            res = a*b
        elif operator == "/":
            if b==0:
                msg = "Делить на 0 нельзя!"
                return render_template('calculate.html', msg=msg)
            res = a/b
    return render_template('calculate.html', res=res)
    
@app.route('/check-phone-number', methods=['get',"post"])
def check_phone_number():
    if request.method == "GET":
        return render_template("check_phone_number.html", msg = "0")
    else:
        phone_number = request.form["check_number1"]
        acceptable_symbols_except_figures = [" ", "(", ")", ".", "+", "-"]
        counter_of_figures = 0
        for i in phone_number:
            if i.isdigit():
                counter_of_figures += 1
        if counter_of_figures == 11 and not(phone_number[:2] == "+7"):#8 495 223 05 23
                return render_template("check_phone_number.html", msg = "1")
        elif counter_of_figures == 10 and not(phone_number[0] == "8"):#исправленное условие
                return render_template("check_phone_number.html", msg = "1")
    for i in phone_number:
        if not(i in acceptable_symbols_except_figures or i.isdigit()):
            return render_template("check_phone_number.html", msg = "2")

    #исправленное форматирование номера телефона
    formating_phone_nuber = phone_number
    if formating_phone_nuber[0] == '+':
        formating_phone_nuber = formating_phone_nuber.replace('+7', '8', 1)
    if formating_phone_nuber[0] != '8':
        formating_phone_nuber = '8' + formating_phone_nuber
    """Здесь было 9 строк"""
    for symb in acceptable_symbols_except_figures:
        formating_phone_nuber = formating_phone_nuber.replace(symb, '')
    formating_phone_nuber = formating_phone_nuber[0] + '-' + formating_phone_nuber[1:4] + '-' + formating_phone_nuber[4:7] + '-' + formating_phone_nuber[7:9] + '-' + formating_phone_nuber[9:]
    return render_template("check_phone_number.html", msg = "3", phone_number = formating_phone_nuber)

if __name__ == "__main__":
    app.run(debug=True)
