import pygame
import math
from PIL import Image 
import time

pygame.init()
pygame.display.set_caption("RACING CAR")

info = pygame.display.Info()

w = info.current_w
h = info.current_h

WIDTH, HEIGHT = w, h - 60
FPS = 60


window = pygame.display.set_mode((WIDTH, HEIGHT))

class PlayerCar():
	def __init__(self):
		super().__init__()
		self.original_image = pygame.image.load("car1.png").convert_alpha()  # Charger l'image de la voiture
		self.original_image = pygame.transform.scale(self.original_image, (26, 43))  # Redimensionner l'image
		self.image = self.original_image

		self.rect = self.image.get_rect(center=((WIDTH*37/40 , HEIGHT*4/10)))
		self.angle = 0
		self.speed = 0
		self.acceleration = 0.075
		self.deceleration = 0.05
		self.brake = 0.15
		self.max_speed = 15

		self.death = 0
		self.myfont = pygame.font.SysFont("monospace", 30)
		self.death_display = self.myfont.render(str(self.death), 3, (255,255,0))
		self.morts_display = self.myfont.render('Morts : ', 3, (255,255,0))

		self.chrono = Chronometre()
		self.time = self.chrono.time()
		self.time_display = self.myfont.render("{:.2f} secondes".format(self.time), True, (255,255,0))

		self.reset_display = self.myfont.render('Appuyez sur r pour reset', 3, (255,255,0))


	def limit_speed(self):
		if self.speed > self.max_speed:
			self.speed = self.max_speed
		if self.speed < -self.max_speed:
			self.speed = -self.max_speed

	def update(self, color):
		print(color)
		self.time = self.chrono.time()
		self.move(color)
		self.limit_speed()
		self.rotate_image()
		

	def move(self, color):
		# Calcul de la vitesse en fonction de l'angle de rotation
		speed_x = self.speed * math.sin(math.radians(self.angle))
		speed_y = -self.speed * math.cos(math.radians(self.angle))

		# Mise à jour de la position
		new_x = self.rect.x + speed_x
		new_y = self.rect.y + speed_y

		# Vérification des collisions avec les bords de l'écran
		if 0 <= new_x <= WIDTH - self.rect.width and 0 <= new_y <= HEIGHT - self.rect.height:
			self.rect.x = new_x
			self.rect.y = new_y
		else:
			self.speed = 0

		# Changements en fonction des couleurs sous la voiture
		
		if color == (0, 0, 0, 255):
			if self.chrono.deja_demarre is False:
				self.chrono.start()
			self.time_display = self.myfont.render("{:.2f} secondes".format(self.time), True, (255,255,0))

		if color == (0, 255, 0, 255):
			self.speed=0
			self.chrono.stop()

		
		if color == (255, 255, 255, 255):
			self.rect = self.image.get_rect(center=(WIDTH*37/40 , HEIGHT*4/10))
			self.angle = 0
			self.speed = 0
			self.death += 1
			self.death_display = self.myfont.render(str(self.death), 1, (255,255,0))
			self.chrono.reset()
			self.time = 0
			self.time_display = self.myfont.render("{:.2f} secondes".format(self.time), True, (255,255,0))

			


	def rotate_image(self):
		rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
		self.image = rotated_image
		self.rect = rotated_image.get_rect(center=self.rect.center)



	def reset(self):
		self.rect = self.image.get_rect(center=(WIDTH*37/40 , HEIGHT*4/10))
		self.angle = 0
		self.speed = 0
		self.chrono.reset()
		self.time = 0
		self.time_display = self.myfont.render("{:.2f} secondes".format(self.time), True, (255,255,0))
		self.death = 0
		self.death_display = self.myfont.render(str(self.death), 1, (255,255,0))



	def display(self):
		window.blit(self.image, (self.rect.x, self.rect.y))
		window.blit(self.death_display, ((WIDTH/1470)*300, (HEIGHT/896)*651))
		window.blit(self.morts_display, ((WIDTH/1470)*170, (HEIGHT/896)*650))
		window.blit(self.time_display, ((WIDTH/1470)*130, (HEIGHT/896)*725))	
		window.blit(self.reset_display, ((WIDTH/1470)*60,(HEIGHT/896)*800))	





class Chronometre:
    def __init__(self):
        self.temps_debut = None
        self.temps_fin = None
        self.deja_demarre = False



    def start(self):
        self.temps_debut = time.time()
        self.deja_demarre = True



    def stop(self):
        self.temps_fin = time.time()



    def reset(self):
        self.temps_debut = None
        self.temps_fin = None
        self.deja_demarre = False



    def time(self):
        if self.temps_debut is None:
            return 0  # Retourne 0 si le chronomètre n'a pas encore démarré
        if self.temps_fin is None:
            return time.time() - self.temps_debut
        return self.temps_fin - self.temps_debut
		




class Game:
	def __init__(self, window, autoPlay = True):
		self.window = window
		self.clock = pygame.time.Clock()
		self.run = True
		self.BG = pygame.image.load("BGF.png").convert_alpha()
		self.BG = pygame.transform.scale(self.BG, (WIDTH, HEIGHT))  # Redimensionner l'image
		self.baseBG = Image.open("BGF.png") 
		self.baseBG = self.baseBG.resize((WIDTH, HEIGHT))

		self.car = PlayerCar()

		self.chrono = Chronometre()


		if autoPlay:
			self.play()



	def play(self):
		while self.run:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run = False
					break

			self.applyKeyPressed()

			self.car.update(self.baseBG.getpixel((self.car.rect.x, self.car.rect.y)))

			self.display()

		self.quit()



	def applyKeyPressed(self):
			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP]:
				self.car.speed += self.car.acceleration

			elif keys[pygame.K_DOWN]:
				self.car.speed -= self.car.brake
				
			else:
				if self.car.speed > 0:
					self.car.speed -= self.car.deceleration
				elif self.car.speed < 0:
					self.car.speed += self.car.deceleration

			if keys[pygame.K_LEFT]:
				self.car.angle -= 3

			elif keys[pygame.K_RIGHT]:
				self.car.angle += 3

			if keys[pygame.K_r]:
				self.car.reset()

			if keys[pygame.K_a]:
				self.car.original_image = pygame.image.load("car1.png").convert_alpha()  # Charger l'image de la voiture
				self.car.original_image = pygame.transform.scale(self.car.original_image, (26, 43))  # Redimensionner l'image
				self.car.image = self.car.original_image

			if keys[pygame.K_z]:
				self.car.original_image = pygame.image.load("car2.png").convert_alpha()  
				self.car.original_image = pygame.transform.scale(self.car.original_image, (26, 43))  
				self.car.image = self.car.original_image

			if keys[pygame.K_q]:
				self.car.original_image = pygame.image.load("car3.png").convert_alpha() 
				self.car.original_image = pygame.transform.scale(self.car.original_image, (26, 43))  
				self.car.image = self.car.original_image

			if keys[pygame.K_s]:
				self.car.original_image = pygame.image.load("car4.png").convert_alpha()  
				self.car.original_image = pygame.transform.scale(self.car.original_image, (26, 43))  
				self.car.image = self.car.original_image



	def display(self):
		window.blit(self.BG, (0,0))
		self.car.display()
		pygame.display.update()



	def quit(self):
		pygame.quit()
		quit()



def main(window):
	myGame = Game(window)

if __name__ == "__main__":
	main(window)