from math import radians, cos, acos, sin, fabs, degrees, atan2
import numpy as np
from numpy import array
from shapely.geometry import Polygon

print("""
=====HELP=====
func get_points_for_draw
    Slug -- (points body for polygon, pos eyes)
    Bird -- (points body for polygon, pos eyes, points wings for polygon)
""")

def rotation_vector2(vector: array, angle: float) -> array:
    rad_angle = radians(angle)
    new_vector = array([0,0], dtype=float)

    new_vector[0] = vector[0] * cos(rad_angle) - vector[1] * sin(rad_angle)
    new_vector[1] = vector[0] * sin(rad_angle) + vector[1] * cos(rad_angle)

    return new_vector

def rotate_vector_to_vector(v1: array, v2: array, max_angle: float):
    v1_n = v1 / np.linalg.norm(v1)
    v2_n = v2 / np.linalg.norm(v2)

    # кут між векторами
    dot = np.clip(np.dot(v1_n, v2_n), -1.0, 1.0)
    angle_between = degrees(acos(dot))

    if angle_between <= max_angle:
        return v2

    cross = v1_n[0]*v2_n[1] - v1_n[1]*v2_n[0]
    direction = 1 if cross > 0 else -1

    return rotation_vector2(v1, max_angle * direction)

class BodyBall:
    def __init__(self, radius):
        self.pos = array([0,0])
        self.angle = 0
        self.move_dir = array([0,0])

        self.left_point_pos = array([0,0])
        self.right_point_pos = array([0,0])

        self.forward_point_pos = array([-radius, 0])
        self.left_forward_point_pos = rotation_vector2(self.forward_point_pos, -45)
        self.right_forward_point_pos = rotation_vector2(self.forward_point_pos, 45)

        self.backward_point_pos = None
        self.left_backward_point_pos = None
        self.right_backward_point_pos = None

        self.radius = radius

class Wings:
    def __init__(self, amplitude: float = 1.5, speed: float = 10, time: float = 0):
        self.amplitude = amplitude
        self.speed = speed
        self.time = time

        self.points = array([])

    def update_wings(self, position: array, angle: float):
        points = []
        x = -self.amplitude
        while x < self.amplitude:
            y = fabs(x) * sin(fabs(x) + self.speed * self.time)
            dir = array([(x * 100), (y * 100)])
            dir = rotation_vector2(dir, angle)
            points.append(position+dir)
            x += 10 ** -2
        self.time += 10**-3

        self.points = array(points)

