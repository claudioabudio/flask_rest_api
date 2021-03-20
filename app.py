from flask import Flask, jsonify, request, Response
import json
from BookModel import *
from settings import *
# app = Flask(__name__)
print(__name__)

# this was just for prototyping without using a database !
# books = [
# {
#     'name' : 'Gren eggs and ham',
#     'price' : 7.99,
#     'isbn' : 978039400165
# },
# {
#    'name' : 'The cat in the hat',
#     'price' : 6.99,
#     'isbn' : 9782371000193

# }

# ]


def validBookObject(book):
    if ('price' in book and 'isbn' in book and 'name' in book):
        return True
    else:
        return False

@app.route('/books')
def get_books():
    return jsonify({'books' : Book.get_books()})

@app.route('/books', methods=['POST'])
def add_book():
    book = request.get_json()
    if validBookObject(book):
        Book.add_book(book['name'], book['price'], book['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/" + str(book['isbn'])
        return response
    else:
        invalidBookErrorMsg = {
            "error" : "Invalid book object passed in request",
            "helpString" : "figure it out !"
        }
        response = Response(json.dumps(invalidBookErrorMsg), 400, mimetype='application/json')
        return response

@app.route("/books/<int:isbn>")
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    print(type(isbn))
    return jsonify(return_value)

@app.route("/books/<int:isbn>", methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    Book.replace_book(request_data['name'], request_data['price'], isbn)
    response = Response("", status=204)    
    return response

@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if 'name' in request_data:
        Book.update_book_name(request_data['name'], isbn)
    if 'price' in request_data:
        Book.update_book_price(request_data['price'], isbn)
    response = Response("", status=204)    
    response.headers['Location'] = "/books/" + str(isbn)
    return response

@app.route("/books/<int:isbn>", methods=['DELETE'])
def delete_book(isbn):
    if Book.delete_book(isbn):
        response = Response("", status=204)
        return response
    else:
        invalidBookErrorMsg = {
            "error" : "The book with the ISBN that was passed was not found",
            "helpString" : "figure it out !"
        }
        response = Response(json.dumps(invalidBookErrorMsg), status=404, mimetype='application/json')
        return response

if __name__ == "__main__":
   app.run(port=5000)