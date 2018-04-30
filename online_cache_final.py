from flask import Flask, request
from flask_restful import Api, Resource
from cacheout import Cache

app = Flask(__name__)
api = Api(app)

document_cache = Cache(maxsize=1000, ttl=15)


class Message(Resource):

    def get(self, doc_id):
        doc_id = int(doc_id)
        if doc_id in document_cache:
            return document_cache.get(doc_id)
        return 'Resource not found', 404

    def put(self, doc_id):
        doc_id = int(doc_id)
        if doc_id not in document_cache: return 'Resource not found', 404
        document_cache.set(doc_id, request.form['doc'])
        return {doc_id: document_cache.get(doc_id)}, 201

    def delete(self, doc_id):
        doc_id = int(doc_id)
        document_cache.delete(doc_id), 204


class Messages(Resource):
    def get(self):
        return document_cache.copy()

    def post(self):
        doc_id = document_cache.size() + 1
        document_cache.set(doc_id, request.form['doc'])
        return document_cache.get(doc_id), 201

    def delete(self):
        document_cache.clear()


api.add_resource(Messages, '/messages')
api.add_resource(Message, '/messages/<doc_id>')

if __name__ == '__main__':
    app.run(debug=True)
