# Planet Sizes arent in scale. Cannot find a intuitive 
# way to do so. Newtonian Gravitational force with taking
# the sun and the 8 planets only
# ======================================================
"""Planets Simulations using Pygame."""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame #2d game module
import math #math functions
import warnings
warnings.filterwarnings('ignore')

pygame.init()
WIDTH, HEIGHT = 1540, 865 #game window size in pixels
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Displaying on specified window size
pygame.display.set_caption("Planet Simulation") #Window Title

#Color Section
GREY = (128,128,128) #mercury
YELLOWISH = (165,124,27) #venus
BLUE = (0,0,225) #for earth
RED = (198, 123, 92) #mars
BROWN = (144, 97, 77) #jupiter
CARMEL = (195, 161, 113) #saturn
URANUS_BLUE = (79, 208, 231) #uranus
NEPTUNE = (62, 84, 232) #neptune
WHITE = (255, 255, 255) #for text
YELLOW = (255, 255, 0) #for sun
DARK_GREY = (80,78,81) #orbit

#Text Properties
FONT = pygame.font.SysFont("arial", 16)

class Planet:
    AU = 149.6e6 * 1000 #AU = Astronomical unit, *1000 to convert into meters
    G = 6.67428e-11 
    SCALE = 25 / AU #1AU = 100 Px
    TIMESTEP = 3600*24 #To see the planet with the time frame of 1 day
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        #To draw things at the center of the screen
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win,self.color,(x,y), self.radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_width()/2))
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = self.G * self.mass * other.mass / distance ** 2 #force of Attraction
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0 #total forces exerted on the planet from planet which are not in self
        for planet in planets: 
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        #calculate velocity
        
        self.x_vel += total_fx / self.mass * self.TIMESTEP 
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
    
    
def main(): #Main Function
    run = True #to start the loop to keep it running
    clock = pygame.time.Clock() #to keep running the simulation on specified time
        
    sun = Planet(0,0,20, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    
    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.30 * 10**24)
    mercury.y_vel = 47.4 * 1000 #Kilometer * 1000 = meter
    
    venus = Planet(0.723 * Planet.AU, 0, 14, YELLOWISH, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000 #Kilometer * 1000 = meter
    
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783 * 1000 #Kilometer * 1000 = meter
    
    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000 #Kilometer * 1000 = meter
    
    jupiter = Planet(5.203 * Planet.AU, 0, 16, BROWN, 1898.13 * 10**24)
    jupiter.y_vel = 13.06 * 1000 #Kilometer * 1000 = meter
    
    saturn = Planet(9.537 * Planet.AU, 0, 16, CARMEL, 568.32 * 10**24)
    saturn.y_vel = 9.68 * 1000 #Kilometer * 1000 = meter
    
    uranus = Planet(19.191 * Planet.AU, 0, 16, URANUS_BLUE, 86.811 * 10**24)
    uranus.y_vel = 6.80 * 1000 #Kilometer * 1000 = meter
    
    neptune = Planet(30.068 * Planet.AU, 0, 16, NEPTUNE, 102.409 * 10**24)
    neptune.y_vel = 5.43 * 1000 #Kilometer * 1000 = meter

    pluto = Planet(39.481 * Planet.AU, 0, 16, BROWN, 0.01303 * 10**24)
    pluto.y_vel = 4.67 * 1000 #Kilometer * 1000 = meter
    
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    
    # Powerful pc might boost the speed and slow pc may delay the speed
    # We need to keep the speed at one constant measure

    while run: 
        clock.tick(60) #Changes will occur at 60 tick rate
        WIN.fill((0,0,0)) #Window Bg
                
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #To quit on clicking the X
                run = False
                
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
            
        pygame.display.update() #To update the display with newly added codes
            
    pygame.quit()

main()