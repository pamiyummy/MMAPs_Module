import bpy
from math import *
from mathutils import *
import numpy as np 
from datetime import datetime
from bpy.app import handlers

# rendering time. This value is reset when 'init_rendertimer' are called.
render_time = 0
__TIMER = 0

# cam_obj: Camera object.
# target_pos: Look at position of camera.
# distance: Distance between camera and target position.
# min_deg, max_deg: The range of degree where camera move.
# num_frame: The number of animation frames.
def cam_animation(cam_obj, target_pos, distance, min_deg, max_deg, num_frame):
    # To prevent zero-devision.
    if num_frame is None or num_frame == 0:
        return

    cam_obj.animation_data_clear()

    deg_per_frame = (max_deg - min_deg) / num_frame

    # Insert animation keyframes to camera.
    deg = min_deg
    frame_count = 0
    while(deg < max_deg):
        x = target_pos.x + distance * sin(radians(deg))
        y = target_pos.y - distance * cos(radians(deg))
        z = target_pos.z 

        cam_obj.location = (x, y, z)
        cam_obj.rotation_euler = (radians(90), 0, radians(-deg))

        cam_obj.keyframe_insert(data_path = 'location', frame = frame_count)
        cam_obj.keyframe_insert(data_path = 'rotation_euler', frame = frame_count)

        deg += deg_per_frame
        frame_count += 1

def __start_timer(scene):
    global __TIMER
    print('start timer')
    __TIMER = datetime.now()

def __end_timer(scene):
    global render_time, __TIMER
    render_time = datetime.now() - __TIMER

def set_rendertimer():
    global render_time, __TIMER
    render_time, __TIMER = 0, 0
    handlers.render_pre.append(__start_timer)
    handlers.render_post.append(__end_timer)