class Animal:
    def __init__(self, size_factor: float=1.0):
        self.animal_name = "animal name"
        self.size_factor = size_factor
        self._body = self._create_animal()

    # TODO: extract form class
    def _create_animal(self) -> [BodyBall]:
        balls = []
        if self.animal_name == "slug":
            size = [x * self.size_factor for x in [34, 42, 43, 42, 41, 38, 32, 30, 25, 19, 17, 16, 9, 7]]
        elif self.animal_name == "bird":
            size = [x * self.size_factor for x in [20,25,30,35,36,35,30,15]]
        elif self.animal_name == "snakeIO":
            size = [x * self.size_factor for x in [self.ball_radius]*self.length]
        for i in range(len(size)):
            balls.append(BodyBall(size[i]))

            if self.animal_name == "snakeIO":
                balls[-1].pos[0] = 400
            else:
                balls[-1].pos[0] = i * max(size) + 400
            balls[-1].pos[1] = 300

        return balls


    def move_animal(self, go_to: tuple, speed):
        direction = (self._body[0].pos - go_to)*1
        dr_dir = direction*-1
        self._body[0].angle = degrees(atan2(direction[1], direction[0]))+90
        distance = np.linalg.norm(direction)
        if distance > self._body[0].radius:
            direction = direction / distance
            self._body[0].pos = self._body[0].pos - direction * speed

            right_d = rotation_vector2(direction, 90)
            left_d = rotation_vector2(direction, -90)
            self._body[0].left_point_pos = self._body[0].pos + left_d * self._body[0].radius
            self._body[0].right_point_pos = self._body[0].pos + right_d * self._body[0].radius
            self._body[0].forward_point_pos = self._body[0].pos - direction * self._body[0].radius

            left_forward_d = rotation_vector2(direction, -135)
            right_forward_d = rotation_vector2(direction, 135)
            self._body[0].left_forward_point_pos = self._body[0].pos + left_forward_d * self._body[0].radius
            self._body[0].right_forward_point_pos = self._body[0].pos + right_forward_d * self._body[0].radius

        for index, ball in enumerate(self._body[1:]):
            prev = self._body[index].pos
            curr = ball.pos
            direction = prev - curr
            distance = np.linalg.norm(direction)
            if distance != 0:
                direction = direction / distance
                ball.angle = degrees(atan2(direction[1], direction[0]))-90
                ball.pos = prev - direction * ball.radius
                ball.left_point_pos = ball.pos + rotation_vector2(direction, 90) * ball.radius
                ball.right_point_pos = ball.pos + rotation_vector2(direction, -90) * ball.radius

                if index == len(self._body) - 2:
                    left_d = rotation_vector2(direction, -135)
                    right_d = rotation_vector2(direction, 135)

                    ball.backward_point_pos = ball.pos - direction * ball.radius
                    ball.left_backward_point_pos = ball.pos + left_d * ball.radius
                    ball.right_backward_point_pos = ball.pos + right_d * ball.radius
        return (dr_dir, self._body[0].pos)

    def get_points_for_draw(self):
        points = [self._body[0].forward_point_pos, self._body[0].left_forward_point_pos]
        for ball in self._body:
            points.append(ball.left_point_pos)
        points.append(self._body[-1].right_backward_point_pos)
        points.append(self._body[-1].backward_point_pos)
        points.append(self._body[-1].left_backward_point_pos)
        for ball in self._body[::-1]:
            points.append(ball.right_point_pos)
        points.append(self._body[0].right_forward_point_pos)
        print(points)
        poly = Polygon(points)
        fixed = poly.buffer(0)
        try:
            points = list(fixed.exterior.coords)
        except AttributeError or TypeError:
            pass
        return (points, [self._body[0].left_forward_point_pos, self._body[0].right_forward_point_pos], )

    def debug(self):
        result = list()

        skeletons = list()
        points = list()
        body = list()

        for index, ball in enumerate(self._body):
            direction = rotation_vector2(array([0, 1]) * ball.radius, ball.angle)

            angle_pos = ball.pos + direction

            skeletons.append((ball.pos, angle_pos))

            points.append(ball.left_point_pos)
            points.append(ball.right_point_pos)
            if ball.forward_point_pos is not None:
                points.append(ball.forward_point_pos)
                points.append(ball.left_forward_point_pos)
                points.append(ball.right_forward_point_pos)
            elif ball.backward_point_pos is not None:
                points.append(ball.backward_point_pos)
                points.append(ball.left_backward_point_pos)
                points.append(ball.right_backward_point_pos)

            body.append((ball.pos, ball.radius))

        result.append(skeletons)
        result.append(points)
        result.append(body)

        return result

    def get_head_rect(self):
        head_pos = self._body[0].pos
        head_radius = self._body[0].radius

        left_top_pos = (head_pos[0] - head_radius, head_pos[1]-head_radius)
        return (left_top_pos[0], left_top_pos[1], head_radius*2, head_radius*2)

class Slug(Animal):
    def __init__(self, size_factor: float = 1.0):
        self.animal_name = "slug"
        self.size_factor = size_factor
        self._body = self._create_animal()

    def get_points_for_draw(self):
        points = [self._body[0].forward_point_pos, self._body[0].left_forward_point_pos]
        for ball in self._body:
            points.append(ball.left_point_pos)
        points.append(self._body[-1].right_backward_point_pos)
        points.append(self._body[-1].backward_point_pos)
        points.append(self._body[-1].left_backward_point_pos)
        for ball in self._body[::-1]:
            points.append(ball.right_point_pos)
        points.append(self._body[0].right_forward_point_pos)
        poly = Polygon(points)
        fixed = poly.buffer(0)
        try:
            points = list(fixed.exterior.coords)
        except AttributeError or TypeError:
            pass
        return (points, [self._body[0].left_forward_point_pos, self._body[0].right_forward_point_pos])

    def debug(self):
        result = super().debug()
        return result

class Bird(Animal):
    def __init__(self, size_factor: float = 1.0, amplitude: float = 1.5, speed: float = 10):
        self.animal_name = "bird"
        self.size_factor = size_factor
        self._body = self._create_animal()

        self._wings = Wings(amplitude, speed)
        self.wings_poly_points = array([])
        self.pin_body_index_wings = 3

    def get_points_for_draw(self):
        points = [self._body[0].forward_point_pos, self._body[0].left_forward_point_pos]
        for ball in self._body:
            points.append(ball.left_point_pos)
        points.append(self._body[-1].right_backward_point_pos)
        points.append(self._body[-1].backward_point_pos)
        points.append(self._body[-1].left_backward_point_pos)
        for ball in self._body[::-1]:
            points.append(ball.right_point_pos)
        points.append(self._body[0].right_forward_point_pos)
        poly = Polygon(points)
        fixed = poly.buffer(0)
        try:
            points = list(fixed.exterior.coords)
        except AttributeError or TypeError:
            pass

        return (points, [self._body[0].left_forward_point_pos, self._body[0].right_forward_point_pos], self.wings_poly_points)

    def move_animal(self, go_to: tuple, speed):
        super().move_animal(go_to, speed)

        self._wings.update_wings(self._body[self.pin_body_index_wings].pos, self._body[self.pin_body_index_wings].angle+90)
        width = 50
        len_line = []
        for index, n in enumerate(self._wings.points):
            if index < len(self._wings.points) // 2:
                len_line.append(width / (len(self._wings.points) / 2) * (index + 1))
        for i in len_line.copy()[::-1]:
            len_line.append(i)

        points_for_draw = []
        for index, l in enumerate(len_line):
            points_for_draw.append((self._wings.points[index][0], self._wings.points[index][1] - (l / 2)))
        for index, l in enumerate(len_line[::-1]):
            real_index = len(len_line) - 1 - index
            points_for_draw.append((self._wings.points[real_index][0], self._wings.points[real_index][1] + (l / 2)))

        self.wings_poly_points = points_for_draw

    def debug(self):
        result = super().debug()
        return result

