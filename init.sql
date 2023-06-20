-- drop table events;

-- Create the "events" table
CREATE TABLE imu_events (
    id                  SERIAL PRIMARY KEY,
    epoch_time          BIGINT,
    P1time_seconds      INTEGER,
    P1time_fraction_ns  INTEGER,
    acc_x               DECIMAL,
    acc_y               DECIMAL,
    acc_z               DECIMAL,
    acc_std_x           DECIMAL,
    acc_std_y           DECIMAL,
    acc_std_z           DECIMAL,
    gyro_x              DECIMAL,
    gyro_y              DECIMAL,
    gyro_z              DECIMAL,
    gyro_std_x          DECIMAL,
    gyro_std_y          DECIMAL,
    gyro_std_z          DECIMAL
);


CREATE TABLE pose_events (
    id                  SERIAL PRIMARY KEY,
    epoch_time          BIGINT,
    P1time_seconds      INTEGER,
    P1time_fraction_ns  INTEGER,
    GPStime_seconds     INTEGER,
    GPStime_fraction_ns INTEGER,
    solution_type       INTEGER,
    lat                 DECIMAL,
    lon                 DECIMAL,
    alt                 DECIMAL,
    yaw                 DECIMAL,
    pitch               DECIMAL,
    roll                DECIMAL,
    heading             DECIMAL,
    vel_0               DECIMAL,
    vel_1               DECIMAL,
    vel_2               DECIMAL,
    Position_std_enu_m  DECIMAL[]
);
