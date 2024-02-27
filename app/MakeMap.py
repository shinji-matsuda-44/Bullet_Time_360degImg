import numpy as np

class MakeMap:
    def __init__(self) -> None:
        self.viewpoint = -1.0
        self.imagepoint = 1.0
        self.base_imagepoint = self.imagepoint

        self.output_width = 600
        self.output_height = 300
        self.sensor_size = 0.561

        self.sensor_width = self.sensor_size
        self.sensor_height = self.sensor_size * self.output_height / self.output_width

        self.roll = 0
        self.pitch = 0
        self.yaw = 0

        self.drag_rate_x = int(self.output_width/200)
        self.drag_rate_y = self.drag_rate_x*30
        self.wheel_rate = int(self.output_width/50)

        self.g_wheel = 0

        self.phi, self.theta = self.update_map(None, None, True)
        

    def update_map(self, g_diff_x, g_diff_y, is_update_g_diff):
        self.g_diff_x, self.g_diff_y = g_diff_x, g_diff_y
        self.is_update_g_diff = is_update_g_diff

        if is_update_g_diff:
            # GUI操作：ピッチ・ヨー操作 ここが分らん
            if self.g_diff_y is not None and self.g_diff_y != 0:
                self.pitch += (self.g_diff_y / self.drag_rate_y)
                self.pitch %= 360
                if self.pitch > 180:
                    self.pitch -= 360
                self.g_diff_y = 0
            if self.g_diff_x is not None and self.g_diff_x != 0:
                self.yaw -= (self.g_diff_x / self.drag_rate_x)
                self.yaw %= 360
                if self.yaw > 180:
                    self.yaw -= 360
                self.g_diff_x = 0

            # GUI操作：ズーム操作
            self.imagepoint = self.base_imagepoint + (self.g_wheel / self.wheel_rate)
            if self.imagepoint < self.viewpoint:
                self.imagepoint = self.viewpoint
                g_wheel += 1

            # 回転行列生成
            rotation_matrix = self.create_rotation_matrix(
                self.roll,
                self.pitch,
                self.yaw,
            )

            # 角度座標φ, θ算出
            self.phi, self.theta = self.calculate_phi_and_theta(
                self.viewpoint,
                self.imagepoint,
                self.sensor_width,
                self.sensor_height,
                self.output_width,
                self.output_height,
                rotation_matrix,
            )

            return self.phi, self.theta
        
        else:
            return self.phi, self.theta


    def create_rotation_matrix(self, roll, pitch, yaw):
        #print(roll)
        roll = roll * np.pi / 180
        pitch = pitch * np.pi / 180
        yaw = yaw * np.pi / 180

        matrix01 = np.array([
            [1, 0, 0],
            [0, np.cos(roll), np.sin(roll)],
            [0, -np.sin(roll), np.cos(roll)],
        ])

        matrix02 = np.array([
            [np.cos(self.pitch), 0, -np.sin(self.pitch)],
            [0, 1, 0],
            [np.sin(self.pitch), 0, np.cos(self.pitch)],
        ])

        matrix03 = np.array([
            [np.cos(yaw), np.sin(yaw), 0],
            [-np.sin(yaw), np.cos(yaw), 0],
            [0, 0, 1],
        ])

        matrix = np.dot(matrix03, np.dot(matrix02, matrix01))

        return matrix
    
    def calculate_phi_and_theta(
        self,
        viewpoint,
        imagepoint,
        sensor_width,
        sensor_height,
        output_width,
        output_height,
        rotation_matrix,
    ):
        width = np.arange(
            (-1) * sensor_width,
            sensor_width,
            sensor_width * 2 / output_width,
        )
        height = np.arange(
            (-1) * sensor_height,
            sensor_height,
            sensor_height * 2 / output_height,
        )

        ww, hh = np.meshgrid(width, height)

        point_distance = (imagepoint - viewpoint)
        if point_distance == 0:
            point_distance = 0.1

        a1 = ww / point_distance
        a2 = hh / point_distance
        b1 = -a1 * viewpoint
        b2 = -a2 * viewpoint

        a = 1 + (a1**2) + (a2**2)
        b = 2 * ((a1 * b1) + (a2 * b2))
        c = (b1**2) + (b2**2) - 1

        d = ((b**2) - (4 * a * c))**(1 / 2)

        x = (-b + d) / (2 * a)
        y = (a1 * x) + b1
        z = (a2 * x) + b2

        xd = rotation_matrix[0][0] * x + rotation_matrix[0][
            1] * y + rotation_matrix[0][2] * z
        yd = rotation_matrix[1][0] * x + rotation_matrix[1][
            1] * y + rotation_matrix[1][2] * z
        zd = rotation_matrix[2][0] * x + rotation_matrix[2][
            1] * y + rotation_matrix[2][2] * z

        phi = np.arcsin(zd)
        theta = np.arcsin(yd / np.cos(phi))

        xd[xd > 0] = 0
        xd[xd < 0] = 1
        yd[yd > 0] = np.pi
        yd[yd < 0] = -np.pi

        offset = yd * xd
        gain = -2 * xd + 1
        theta = gain * theta + offset

        return phi, theta