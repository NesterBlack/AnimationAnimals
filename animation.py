import pygame
import math
from shapely.geometry import Polygon

class BodyBall:
    def __init__(self, surface, radius):
        self.surface = surface
        self.pos = pygame.Vector2(0, 0)
        self.angle = 0

        self.left_point_pos = pygame.Vector2()
        self.right_point_pos = pygame.Vector2()

        self.forward_point_pos = None
        self.left_forward_point_pos = None
        self.right_forward_point_pos = None

        self.backward_point_pos = None
        self.left_backward_point_pos = None
        self.right_backward_point_pos = None

        self.radius = radius

    def draw(self):
        pygame.draw.circle(self.surface, (100, 100, 100), (self.pos[0], self.pos[1]), self.radius, 5)
        pygame.draw.circle(self.surface, (0, 100, 0), self.left_point_pos, 5)
        pygame.draw.circle(self.surface, (100, 0, 0), self.right_point_pos, 5)
        if self.forward_point_pos:
            pygame.draw.circle(self.surface, (0, 0, 100), self.forward_point_pos, 5)
            pygame.draw.circle(self.surface, (100, 0, 100), self.left_forward_point_pos, 5)
            pygame.draw.circle(self.surface, (0, 100, 100), self.right_forward_point_pos, 5)
        if self.backward_point_pos:
            pygame.draw.circle(self.surface, (0, 0, 100), self.backward_point_pos, 5)
            pygame.draw.circle(self.surface, (100, 0, 100), self.left_backward_point_pos, 5)
            pygame.draw.circle(self.surface, (0, 100, 100), self.right_backward_point_pos, 5)



