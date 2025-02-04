import math
import pygame
import pymunk
import pymunk.pygame_util
def create_hollow_pentagon(space,center,size,angular_velocity):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position=center
    body.angular_velocity=angular_velocity
    angle_step=2*math.pi/5
    vertices=[(math.cos(i*angle_step)*size,math.sin(i*angle_step)*size) for i in range(5)]
    space.add(body)
    segments=[]
    for i in range(5):
        segment=pymunk.Segment(body, vertices[i], vertices[(i + 1) % 5], 5)
        segment.elasticity=1.0
        segment.friction=0.5
        space.add(segment)
        segments.append(segment)
    return body,vertices,segments
def update_pentagon_rotation(body,vertices,segments,dt):
    body.angle+=body.angular_velocity*dt
    angle_step=2*math.pi/5
    rotated_vertices=[]
    for x,y in vertices:
        new_x=math.cos(body.angle)*x-math.sin(body.angle)*y
        new_y=math.sin(body.angle)*x+math.cos(body.angle)*y
        rotated_vertices.append((new_x,new_y))
    for i in range(5):
        new_segment=pymunk.Segment(body,rotated_vertices[i],rotated_vertices[(i + 1) % 5],5)
        new_segment.elasticity=1.0
        new_segment.friction=0.5
        segments[i]=new_segment  
def create_ball(space,pos,radius=10):
    mass=1
    moment=pymunk.moment_for_circle(mass,0,radius)
    body=pymunk.Body(mass,moment)
    body.position=pos
    shape=pymunk.Circle(body,radius)
    shape.elasticity=0.8
    shape.friction=0.3
    space.add(body,shape)
    return body
def main():
    pygame.init()
    screen=pygame.display.set_mode((600,600))
    clock=pygame.time.Clock()
    space=pymunk.Space()
    space.gravity=(0,500)
    draw_options=pymunk.pygame_util.DrawOptions(screen)
    pentagon,vertices,segments=create_hollow_pentagon(space,(300, 300),100,angular_velocity=1.0)
    ball=create_ball(space, (300, 250))
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
        update_pentagon_rotation(pentagon,vertices,segments,1/60.0)
        space.step(1/60.0)
        screen.fill((0,0,0))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__=="__main__":
    main()
