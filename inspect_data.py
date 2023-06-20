import json

# Specify the path to your JSON file
json_file_path = './GPS_track.json'

# Open the JSON file
with open(json_file_path, 'r') as file:
    # Load the JSON data
    json_data = json.load(file)

    print(len(json_data))
    for timestamp in json_data:
        sensor_label = 'imu' if 'imu' in json_data[timestamp] else 'pose'
        event = json_data[timestamp][sensor_label]
        if sensor_label =='imu':
            print(timestamp, sensor_label, event['acc_x'])
        else:
            print(timestamp, sensor_label, event['yaw'])