class Animal:
    def __init__(self, surface: pygame.Surface, animal_name: str="slug", size_factor: float=1.0, color: tuple=(79, 227, 134), debug: bool=False):
        self.surface = surface
        self.animal_name = animal_name
        self.size_factor = size_factor
        self.color = color
        self.debug = debug
        self.body = self._create_animal(self.animal_name, self.size_factor)

    # TODO: extract form class
    def _create_animal(self, animal="slug", size_factor=1) -> [BodyBall]:
        balls = []
        if animal.lower() == "slug":
            size = [x * size_factor for x in [34, 42, 43, 42, 41, 38, 32, 30, 25, 19, 17, 16, 9, 7]]
        elif animal.lower() == "robocode":
            size = [x * size_factor for x in [40, 40, 40, 45, 50, 50, 45, 40, 40, 40]]
        for i in range(len(size)):
            balls.append(BodyBall(self.surface, size[i]))
            balls[-1].pos.x = i*max(size)
        return balls


    def move_animal(self, go_to, speed):
        direction = self.body[0].pos - pygame.Vector2(go_to)
        self.body[0].angle = math.degrees(math.atan2(direction.y, direction.x))
        distance = direction.length()
        if distance != 0:
            direction = direction.normalize()
            self.body[0].pos = self.body[0].pos - direction * (distance // speed)

            right_d = direction.rotate(90)
            left_d = direction.rotate(-90)
            self.body[0].left_point_pos = self.body[0].pos + left_d * self.body[0].radius
            self.body[0].right_point_pos = self.body[0].pos + right_d * self.body[0].radius
            self.body[0].forward_point_pos = self.body[0].pos - direction * self.body[0].radius

            left_forward_d = direction.rotate(135)
            right_forward_d = direction.rotate(-135)
            self.body[0].left_forward_point_pos = self.body[0].pos + left_forward_d * self.body[0].radius
            self.body[0].right_forward_point_pos = self.body[0].pos + right_forward_d * self.body[0].radius
        for index, ball in enumerate(self.body[1:]):
            prev = pygame.Vector2(self.body[index].pos)
            curr = pygame.Vector2(ball.pos)
            direction = prev - curr
            distance = direction.length()
            if distance != 0:
                direction = direction.normalize()
                ball.angle = math.degrees(math.atan2(direction.y, direction.x))
                ball.pos = prev - direction * ball.radius
                ball.left_point_pos = ball.pos + pygame.Vector2(-direction.y, direction.x) * ball.radius
                ball.right_point_pos = ball.pos + pygame.Vector2(direction.y, -direction.x) * ball.radius

                if index == len(self.body) - 2:
                    left_d = direction.rotate(-135)
                    right_d = direction.rotate(135)

                    ball.backward_point_pos = ball.pos - direction * ball.radius
                    ball.left_backward_point_pos = ball.pos + left_d * ball.radius
                    ball.right_backward_point_pos = ball.pos + right_d * ball.radius

                if index >= 2:
                    Blast_ball_pos = self.body[index].pos
                    Alast_last_ball_pos = self.body[index-1].pos
                    Cball_pos = ball.pos

                    BA = Alast_last_ball_pos - Blast_ball_pos
                    BC = Cball_pos - Blast_ball_pos

                    angle = BA.angle_to(BC)

                    max_angle = 160
                    if abs(angle) < max_angle:
                        angle_difference = max_angle - angle
                        if angle < 0:
                            angle_difference = -max_angle - angle
                        BC = BC.rotate(angle_difference)
                        ball.pos = self.body[index].pos + BC

    def draw_animal(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.body[0].pos, self.body[0].radius)
        points = [self.body[0].forward_point_pos, self.body[0].left_forward_point_pos]
        for ball in self.body:
            points.append(ball.left_point_pos)
        points.append(self.body[-1].right_backward_point_pos)
        points.append(self.body[-1].backward_point_pos)
        points.append(self.body[-1].left_backward_point_pos)
        for ball in self.body[::-1]:
            points.append(ball.right_point_pos)
        points.append(self.body[0].right_forward_point_pos)
        poly = Polygon(points)
        fixed = poly.buffer(0)
        try:
            points = list(fixed.exterior.coords)
        except AttributeError or TypeError:
            pass
        animal_rect = pygame.draw.polygon(surface, self.color, points, 0)

        # eyes
        pygame.draw.circle(surface, (255, 255, 255), self.body[0].left_forward_point_pos, 10*self.size_factor)
        pygame.draw.circle(surface, (255, 255, 255), self.body[0].right_forward_point_pos, 10*self.size_factor)
        pygame.draw.circle(surface, (0, 0, 0), self.body[0].left_forward_point_pos, 4*self.size_factor)
        pygame.draw.circle(surface, (0, 0, 0), self.body[0].right_forward_point_pos, 4*self.size_factor)

        if self.animal_name == "robocode":
            direction = (pygame.Vector2(self.body[-1].left_backward_point_pos) - self.body[-1].pos)*self.size_factor
            posX = direction.x + self.body[-1].left_backward_point_pos[0]
            posY = direction.y + self.body[-1].left_backward_point_pos[1]
            pygame.draw.line(surface, self.color, self.body[-1].pos, (posX, posY), 10)

            direction = (pygame.Vector2(self.body[-1].right_backward_point_pos)-self.body[-1].pos)*self.size_factor*1.5
            posX = direction.x + self.body[-1].right_backward_point_pos[0]
            posY = direction.y + self.body[-1].right_backward_point_pos[1]
            pygame.draw.line(surface, self.color, self.body[-1].pos, (posX, posY), 10)


            direction = (self.body[0].left_point_pos - self.body[0].pos)*self.size_factor*1.5
            direction = direction.rotate(45)
            posX = direction.x + self.body[0].left_point_pos[0]
            posY = direction.y + self.body[0].left_point_pos[1]
            pygame.draw.line(surface, self.color, self.body[0].pos, (posX, posY), 10)

            direction = (self.body[0].right_point_pos - self.body[0].pos)*self.size_factor*1.5
            direction = direction.rotate(-45)
            posX = direction.x + self.body[0].right_point_pos[0]
            posY = direction.y + self.body[0].right_point_pos[1]
            pygame.draw.line(surface, self.color, self.body[0].pos, (posX, posY), 10)

            font = pygame.font.SysFont("Arial", int(40*self.size_factor))
            text = "ROBOCODE"[::-1]
            for index, ball in enumerate(self.body[1:-1]):
                word = font.render(text[index], True, (0,0,0))
                rotated_word = pygame.transform.rotate(word, -ball.angle)
                rotated_rect = rotated_word.get_rect(center=(ball.pos.x, ball.pos.y))
                self.surface.blit(rotated_word, rotated_rect)



        # size rect
        if True:
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.center, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.bottomleft, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.bottomright, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.topleft, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.topright, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.midbottom, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.midleft, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.midright, 5)
            pygame.draw.circle(self.surface, (255, 0, 0), animal_rect.midtop, 5)

            for ball in self.body:
                ball.draw()
            pygame.draw.rect(self.surface, (100, 255, 100), self.rect(), 5)



    def rect(self):
        x = self.body[0].pos.x-self.body[0].radius
        y = self.body[0].pos.y-self.body[0].radius
        rect = pygame.Rect(x, y, self.body[0].radius*2, self.body[0].radius*2)
        return rect




