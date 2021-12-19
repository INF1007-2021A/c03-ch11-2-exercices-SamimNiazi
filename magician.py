"""
Chapitre 11.3

Classes pour représenter un magicien et ses pouvoirs magiques.
"""


import random

import utils
from character import *


# TODO: Créer la classe Spell qui a les même propriétés que Weapon, mais avec un coût en MP pour l'utiliser
class Spell(Weapon):
	"""
	Un sort dans le jeu.

	:param name: Le nom du sort
	:param power: Le niveau d'attaque
	:param mp_cost: Le coût en MP d'utilisation du sort
	:param min_level: Le niveau minimal pour l'utiliser
	"""
	def __init__(self, name, power, mp_cost, min_level):
		super().__init__(name, power, min_level)
		self.mp_cost = mp_cost
	pass

# TODO: Déclarer la classe Magician qui étend la classe Character
class Magician(Character):
	"""
	Un utilisateur de magie dans le jeu. Un magicien peut utiliser des sorts, mais peut aussi utiliser des armes physiques. Sa capacité à utiliser des sorts dépend 

	:param name: Le nom du personnage
	:param max_hp: HP maximum
	:param max_mp: MP maximum
	:param attack: Le niveau d'attaque physique du personnage
	:param magic_attack: Le niveau d'attaque magique du personnage
	:param defense: Le niveau de défense du personnage
	:param level: Le niveau d'expérience du personnage

	:ivar using_magic: Détermine si le magicien tente d'utiliser sa magie dans un combat.
	"""

	def __init__(self, name, max_hp, max_mp, attack, magic_attack, defense, level):

		super().__init__(name, max_hp, attack, defense, level)
		self.max_mp = max_mp
		self.magic_attack = magic_attack
		self.using_magic = None
		self.mp = max_mp
		self.spell = False #pas mettre None mettre False.

	@property
	def mp(self):
		return self.__mp

	@mp.setter
	def mp(self, val):
		utils.clamp(val ,0 , self.max_mp)  #faut restreindre les valeurs

	@property
	def spell(self):
		return self.__spell

	@spell.setter
	def spell(self, value):
		if value.min_level > self.level and value is not None:
			raise ValueError()
		self.spell = value

	# TODO: Surcharger la méthode `compute_damage` 
	def compute_damage(self, other):
		# Si le magicien va utiliser sa magie (`will_use_spell()`):
			# Soustraire à son MP le coût du sort
			# Retourner le résultat du calcul de dégâts magiques
		if self.will_use_spell() is True:
			self._compute_magical_damage(other)
			self.mp -= self.spell.mp_cost	
		else:
			return self._compute_physical_damage(other)
		

	def will_use_spell(self):
		if self.spell and self.using_magic is not None and self.mp > self.spell.mp_cost :
			return True

	def _compute_magical_damage(self, other):
		rand = random.uniform(0.85,0.1)
		if random.randint(0,100) < 6.25:
			crit = 2
		else:
			crit = 1
		modifier = rand * crit
		damage = ((((((2/5)*(self.level + self.magic_attack))+2)*self.spell.power)/50)+2)*modifier
		return damage, crit

	def _compute_physical_damage(self, other):
		# TODO: Calculer le dommage physique exactement de la même façon que dans `Character`
		parametrelevel = ((2/5)*self.level) + 2
		attackanddefense = self.attack/other.defense
		rand = random.uniform(0.85,0.1)
		if random.randint(0,100) < 6.25:
			crit = 2
		else:
			crit = 1
		modifier = rand * crit
		damage = round((((parametrelevel * self.weapon.power * attackanddefense) /50 ) + 2) * modifier)
		return damage, crit

