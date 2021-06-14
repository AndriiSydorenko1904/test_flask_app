import csv
import io
import uuid
from multiprocessing import Process
from flask import request, jsonify
from flask.views import MethodView
from database import db, Task, Point, Link
from utils import geo_reverse, all_subsets, distance_meters


def processing(task_id, csv_input):
    link_names = []
    point_tmp = {}
    for row in csv_input:
        name, lat, lon = row[0].split(';')
        link_names.append(name)
        lat, lon = float(lat), float(lon)
        name_geo = geo_reverse(lat, lon)
        point_tmp[name] = [lat, lon]
        point = Point(
            point_name=name,
            latitude=lat,
            longitude=lon,
            task_id=task_id,
            address=name_geo
        )
        db.session.add(point)
    for link_name in all_subsets(link_names):
        geo1, geo2 = point_tmp[link_name[0]], point_tmp[link_name[1]]
        link = Link(
            task_id=task_id,
            link_name=''.join(link_name),
            distance=distance_meters(geo1, geo2)
        )
        db.session.add(link)
    task = Task.query.get(task_id)
    task.status = 'done'
    db.session.commit()


class CalculateDistancesAPI(MethodView):
    def post(self):
        f = request.files.get('data')
        if not f:
            return jsonify("file not loaded")
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        next(csv_input)
        task_uuid = str(uuid.uuid4())

        task = Task(uuid=task_uuid)
        db.session.add(task)
        db.session.flush()
        task_id = task.id
        db.session.commit()

        task_cb = Process(target=processing, args=(task_id, csv_input))
        task_cb.start()
        return jsonify({'task_id': task_uuid, 'status': 'running'})


class ResultAPI(MethodView):
    def get(self):
        task_uuid = request.args.get('task', type=str)
        task = Task.query.filter_by(uuid=task_uuid).first()
        if not task:
            return jsonify('task not exist')
        data = {}
        if task.status == 'done':
            data = {
                'points': [
                    {'name': point.point_name, 'address': point.address}
                    for point in Point.query.filter_by(task_id=task.id).all()
                ],
                'links': [
                    {'name': link.link_name, 'distance': link.distance}
                    for link in Link.query.filter_by(task_id=task.id).all()
                ]
            }
        return jsonify(
            {'task_id': task_uuid, 'status': task.status, 'data': data}
        )
