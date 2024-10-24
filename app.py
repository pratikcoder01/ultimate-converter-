from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home route to display the main page with links to different converters
@app.route('/')
def index():
    return render_template('index.html')  # The main page that links to each converter


# Route to display the Electronic Unit Converter page
@app.route('/electronic')
def electronic_converter():
    return render_template('electronic.html')


# Route to handle the electronic conversion logic
@app.route('/electronic/convert', methods=['POST'])
def electronic_convert():
    try:
        unit_from = request.form['unit_from']
        unit_to = request.form['unit_to']
        input_value_1 = float(request.form['input_value_1'])
        input_value_2 = float(request.form.get('input_value_2', 0))  # Optional second value, default to 0

        result = None
        if unit_from == 'volt' and unit_to == 'amp':
            result = input_value_1 / input_value_2  # I = V/R
        elif unit_from == 'amp' and unit_to == 'volt':
            result = input_value_1 * input_value_2  # V = IR
        elif unit_from == 'ohm' and unit_to == 'volt':
            result = input_value_1 * input_value_2  # V = IR
        elif unit_from == 'farad' and unit_to == 'coulomb':
            result = input_value_1 * input_value_2  # C = CV
        elif unit_from == 'watt' and unit_to == 'volt':
            result = input_value_1 / input_value_2  # V = P/I
        elif unit_from == 'volt' and unit_to == 'watt':
            result = input_value_1 * input_value_2  # P = VI
        elif unit_from == 'amp' and unit_to == 'watt':
            result = input_value_1 * input_value_2  # P = VI
        else:
            return jsonify({'error': 'Conversion not supported for these units.'}), 400

        return jsonify({'result': f'{result:.2f}'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to display the Number System Converter page
@app.route('/number_system')
def number_system_converter():
    return render_template('number_system.html')


# Route to handle number system conversion logic
@app.route('/number_system/convert', methods=['POST'])
def number_system_convert():
    try:
        input_value = request.form['inputValue']
        second_value = request.form.get('secondValue', None)
        input_base = request.form['inputBase']
        output_bases = request.form.getlist('outputBase')
        operation = request.form['operation']

        decimal_value = convert_to_decimal(input_value, input_base)
        decimal_second_value = None
        if second_value:
            decimal_second_value = convert_to_decimal(second_value, input_base)

        result = None
        if operation == 'convert':
            result = convert_to_output_bases(decimal_value, output_bases)
        elif operation == 'addition' and decimal_second_value is not None:
            result = bin(decimal_value + decimal_second_value)[2:]
        elif operation == 'subtraction' and decimal_second_value is not None:
            result = bin(decimal_value - decimal_second_value)[2:]
        elif operation == 'multiplication' and decimal_second_value is not None:
            result = bin(decimal_value * decimal_second_value)[2:]
        elif operation == 'division' and decimal_second_value is not None:
            result = bin(decimal_value // decimal_second_value)[2:]
        elif operation == 'bcdAddition':
            result = bcd_addition(input_value, second_value)
        elif operation == 'bcdSubtraction':
            result = bcd_subtraction(input_value, second_value)

        return render_template('number_system.html', result=result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to display the Bits/Bytes Converter page
@app.route('/bits_bytes')
def bits_bytes_converter():
    return render_template('bits_bytes.html')


# Route to handle bits/bytes conversion logic
@app.route('/bits_bytes/convert', methods=['POST'])
def bits_bytes_convert():
    try:
        input_value = float(request.form['input_value'])
        sub_type = request.form['sub_type']
        if sub_type == 'bits_to_bytes':
            result = bits_to_bytes(input_value)
        elif sub_type == 'bytes_to_bits':
            result = bytes_to_bits(input_value)
        else:
            return jsonify({'error': 'Invalid Conversion Type'}), 400

        return render_template('bits_bytes.html', result=result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Conversion helper functions for number system
def convert_to_decimal(value, base):
    if base == 'binary':
        return int(value, 2)
    elif base == 'octal':
        return int(value, 8)
    elif base == 'hexadecimal':
        return int(value, 16)
    else:
        return int(value)

@app.route('/bytes')
def bytes_converter():
    return render_template('bytes.html')

def convert_to_output_bases(decimal_value, output_bases):
    results = {}
    for base in output_bases:
        if base == 'binary':
            results['Binary'] = bin(decimal_value)[2:]
        elif base == 'octal':
            results['Octal'] = oct(decimal_value)[2:]
        elif base == 'hexadecimal':
            results['Hexadecimal'] = hex(decimal_value)[2:].upper()
        else:
            results['Decimal'] = str(decimal_value)
    return results


def bcd_addition(a, b):
    return str(int(a) + int(b))


def bcd_subtraction(a, b):
    return str(int(a) - int(b))


def bits_to_bytes(bits):
    return bits / 8


def bytes_to_bits(bytes):
    return bytes * 8


if __name__ == '__main__':
    app.run(debug=True)

