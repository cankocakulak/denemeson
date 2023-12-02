from flask import Flask, request

app = Flask(__name__)

@app.route('/choose', methods=['POST'])
def choose_best_option():
    name = request.form['name']
    total_score = sum(int(request.form[f'q{i}']) for i in range(1, 6))

    # Define scores, URLs, and stock data in separate dictionaries
    scores = {
        'Gül': 20,
        'Eleya': 30,
        'Rüya': 40
    }

    urls = {
        'Gül': 'https://shop.kantakademi.com/products/gul-rana?selling_plan=690226987316&variant=47176726446388',
        'Eleya': 'https://shop.kantakademi.com/products/eleya-ovul?selling_plan=690226987316&variant=47163825553716',
        'Rüya': 'https://shop.kantakademi.com/products/ruya?selling_plan=690226987316&variant=47176726249780'
    }

    stock_data = {
        'Gül': 2,
        'Eleya': 2,
        'Rüya': 2
    }

    preview_image_urls = {
        'Gül': 'https://shop.kantakademi.com/cdn/shop/products/1EeoN_LzlHrnOd2LnUq9Ujt3kvnGtxvw5.jpg?v=1700439401&width=600',
        'Eleya': 'https://shop.kantakademi.com/cdn/shop/files/EleyaOvulMadak.jpg?v=1698185012&width=600',
        'Rüya': 'https://shop.kantakademi.com/cdn/shop/products/12yFqoDWkeVOHXwDCk3PJZ3sJ5SzaENVi.jpg?v=1700439387&width=360'
    }

    # Combine the data for sorting and filtering
    options = {name: {'score': scores[name], 'url': urls[name], 'stock': stock_data[name]} for name in scores}

    # Filter out options that are out of stock
    in_stock_options = {name: info for name, info in options.items() if info['stock'] > 0}

    # Sort the in-stock options based on their closeness to the total_score
    sorted_options = sorted(in_stock_options.items(), key=lambda x: abs(x[1]['score'] - total_score))

    # Get the two best options
    best_options = sorted_options[:2]

    # Generate HTML content for the best options
    best_options_content = ""
    for option_name, option_info in best_options:
        preview_image_url = preview_image_urls.get(option_name, '') # Default to empty string if not found

        best_options_content += f'''
            <div class="result">
                <h2>{option_name}</h2>
                <img src="{preview_image_url}" alt="Önizleme" class="option-image">
                <div class="button-container">
                    <a href="{option_info['url']}" target="_blank"><button>Koçluğa Başla!</button></a>
                </div>
            </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sonuç Sayfası</title>
        <style>
            body {{ text-align: center; }}
            .results-container {{ display: flex; flex-wrap: wrap; justify-content: center; }}
            .result {{ margin: 10px; flex-basis: calc(50% - 20px); text-align: center; box-sizing: border-box; }}
            .option-image {{ width: 100%; max-width: 250px; height: auto; margin: auto; display: block; }}
            .button-container {{ margin-top: 10px; }}
            .button-container button {{ background-color: #b60000; color: white; padding: 10px 20px; border: none; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>{name}, senin için en uygun iki seçenek:</h1>
        <div class="results-container">
            {best_options_content}
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
