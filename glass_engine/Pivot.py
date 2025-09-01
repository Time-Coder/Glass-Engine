import cgmath as cgm
import math
import numpy as np
from typing import Union

import cgmath as cgm


class Pivot:

    def __init__(self, scene_node):
        self._position: cgm.vec3 = cgm.vec3()
        self._position.on_changed = self.update_screens

        self._orientation: cgm.quat = cgm.quat()
        self._orientation.on_changed = self._update_yaw_pitch_roll

        self._scale: cgm.vec3 = cgm.vec3(1)
        self._scale.on_changed = self.update_screens

        self._yaw_pitch_roll: cgm.vec3 = cgm.vec3()
        self._parent_scene_node = scene_node
        self._should_update_yaw_pitch_roll: bool = True
        self._is_set:bool = False
        self._should_callback:bool = True

    def update_screens(self):
        if not self._should_callback:
            return
        
        self._is_set = True
        self._parent_scene_node.update_screens()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position: cgm.vec3):
        self._position[:] = position

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale: Union[cgm.vec3, float]):
        self._scale[:] = scale

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation: cgm.quat):
        self._orientation[:] = orientation

    def rotate(self, axis:cgm.vec3, angle:float):
        angle_rad = angle/180*math.pi
        self._orientation[:] = cgm.quat(math.cos(angle_rad/2), math.sin(angle_rad/2)*axis) * self._orientation

    def translate(self, translation:cgm.vec3):        
        self._position += translation

    def _update_yaw_pitch_roll(self):
        if not self._should_update_yaw_pitch_roll:
            return

        q0 = self._orientation.w
        q1 = self._orientation.x
        q2 = self._orientation.y
        q3 = self._orientation.z
        self._yaw_pitch_roll[0] = (
            math.atan2(2 * (q0 * q3 - q1 * q2), 1 - 2 * (q1 * q1 + q3 * q3))
            / math.pi
            * 180
        )
        self._yaw_pitch_roll[1] = (
            math.asin(np.clip(2 * (q0 * q1 + q2 * q3), -1, 1)) / math.pi * 180
        )
        self._yaw_pitch_roll[2] = (
            math.atan2(2 * (q0 * q2 - q1 * q3), 1 - 2 * (q1 * q1 + q2 * q2))
            / math.pi
            * 180
        )

        self.update_screens()

    def _update_orientation(self):
        yaw = self._yaw_pitch_roll[0] / 180 * math.pi
        pitch = self._yaw_pitch_roll[1] / 180 * math.pi
        roll = self._yaw_pitch_roll[2] / 180 * math.pi

        quat1 = cgm.quat(math.cos(yaw / 2), 0, 0, math.sin(yaw / 2))
        quat2 = cgm.quat(math.cos(pitch / 2), math.sin(pitch / 2), 0, 0)
        quat3 = cgm.quat(math.cos(roll / 2), 0, math.sin(roll / 2), 0)

        self._should_update_yaw_pitch_roll = False
        self.orientation = quat1 * quat2 * quat3
        self._should_update_yaw_pitch_roll = True

        self.update_screens()

    @property
    def yaw(self):
        return self._yaw_pitch_roll[0]

    @yaw.setter
    def yaw(self, yaw: float):
        self._yaw_pitch_roll[0] = yaw
        self._update_orientation()

    @property
    def pitch(self):
        return self._yaw_pitch_roll[1]

    @pitch.setter
    def pitch(self, pitch: float):
        self._yaw_pitch_roll[1] = pitch
        self._update_orientation()

    @property
    def roll(self):
        return self._yaw_pitch_roll[2]

    @roll.setter
    def roll(self, roll: float):
        self._yaw_pitch_roll[2] = roll
        self._update_orientation()
