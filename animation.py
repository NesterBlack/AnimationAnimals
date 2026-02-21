import pygame
import math
from shapely.geometry import Polygon

def rotation_vector2(vector: array, angle: float) -> array:
    new_vector = array([0,0])

    new_vector[0] = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
    new_vector[1] = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)

    return new_vector

class BodyBall:
    def __init__(self, surface, radius):
        self.surface = surface
        self.pos = pygame.Vector2(0, 0)
        self.angle = 0

        self.left_point_pos = None
        self.right_point_pos = None

        self.forward_point_pos = None
        self.left_forward_point_pos = None
        self.right_forward_point_pos = None

        self.backward_point_pos = None
        self.left_backward_point_pos = None
        self.right_backward_point_pos = None

        self.radius = radius




class Animal:
    def __init__(self, size_factor: float=1.0, color: tuple=(79, 227, 134), debug: bool=False):
        self.animal_name = "animal name"
        self.size_factor = size_factor
        self.color = color
        self.debug = debug
        self._body = self._create_animal(self.animal_name, self.size_factor)

    # TODO: extract form class
    def _create_animal(self, animal="slug", size_factor=1) -> [BodyBall]:
        balls = []
        if animal.lower() == "slug":
            size = [x * size_factor for x in [34, 42, 43, 42, 41, 38, 32, 30, 25, 19, 17, 16, 9, 7]]
        for i in range(len(size)):
            balls.append(BodyBall(self.surface, size[i]))
            balls[-1].pos[0] = i*max(size)
            balls[-1].pos[1] = self.surface.get_height()//2

        return balls

    
    def move_animal(self, go_to: tuple, speed):
        direction = self._body[0].pos - go_to
        self._body[0].angle = math.degrees(math.atan2(direction[1], direction[0]))
        distance = np.linalg.norm(direction)
        if distance != 0:
            direction = direction / distance
            self._body[0].pos = self._body[0].pos - direction * (distance * speed)

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
                ball.angle = math.degrees(math.atan2(direction[1], direction[0]))
                ball.pos = prev - direction * ball.radius
                ball.left_point_pos = ball.pos + rotation_vector2(direction, 90) * ball.radius
                ball.right_point_pos = ball.pos + rotation_vector2(direction, -90) * ball.radius

                if index == len(self._body) - 2:
                    left_d = rotation_vector2(direction, -135)
                    right_d = rotation_vector2(direction, 135)

                    ball.backward_point_pos = ball.pos - direction * ball.radius
                    ball.left_backward_point_pos = ball.pos + left_d * ball.radius
                    ball.right_backward_point_pos = ball.pos + right_d * ball.radius

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


class Slug(Animal):
    def __init__(self, size_factor: float = 1.0, color: tuple = (79, 227, 134), debug: bool = False):
        self.animal_name = "slug"
        self.size_factor = size_factor
        self.color = color
        self.debug = debug
        self._body = self._create_animal(self.animal_name, self.size_factor)

