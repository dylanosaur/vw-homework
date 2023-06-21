import json
from flask import Flask, request, render_template
from flask_cors import CORS

from models import db, IMUEvents, PoseEvents, load_samples, external_session

import pandas as pd
import plotly
import plotly.express as px


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vw_adams:wyvernfiles@db:5432/vw_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'not-a-very-secure-key'

db.init_app(app)
CORS(app)

load_samples(session=external_session())


@app.route('/')
def home():
    # this route will serve as a directory to explore the data
    columns = IMUEvents.__table__.columns
    # remove table name prefix
    columns = [str(x).split('.')[1] for x in columns]
    IMU_containers = [{'name': 'IMU.'+column, 'link': f'/plotly?field={column}&table=IMUEvents'} for column in columns]

    columns_pose = PoseEvents.__table__.columns
    # remove table name prefix
    columns_pose = [str(x).split('.')[1] for x in columns_pose]
    pose_containers = [{'name': 'Pose.'+column, 'link': f'/plotly?field={column}&table=PoseEvents'} for column in columns_pose]

    plot_containers = IMU_containers + pose_containers
    return render_template('all_plots.html', plot_containers=plot_containers)

@app.route('/load_samples')
def load_samples_route():
    # route to load/reload samples
    try:
        limiter = int(request.args.get('limiter'))
        res = load_samples(limiter=limiter)
        return res
    except Exception as ex:
        return f'provide a limiter for the amount of data to load like /load_samples?limiter=1000 \
            or /load_samples?limiter=0 to load all data, ex: {ex}'

@app.route('/sample')
def sample_table():
    # route to debug initial sample loading
    imu = IMUEvents.query.first()
    pose = PoseEvents.query.first()
    return {'IMU': imu.as_dict(), 'POSE': pose.as_dict()}


@app.route('/plotly')
def plotly_generator():
    try:
        field = request.args.get('field')
        table = request.args.get('table')
        if table == 'IMUEvents':
            data = [x.filtered_dict(field) for x in IMUEvents.query.all()]
        else:
            data = [x.filtered_dict(field) for x in PoseEvents.query.all()]

        df = pd.DataFrame(data)
        fig = px.line(df, x='epoch_time', y=field)   
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)   
        return render_template('plot.html', graphJSON=graphJSON)
    except Exception as ex:
        print(ex)
        return f'specify the field like /plotly?field=acc_x&table=IMUEvents from the fields {IMUEvents.__table__.columns}. \n exception: {ex}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
