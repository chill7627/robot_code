from vpython import vector
import json


with open("gyro_offset.json") as f:
    j = json.load(f)
gyro_offsets = vector(j["x"], j["y"], j["z"])
