import streamlit as st

import datetime
from requests import get

from multiapp import MultiApp
from apps import home, SignToText, SpeechToText, SignToSpeech  # importation des modules de apps


# Sécurité pour le mot de passe
#passlib,hashlib,bcrypt,scrypt
import hashlib

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# Bases de Données
import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, userlastname TEXT, userpseudo TEXT,'
			  'usernum INT, password TEXT)')

def add_userdata(username,userlastname, userpseudo, usernum,password):
	c.execute('INSERT INTO userstable(username, userlastname, userpseudo,'
			  'usernum, password) VALUES (?,?,?,?,?)',(username, userlastname, userpseudo,
			  usernum, password))
	conn.commit()

def login_user(username, userpseudo,password):
	c.execute('SELECT * FROM userstable WHERE (username =? OR userpseudo =?) AND password = ?',(username, userpseudo,password))
	data = c.fetchall()
	return data

def verify_user(userpseudo):
	c.execute('SELECT userpseudo FROM userstable WHERE (userpseudo =?)',( userpseudo,))
	data = c.fetchall()
	return data

app = MultiApp()



# Programme principal

def main():
	st.markdown("""
	# real Hear
	### L'application real Hear (rHr) est une révolution dans la communication entre les malentendants et les entendants. 
	""")
# Le menu de connexion et d'inscription
	st.sidebar.image("Logo_rHr_petit-removebg-preview.png")
	sign_log = st.sidebar.selectbox('Connexion / Inscription', ["Connexion", "Inscription"])


	if sign_log == "Inscription":
		st.subheader("Créer un nouveau compte")
		# Entrez des données
		new_user_name = st.sidebar.text_input("Nom").strip()
		new_user_last_name = st.sidebar.text_input("Prénom").strip()
		new_user_pseudo = st.sidebar.text_input("Pseudo utilisateur").strip()
		new_user_num = st.sidebar.number_input(label="Numéro de téléphone", value=2250700000000)
		new_password = st.sidebar.text_input("Mot de passe", type='password')
		new_password_conf = st.sidebar.text_input("Confirmation de mot de passe", type='password')

		# Vérification
		if new_user_name == "" or  new_user_last_name == "" or new_user_pseudo == "" or len(new_password) == 0:
			st.sidebar.info("Remplissez tous les champs s'il vous plaît")
		elif len(new_password) < 4:
			st.sidebar.warning("Votre mot de passe est trop court!!!")
		elif new_password == new_password_conf:
			if st.sidebar.button("S'inscrire"):
				create_usertable()
				verification = verify_user( new_user_pseudo)
				if verification:
					st.info("Le pseudo existe déjà")
				else:
					# Création du compte
					create_usertable()
					add_userdata(new_user_name, new_user_last_name, new_user_pseudo, new_user_num, make_hashes(new_password))
					st.success("Votre compte a été créé avec succès")
					st.sidebar.info("Connectez-vous dans la section 'Connexion'")


		else:
			# Message d'erreur
			st.sidebar.warning("Les mots de passes ne sont pas identiques")

	else:
		# Connexion
		st.subheader("Connectez-vous...")
		username = st.sidebar.text_input("Nom ou Pseudo")
		password = st.sidebar.text_input("Mot de passe", type='password')


		if st.sidebar.checkbox("Connexion"):

			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username, username, check_hashes(password, hashed_pswd))
			if result:
				# Les différentes pages de notre application
				st.success("Connecté en tant que {}".format(username))
				app.add_app("Accueil", home.app)
				app.add_app("Sign To Text", SignToText.app)
				app.add_app("Speech To Text", SpeechToText.app)
				app.add_app("Sign To Speech", SignToSpeech.app)

				# The main app
				app.run()

			else:
				st.warning("Nom /Pseudo ou mot de passe incorrect")



if __name__ == '__main__':
	main()