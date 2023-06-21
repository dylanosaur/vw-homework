import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, Integer, BigInteger, ARRAY, create_engine

db = SQLAlchemy()

class IMUEvents(db.Model):
    __tablename__ = 'imu_events'

    id = Column(Integer, primary_key=True)
    epoch_time = Column(BigInteger)
    p1time_seconds = Column(Integer)
    p1time_fraction_ns = Column(Integer)
    acc_x = Column(Float)
    acc_y = Column(Float)
    acc_z = Column(Float)
    acc_std_x = Column(Float)
    acc_std_y = Column(Float)
    acc_std_z = Column(Float)
    gyro_x = Column(Float)
    gyro_y = Column(Float)
    gyro_z = Column(Float)
    gyro_std_x = Column(Float)
    gyro_std_y = Column(Float)
    gyro_std_z = Column(Float)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def filtered_dict(self, y):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns if column.name in ['epoch_time', y]}


class PoseEvents(db.Model):
    __tablename__ = 'pose_events'

    id = Column(Integer, primary_key=True)
    epoch_time = Column(BigInteger)
    p1time_seconds = Column(Integer)
    p1time_fraction_ns = Column(Integer)
    gpstime_seconds = Column(Integer)
    gpstime_fraction_ns = Column(Integer)
    solution_type = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    alt = Column(Float)
    yaw = Column(Float)
    pitch = Column(Float)
    roll = Column(Float)
    heading = Column(Float)
    vel_0 = Column(Float)
    vel_1 = Column(Float)
    vel_2 = Column(Float)
    position_std_enu_m = Column(ARRAY(Float))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def filtered_dict(self, y):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns if column.name in ['epoch_time', y]}


from sqlalchemy.orm import sessionmaker
import time
def external_session():
    # Create a database engine
    time.sleep(2)
    engine = create_engine('postgresql://vw_adams:wyvernfiles@db:5432/vw_db')

    # Create a session factory
    Session = sessionmaker(bind=engine)

    # Create a new session
    session = Session()
    return session

def load_samples(limiter=0, session = db.session):

    # clear all samples
    session.query(IMUEvents).delete()
    session.query(PoseEvents).delete()

    # Specify the path to your JSON file
    json_file_path = './GPS_track.json'

    count_imu = 0
    count_pose = 0

    # Open the JSON file
    with open(json_file_path, 'r') as file:
        # Load the JSON data
        json_data = json.load(file)

        print(len(json_data))
        # by default we will only load the first 1000 events
        # but if you visit /load_samples?limiter=0 it will load all the events
        if limiter == 0:
            limiter = len(json_data)

        for timestamp in json_data:
            if count_imu + count_pose > limiter:
                break
            sensor_label = 'imu' if 'imu' in json_data[timestamp] else 'pose'
            event = json_data[timestamp][sensor_label]
            if sensor_label =='imu':
                # print(timestamp, sensor_label, event['acc_x'])

                datum = IMUEvents(epoch_time=timestamp, 
                                  p1time_seconds=event['P1time.seconds'], 
                                  p1time_fraction_ns=event['P1time.fraction_ns'],
                                  acc_x=event['acc_x'], 
                                  acc_y=event['acc_y'],
                                  acc_z=event['acc_z'],
                                  acc_std_x=event['acc_std_x'],
                                  acc_std_y=event['acc_std_y'],
                                  acc_std_z=event['acc_std_z'],
                                  gyro_x=event['gyro_x'],
                                  gyro_y=event['gyro_y'],
                                  gyro_z=event['gyro_z'],
                                  gyro_std_x=event['gyro_std_x'],
                                  gyro_std_y=event['gyro_std_y'],
                                  gyro_std_z=event['gyro_std_z']
                                )
                session.add(datum)
                count_imu += 1
            else:
                # print(timestamp, sensor_label, event['yaw'])
                datum = PoseEvents(epoch_time=timestamp, 
                    p1time_seconds=event['P1time.seconds'], 
                    p1time_fraction_ns=event['P1time.fraction_ns'],
                    gpstime_seconds=event['GPStime.seconds'], 
                    gpstime_fraction_ns=event['GPStime.fraction_ns'],
                    solution_type=event['solution_type'],
                    lat=event['lat'],
                    lon=event['lon'],
                    alt=event['alt'],
                    yaw=event['yaw'],
                    pitch=event['pitch'],
                    roll=event['roll'],
                    heading=event['heading'],
                    vel_0=event['vel_0'],
                    vel_1=event['vel_1'],
                    vel_2=event['vel_2'],
                    position_std_enu_m=event['Position_std_enu_m']
                )
                session.add(datum)
                count_pose += 1
        session.commit()
    return f"loaded {count_imu} IMU events and {count_pose} pose events"
