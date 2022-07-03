from flask import Flask, request, jsonify, abort, make_response


from models import cds

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/cds/<int:cd_id>", methods=["GET"])
def get_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    return jsonify({"cd": cd})


@app.route("/cds/", methods=["GET"])
def cds_collection():
    return jsonify(cds.all())


@app.route("/cds/<int:cd_id>", methods=['DELETE'])
def delete_cd(cd_id):
    result = cds.delete(cd_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/cds/", methods=["POST"])
def add_cd():
    if not request.json or not 'title' in request.json:
        abort(400)
    cd = {
        'id': cds.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'artist': request.json['artist'],
        'song_list': request.json['song_list'],
        'genre': request.json['genre'],
        'release': request.json['release']
    }
    cds.create(cd)
    return jsonify({'cd': cd}), 201


@app.route("/cds/<int:cd_id>", methods=["PUT"])
def update_cd(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'artist' in data and not isinstance(data.get('artist'), str),
        'song_list' in data and not isinstance(data.get('song_list'), str),
        'genre' in data and not isinstance(data.get('genre'), str),
        'release' in data and not isinstance(data.get('release'), str),
    ]):
        abort(400)
    cd = {
        'title': data.get('title', cd['title']),
        'artist': data.get('artist', cd['artist']),
        'song_list': data.get('song_list', cd['song_list']),
        'genre': data.get('genre', cd['genre']),
        'release': data.get('release', cd['release'])
    }
    cds.update(cd_id, cd)
    return jsonify({'cd': cd})


@app.route("/favorites_cds/<int:cd_id>", methods=["POST"])
def add_cd_to_favorite(cd_id):
    cd = cds.get(cd_id)
    if not cd:
        abort(404)
    if not request.json:
        abort(400)
    cds.add_favorites(cd_id)
    return jsonify({'cd': cd})


@app.route("/favorites_cds/", methods=["GET"])
def show_favorite_list():
    return jsonify(cds.favorites())


if __name__ == "__main__":
    app.run(debug=True)
