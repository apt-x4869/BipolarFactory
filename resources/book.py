from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_optional,
    fresh_jwt_required
)
from models.book import BookModel

class Book(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('author',
                        type=str,
                        required=False,
                        help="Book must have an Author"
                        )
    parser.add_argument('amazon_url',
                        type=str,
                        required=False,
                        help="Book must have an amazon URL"
                        )
    parser.add_argument('book_genre',
                        type=str,
                        required=False,
                        help="Book must have a genre"
                        )
    @jwt_required
    def get(self, title):
        book = BookModel.find_by_title(title)
        if book:
            return book.json()
        return {"message" : "Book with title'{}'was not found".format(title)}, 404
    
    @fresh_jwt_required
    def post(self, title):
        if BookModel.find_by_title(title=title):
            return {"message": "Book with title'{}' already exsist".format(title)}

        data = Book.parser.parse_args()
        
        book = BookModel(title,**data)

        try:
            book.save_to_db()
        except:
            return {"message": "An Error ocurred while inseting the book"}, 500

        return book.json(), 201
    
    @jwt_required
    def delete(self,title):
        book = BookModel.find_by_title(title)
        if book:
            book.delete_from_db()
            return {"message": "Book has been deleted"}

        return {"message": "Book Not Found in database"}, 404


    @jwt_required
    def put(self,title):
        data = Book.parser.parse_args()
        book = BookModel.find_by_title(title)
        if book:
            book.author = data['author'] if data['author'] else book.author 
            book.amazon_url = data['amazon_url'] if data['amazon_url'] else book.amazon_url
            book.book_genre = data['book_genre'] if data['book_genre'] else book.book_genre
        else:
            book = BookModel(title, **data)
        
        book.save_to_db()

        return book.json()