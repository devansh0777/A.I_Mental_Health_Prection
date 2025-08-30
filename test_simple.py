from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Button Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>Button Test Page</h1>
        <div class="mt-4">
            <a href="/predict" class="btn btn-primary btn-lg me-3">Test Button 1 - /predict</a>
            <a href="/about" class="btn btn-success btn-lg me-3">Test Button 2 - /about</a>
            <button onclick="window.location.href='/predict'" class="btn btn-warning btn-lg">Test Button 3 - JS</button>
        </div>
        <div class="mt-4">
            <p>Click any button to test navigation.</p>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/predict')
def predict():
    return render_template_string('''
<div class="container mt-5">
    <h1>Predict Page Working!</h1>
    <a href="/" class="btn btn-primary">Back to Home</a>
</div>
    ''')

@app.route('/about')
def about():
    return render_template_string('''
<div class="container mt-5">
    <h1>About Page Working!</h1>
    <a href="/" class="btn btn-primary">Back to Home</a>
</div>
    ''')

if __name__ == '__main__':
    app.run(debug=True, port=8082)
