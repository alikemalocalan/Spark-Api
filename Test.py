from flask import Flask, jsonify
from flask import request
from flask_request_params import bind_request_params
from pyspark import Row
from pyspark import StorageLevel
from pyspark.sql import SparkSession


def sparktest():
    spark = SparkSession \
        .builder \
        .appName("Spark Test") \
        .getOrCreate()

    sc = spark.sparkContext

    tracks_txt = "dataset/unique_tracks.txt"

    track_line = sc.textFile(tracks_txt)

    track_parts = track_line.map(lambda l: l.split(",")) \
        .map(lambda p: Row(trackID=p[0], songID=p[1], artistName=p[2], songTitle=p[3])) \
        .persist(StorageLevel.MEMORY_ONLY) \
        .cache()

    schemaSongs = spark.createDataFrame(track_parts)

    singer = 'Kruiz'
    result = schemaSongs \
        .filter(schemaSongs.artistName == singer) \
        .show()


app = Flask(__name__)


def save_request(request):
    req_data = {}
    req_data['endpoint'] = request.endpoint
    req_data['method'] = request.method
    req_data['data'] = request.data
    req_data['headers'] = dict(request.headers)
    req_data['args'] = request.args
    req_data['form'] = request.form
    req_data['remote_addr'] = request.remote_addr
    return req_data


def save_response(resp):
    resp_data = {}
    resp_data['status_code'] = resp.status_code
    resp_data['status'] = resp.status
    resp_data['headers'] = dict(resp.headers)
    resp_data['data'] = resp.response
    return resp_data


@app.before_request
def before_request():
    print(request.method, request.path)


app.before_request(bind_request_params)


@app.after_request
def after_request(resp):
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Allow-Headers', 'Content-Type, X-Token')
    resp.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
    resp.headers['server'] = 'BitirmeServer'
    save_response(resp)
    return resp


@app.route('/')
def index():
    return jsonify(request.params)


if __name__ == '__main__':
    app.run()
