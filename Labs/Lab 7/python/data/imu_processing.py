# imu_processing.py
# 
# class for processing 6 DoF IMU data (3-axis accelerometer and 3-axis gyroscope)
#     - update([[ax, ay, az], [gx, gy, gz]]) once per loop
# 
# provides the following derived signals:
#     - [x,y,z] = imu.accel     smoothed accelerometer
#     - [x,y,z] = imu.gyro     smoothed gyroscope    
#     - [x,y,z] = imu.tilt     smoothed tilt
#     - mag = imu.magnitude     magnitude of acceleration, with rising and falling smoothing
#     - [x,y,z] = imu.jerk     smoothed derivative of acceleration - no gravity
#     - [x,y,z] = imu.accel_linear     smoothed linear acceleration - no gravity
#     - [x,y,z] = imu.angle     ingegrated angular velocity (will drift!)


import math, time
from data.sensor import Sensor

class IMUProcessing:
    """
    update([[ax, ay, az], [gx, gy, gz]]) once per loop
    """

    def __init__(self, accel_smooth=0.9, gyro_smooth=0.5, tilt_smooth=0.95):
        self._acceleration = [Sensor(alpha=accel_smooth) for _ in range(3)]
#         self._acceleration = {values:[0,0,0], alpha:0.9}
        self._gyro_rotation = [Sensor(alpha=gyro_smooth) for _ in range(3)]
        self._tilt = [Sensor(alpha=tilt_smooth) for _ in range(3)]
        self._magnitude = Sensor(alpha=accel_smooth)
        self._jerk = [Sensor(alpha=accel_smooth) for _ in range(3)]
#         self._angle = [Sensor(alpha=gyro_smooth) for _ in range(3)]
        self._angle = [0,0,0]
        self.accel_raw = [0,0,0]
        self.gyro_raw = [0,0,0]
    
    # ------------------------------------------------------------ outputs
    @property
    def accel(self): return [s.get() for s in self._acceleration]

    @property
    def gyro(self): return [s.get() for s in self._gyro_rotation]

    @property
    def tilt(self): return [s.get() for s in self._tilt]

    @property
    def magnitude(self): return abs(self._magnitude.get() - 1)

    @property
    def jerk(self): return [s.get() for s in self._jerk]

    @property
    def angle(self): return self._angle #[s.get() for s in self._angle]
    
    @angle.setter
    def angle(self, value = [0,0,0]):
        self._angle = value

    # ------------------------------------------------------------- update
    def update(self, accel, gyro):
#         print(gyro[0], self.gyro_raw[0], gyro[0] + self.gyro_raw[0])
        for i in range(3):
            self._acceleration[i].update(accel[i])
            self._gyro_rotation[i].update(gyro[i])
            
            self._jerk[i].update(self.accel_raw[i] - accel[i])
            self._angle[i] = self._angle[i] + gyro[i]
#             self._gyro_rotation[i].update(gyro[i])
            
        self._update_tilt(accel, gyro)
        self._magnitude.update( math.sqrt(accel[0]**2 + accel[1]**2 + accel[2]**2 ) )
        
        # store for next loops calculation
        self.accel_raw = [accel[i] for i in range(3)]
#         self.gyro_raw = [gyro[i] for i in range(3)] 
        
    def _update_tilt(self, accel, gyro):
        """
        Converts gravity distribution into Tilt (Degrees).
        Works best when the device is moving slowly.
        """
        x, y, z = accel
        # math.atan2 is safer than atan as it handles division by zero
        pitch = math.atan2(x, math.sqrt(y*y + z*z)) * 180 / math.pi
        roll = math.atan2(y, math.sqrt(x*x + z*z)) * 180 / math.pi
        yaw = math.atan2(z, math.sqrt(x*x + y*y)) * 180 / math.pi

        self._tilt[0].update(pitch)
        self._tilt[1].update(roll)
        self._tilt[2].update(yaw)
        
        return pitch, roll, yaw
    
    
    # ------------------------------------------------------------ smoothing
    # ---------------------------------------------------- smoothing setters
    @property
    def accel_smoothing(self):
        return self._accel_smooth

    @accel_smoothing.setter
    def accel_smoothing(self, alpha):
        self._accel_smooth = alpha
        for s in self._acceleration: s.alpha = alpha

    @property
    def gyro_smoothing(self):
        return self._gyro_smooth

    @gyro_smoothing.setter
    def gyro_smoothing(self, alpha):
        self._gyro_smooth = alpha
        for s in self._gyro_rotation: s.alpha = alpha

    @property
    def tilt_smoothing(self):
        return self._tilt_smooth

    @tilt_smoothing.setter
    def tilt_smoothing(self, alpha):
        self._tilt_smooth = alpha
        for s in self._tilt: s.alpha = alpha

    @property
    def magnitude_smoothing(self):
        return self._magnitude_smooth

    @magnitude_smoothing.setter
    def magnitude_smoothing(self, alpha):
        self._magnitude_smooth = alpha
        self._magnitude.alpha = alpha

    @property
    def angle_smoothing(self):
        return self._angle_smooth

    @angle_smoothing.setter
    def angle_smoothing(self, alpha):
        self._angle_smooth = alpha
        for s in self._angle: s.alpha = alpha

    @property
    def jerk_smoothing(self):
        return self._jerk_smooth

    @jerk_smoothing.setter
    def jerk_smoothing(self, alpha):
        self._jerk_smooth = alpha
        for s in self._jerk: s.alpha = alpha
