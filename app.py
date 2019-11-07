from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from dbdata import dbconf, queries
from mysql.connector import Error
from mysql.connector import errorcode
from base64 import b64encode, b64decode
import os
import re

app = Flask(__name__)

# Llave secreta
app.secret_key = os.urandom(24)

# Coneccion a la base de datos
conexion = mysql.connector.connect(**dbconf)



# carga las vistas
from views import *
