from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "YOUR DB"
db = SQLAlchemy(app)


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # def __repr__(self):
    #     return f"Video(name={name},views={views},likes={likes})"


db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video", required=True)
video_put_args.add_argument("likes", type=str, help="likes of the video", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video", required=True)


# Http response
# def abort_not_found_vid_id(video_id):
#     if video_id not in videos:
#         abort(404, message="video id is not valid")
#
#
# def abort_if_video_id_exist(video_id):
#     if video_id in videos:
#         abort(409, message="video id already exist")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Videos(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.get(id=video_id)
        if not result:
            abort(404, message="video doesn't exist")

        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id)
        if result:
            abort(409, message="video already exist")
        videos = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(videos)
        db.session.commit()
        return videos, 201

    def patch(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id)
        if not result:
            abort(404, message="video can't be updated")
        if args["name"]:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit()
        return result

    @marshal_with(resource_fields)
    def delete(self, video_id):
        video = VideoModel.filter_by(id=video_id).first()
        if not video:
            abort(404,message="video don't exist")
        db.session.delete(video)
        db.commit()
        return '', 204


api.add_resource(Videos, "/helloworld/<int:video_id>")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
