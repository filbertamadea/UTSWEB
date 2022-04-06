from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField

# ANGGOTA #
#Registration
class Registration(FlaskForm):
    nim = StringField('NIM: ')
    nama = StringField('Nama Anggota: ')
    jurusan = StringField('Jurusan: ')
    username = StringField('Username: ')
    password = PasswordField('Password: ')
    submit = SubmitField('Register')

#Login
class Login(FlaskForm):
    username = StringField('Username: ')
    password = PasswordField('Password: ')
    submit = SubmitField('Login')