class SnakeIO(Animal):
    def __init__(self, size_factor: float = 1.0, length: int = 10, ball_radius: float= 10, void_with_out_ball: float = 5, rotated_speed:float = 5):
        self.animal_name = "snakeIO"
        self.size_factor = size_factor

        self.length = length
        self.ball_radius = ball_radius
        self.void_with_out_ball = void_with_out_ball
        self.rotated_speed = rotated_speed

        self._body = self._create_animal()

    def move_animal(self, go_to: tuple, speed):
        dir_to_pos = array(go_to) - self._body[0].pos
        self_dir = rotation_vector2(array([0, 1]), self._body[0].angle)
        new_dir = rotate_vector_to_vector(self_dir, dir_to_pos, self.rotated_speed)
        direction = new_dir / np.linalg.norm(new_dir)  # нормалізували
        velocity = direction * speed*10
        new_target = self._body[0].pos + velocity

        "start"
        direction = (self._body[0].pos - new_target) * 1
        self._body[0].angle = degrees(atan2(direction[1], direction[0])) + 90
        distance = np.linalg.norm(direction)

        direction = direction / distance
        self._body[0].pos = self._body[0].pos - direction * speed
        self._body[0].move_dir = direction*-1

        right_d = rotation_vector2(direction, 90)
        left_d = rotation_vector2(direction, -90)
        self._body[0].left_point_pos = self._body[0].pos + left_d * self._body[0].radius
        self._body[0].right_point_pos = self._body[0].pos + right_d * self._body[0].radius
        self._body[0].forward_point_pos = self._body[0].pos - direction * self._body[0].radius

        left_forward_d = rotation_vector2(direction, -135)
        right_forward_d = rotation_vector2(direction, 135)
        self._body[0].left_forward_point_pos = self._body[0].pos + left_forward_d * self._body[0].radius
        self._body[0].right_forward_point_pos = self._body[0].pos + right_forward_d * self._body[0].radius

        for index, ball in enumerate(self._body[1:]):
            # prev = self._body[index]
            # ball.pos = prev.pos - rotation_vector2(array([0,10]), prev.angle)

            # prev = self._body[index].pos
            # curr = ball.pos
            # direction = prev - curr
            # distance = np.linalg.norm(direction)
            #
            # direction = direction / distance
            # ball.angle = degrees(atan2(direction[1], direction[0])) - 90

            # move_dir = rotation_vector2(array([0,1], dtype=float), ball.angle)
            ball.pos = ball.pos + ball.move_dir*speed

            ball.left_point_pos = ball.pos + rotation_vector2(direction, 90) * ball.radius
            ball.right_point_pos = ball.pos + rotation_vector2(direction, -90) * ball.radius

            if index == len(self._body) - 2:
                left_d = rotation_vector2(direction, -135)
                right_d = rotation_vector2(direction, 135)

                ball.backward_point_pos = ball.pos - direction * ball.radius
                ball.left_backward_point_pos = ball.pos + left_d * ball.radius
                ball.right_backward_point_pos = ball.pos + right_d * ball.radius

        for ball in self._body[len(self._body):0:-1]:
            index_b = self._body.index(ball)-1
            ball.move_dir = self._body[index_b].move_dir
            ball.angle = self._body[index].angle

        "end"

        return (new_dir, self_dir, dir_to_pos, self._body[0].pos, new_target)

    def get_points_for_draw(self):
        balls_pos = [x.pos for x in self._body]

        return (self.ball_radius, balls_pos, [self._body[0].left_forward_point_pos, self._body[0].right_forward_point_pos])

    def add_ball(self, ball_count: int = 1):
        for i in range(ball_count):
            self._body.append(BodyBall(self.ball_radius))
            self._body[-1].pos = self._body[-2].pos

    def magnification_radius_ball(self, add_r: float):
        pass
