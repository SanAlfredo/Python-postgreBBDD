import sys
from ventana1 import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import psycopg2
from psycopg2 import sql
conn=""
cursor=""
counter=0
contra=""
class Iniciar_programa(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_barra1.setVisible(False)
        self.ui.txt_pass.setFocus()
        self.ui.pb_iniciar.clicked.connect(self.Conectarse)
        self.ui.txt_pass.returnPressed.connect(self.Verifica)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Progreso)
    #region Reescribiendo el evento close
    def closeEvent(self, event):
        global conn
        global cursor
        cerrar = QMessageBox.question(self, "Cerrar programa", "¿Está seguro de cerrar el programa?", QMessageBox.Yes
                                      | QMessageBox.No, QMessageBox.Yes)
        if cerrar==QMessageBox.Yes:
            if conn!="":
                cursor.close()
                conn.close()
                event.accept()
            else:
                event.accept()
        else:
            event.ignore()
    #endregion
    #region Verifica quien tiene foco
    def Verifica(self):
        if self.ui.txt_pass.hasFocus():
            self.ui.pb_iniciar.setFocus()
        if self.ui.pb_iniciar.hasFocus():
            self.Conectarse()
    #endregion
    #region Crear la conexión a la base de datos
    def Conectarse(self):
        global conn
        global cursor
        global contra
        contra=self.ui.txt_pass.text()
        if not contra:
            QMessageBox.critical(self,"Mensaje de error","Debe escribir una contraseña")
            self.ui.txt_pass.setFocus()
        else:
            #region conectando a la base de datos
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    database="postgres",
                    user="postgres",
                    password=contra
                )
                conn.autocommit=True
                cursor=conn.cursor()
                self.timer.start(5)
                resp=1
            except:
                resp=0
            #endregion
            if resp==0:
                QMessageBox.critical(self,"Mensaje de error","No se ha podido establecer la conexión\n"
                                                         "con la base de datos o la contraseña es incorrecta")
                self.ui.txt_pass.setFocus()

            else:
                self.ui.lbl_progreso.setText("Conectado a la base de datos")
                self.ui.txt_pass.clear()
                #region Creacion de la base de datos
                try:
                    self.ui.lbl_progreso.setText("Creando Base de datos")
                    self.timer.start(5)
                    query ='''CREATE database "CLINICA"''';
                    cursor.execute(query)
                    resp1=1
                except:
                    resp1=0
                #endregion
                if resp1==1:
                    self.ui.lbl_progreso.setText("Base de datos creada")
                    #region Creacion del superusuario
                    try:
                        self.ui.lbl_progreso.setText("Creando usuarios básicos")
                        self.timer.start(5)
                        user="administrador"
                        password="rVenE24zP6"
                        query = sql.SQL("CREATE USER {username} WITH LOGIN PASSWORD {password}").format(
                            username=sql.Identifier(user),
                            password=sql.Placeholder()
                        )
                        cursor.execute(query, (password,))
                        query=sql.SQL("ALTER USER {username} WITH SUPERUSER CREATEROLE").format(
                            username=sql.Identifier(user)
                        )
                        cursor.execute(query)
                        resp2 = 1
                    except:
                        resp2 = 0
                    #endregion
                    if resp2==1:
                        self.ui.lbl_progreso.setText("Creado admin con exito")
                        #region Cerrar conexion en postgre
                        if conn!="":
                            cursor.close()
                            conn.close()
                        #endregion
                        #region iniciar nueva conexion con CLinica
                        try:
                            conn = psycopg2.connect(
                                host="localhost",
                                database="CLINICA",
                                user="postgres",
                                password=contra
                            )
                            conn.autocommit = True
                            cursor = conn.cursor()
                            resp3=1
                        except:
                            resp3=0
                        #endregion
                        if resp3==1:
                            self.ui.lbl_progreso.setText("Conectado a la base de datos")
                            #region Creando las nuevas tablas en la base de datos
                            try:
                                self.ui.lbl_progreso.setText("Creando tablas en la base de datos")
                                self.timer.start(5)
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS GRUPO_SANGUINEO(
                                        ID_GRUPO SERIAL NOT NULL,
                                        GRUPO VARCHAR NOT NULL,
                                        PRIMARY KEY (ID_GRUPO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS DATO_GENERAL(
                                        ID_DATO serial NOT NULL,
                                        PESO DECIMAL(10,3),
                                        TALLA DECIMAL(10,2),
                                        PRIMARY KEY (ID_DATO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS FACTOR_SANGUINEO(
                                        ID_FACTOR SERIAL NOT NULL,
                                        FACTOR VARCHAR,
                                        PRIMARY KEY (ID_FACTOR));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS USUARIO(
                                        CUENTA_USER VARCHAR NOT NULL,
                                        PASS VARCHAR,
                                        SAL VARCHAR,
                                        TEMA INT,
                                        PRIMARY KEY (CUENTA_USER));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS VALIDACIONES(
                                        ID_VALIDACIONES SERIAL NOT NULL,
                                        CODIGO VARCHAR,
                                        VALIDACION BOOLEAN,
                                        HABILITACION BOOLEAN,
                                        PRIMARY KEY (ID_VALIDACIONES));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS EXTENSION(
                                        ID_EXTENSION SERIAL NOT NULL,
                                        TIPO VARCHAR,
                                        DESCRIPCION VARCHAR,
                                        PRIMARY KEY (ID_EXTENSION));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS DESCRIPCIONES(
                                        ID_DESCRIPCION SERIAL NOT NULL,
                                        DESCRIPCION VARCHAR,
                                        PRIMARY KEY (ID_DESCRIPCION));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS TIPO_DATO(
                                        ID_TIPO SERIAL NOT NULL,
                                        TIPO_DATO VARCHAR,
                                        PRIMARY KEY (ID_TIPO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS TIPO_SEXO(
                                        ID_TIPO SERIAL NOT NULL,
                                        TIPO_DATO VARCHAR,
                                        PRIMARY KEY (ID_TIPO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS TIPO_FAMILIAR(
                                        ID_TIPO SERIAL NOT NULL,
                                        TIPO_DATO VARCHAR,
                                        PRIMARY KEY (ID_TIPO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS FECHA(
                                        ID_FECHA SERIAL NOT NULL,
                                        FECHAYHORA timestamp,
                                        TIPO_FECHA INT,
                                        PRIMARY KEY (ID_FECHA),
                                        FOREIGN KEY (TIPO_FECHA) REFERENCES TIPO_DATO(ID_TIPO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS PERSONA(
                                        ID_PERSONA VARCHAR NOT NULL,
                                        NOMBRE VARCHAR,
                                        APELLIDO1 VARCHAR,
                                        APELLIDO2 VARCHAR,
                                        FECHA INT,
                                        TIPO_SEXO INT,
                                        PRIMARY KEY (ID_PERSONA),
                                        FOREIGN KEY (FECHA) REFERENCES FECHA(ID_FECHA),
                                        FOREIGN KEY (TIPO_SEXO) REFERENCES TIPO_SEXO(ID_TIPO));
                                        ''')
                                cursor.execute('''
                                                    CREATE TABLE IF NOT EXISTS CARNET(
                                                    ID_CARNET SERIAL NOT NULL,
                                                    NUMERO VARCHAR,
                                                    EXTENSION INT,
                                                    PERSONA VARCHAR UNIQUE,
                                                    PRIMARY KEY (ID_CARNET),
                                                    FOREIGN KEY (PERSONA) REFERENCES persona(id_persona),
                                                    FOREIGN KEY (EXTENSION) REFERENCES EXTENSION(ID_EXTENSION));
                                                    ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS MEDICO(
                                        MATRICULA VARCHAR NOT NULL,
                                        ID_PERSONA VARCHAR,
                                        USUARIO VARCHAR,
                                        CORREO VARCHAR,
                                        VALIDACIONES INT,
                                        PRIMARY KEY (MATRICULA),
                                        FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
                                        FOREIGN KEY (USUARIO) REFERENCES USUARIO(CUENTA_USER),
                                        FOREIGN KEY (VALIDACIONES) REFERENCES VALIDACIONES(ID_VALIDACIONES));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS PACIENTE(
                                        ID_PACIENTE VARCHAR NOT NULL,
                                        ID_PERSONA VARCHAR,
                                        GRUPO_SANGUINEO INT,
                                        FACTOR_SANGUINEO INT,
                                        PROCEDENCIA VARCHAR,
                                        RESIDENCIA VARCHAR,
                                        DIRECCION VARCHAR,
                                        BARRIO VARCHAR,
                                        DATO_GENERAL INT,
                                        PRIMARY KEY (ID_PACIENTE),
                                        FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
                                        FOREIGN KEY (GRUPO_SANGUINEO) REFERENCES GRUPO_SANGUINEO(ID_GRUPO),
                                        FOREIGN KEY (FACTOR_SANGUINEO) REFERENCES FACTOR_SANGUINEO(ID_FACTOR),
                                        FOREIGN KEY (DATO_GENERAL) REFERENCES DATO_GENERAL(ID_DATO));
                                        ''')
                                cursor.execute('''
                                                    CREATE TABLE IF NOT EXISTS ANTECEDENTES(
                                                    ID_ANTECEDENTES SERIAL NOT NULL,
                                                    PATOLOGICOS VARCHAR,
                                                    ALERGIAS VARCHAR,
                                                    PACIENTE VARCHAR unique,
                                                    PRIMARY KEY (ID_ANTECEDENTES),
                                                    FOREIGN KEY (PACIENTE) REFERENCES PACIENTE(id_paciente));
                                                    ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS FAMILIAR(
                                        ID_FAMILIAR VARCHAR NOT NULL,
                                        ID_PERSONA VARCHAR,
                                        TIPO_FAMILIAR INT,
                                        PACIENTE VARCHAR,
                                        PRIMARY KEY (ID_FAMILIAR),
                                        FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
                                        FOREIGN KEY (TIPO_FAMILIAR) REFERENCES TIPO_FAMILIAR(ID_TIPO),
                                        FOREIGN KEY (PACIENTE) REFERENCES PACIENTE(ID_PACIENTE));
                                        ''')
                                cursor.execute('''
                                                    CREATE TABLE IF NOT EXISTS TELEFONO(
                                                    ID_TELEFONO serial NOT NULL,
                                                    NUMERO INT,
                                                    FAMILIAR VARCHAR UNIQUE,
                                                    FOREIGN KEY (FAMILIAR) REFERENCES familiar(id_familiar),
                                                    PRIMARY KEY (ID_TELEFONO));
                                                    ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS CONSULTA(
                                        ID_CONSULTA VARCHAR NOT NULL,
                                        CODIGO_PACIENTE VARCHAR,
                                        ID_MEDICO VARCHAR,
                                        FECHA INT,
                                        FRECUENCIA_CARDIACA INT,
                                        FRECUENCIA_RESPIRATORIA INT,
                                        TEMPERATURA DECIMAL(10,2),
                                        SATURACION INT,
                                        PRESION VARCHAR,
                                        PERIMETRO_CEFALICO DECIMAL(10,2),
                                        MOTIVO VARCHAR,
                                        EXAMEN VARCHAR,
                                        DIAGNOSTICO VARCHAR,
                                        TRATAMIENTO VARCHAR,
                                        OBSERVACIONES VARCHAR,
                                        PROXIMA_REVISION DATE,
                                        DATO_GENERAL INT,
                                        PRIMARY KEY (ID_CONSULTA),
                                        FOREIGN KEY (CODIGO_PACIENTE) REFERENCES PACIENTE(ID_PACIENTE),
                                        FOREIGN KEY (ID_MEDICO) REFERENCES MEDICO(MATRICULA),
                                        FOREIGN KEY (FECHA) REFERENCES FECHA(ID_FECHA),
                                        FOREIGN KEY (DATO_GENERAL) REFERENCES DATO_GENERAL(ID_DATO));
                                        ''')
                                cursor.execute('''
                                        CREATE TABLE IF NOT EXISTS HISTORIAL(
                                        ID_HISTORIAL SERIAL NOT NULL,
                                        MEDICO VARCHAR,
                                        FECHA INT,
                                        ID_TABLA VARCHAR,
                                        DESCRIPCIONES INT,
                                        TABLA VARCHAR,
                                        PRIMARY KEY (ID_HISTORIAL),
                                        FOREIGN KEY (MEDICO) REFERENCES MEDICO(MATRICULA),
                                        FOREIGN KEY (FECHA) REFERENCES fecha(id_fecha),
                                        FOREIGN KEY (DESCRIPCIONES) REFERENCES descripciones(id_descripcion));
                                        ''')
                                resp4=1
                            except:
                                resp4=0
                            #endregion
                            if resp4==1:
                                self.ui.lbl_progreso.setText("Tablas creadas con éxito")
                                #region Insertar datos iniciales a las tablas
                                try:
                                    self.ui.lbl_progreso.setText("Llenando tablas importantes")
                                    self.timer.start(5)
                                    #llenando la tabla grupo sanguineo
                                    query='INSERT INTO grupo_sanguineo (id_grupo, grupo) VALUES (%s,%s)'
                                    valor ="A","B","AB","O","No sabe"
                                    a=1
                                    for i in valor:
                                        cursor.execute(query,(a,i,))
                                        a+=1
                                    #llenando la tabla factor sanguineo
                                    query = 'INSERT INTO factor_sanguineo (id_factor, factor) VALUES (%s,%s)'
                                    valor = "positivo", "negativo" , "no sabe"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i,))
                                        a += 1
                                    #llenando la tabla tipo familiar
                                    query = 'INSERT INTO tipo_familiar (id_tipo, tipo_dato) VALUES (%s,%s)'
                                    valor = "padre","madre"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i,))
                                        a += 1
                                    #llenar la tabla tipo sexo
                                    query = 'INSERT INTO tipo_sexo (id_tipo, tipo_dato) VALUES (%s,%s)'
                                    valor = "masculino","femenino"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i,))
                                        a += 1
                                    #llenar tabla tipo dato
                                    query = 'INSERT INTO tipo_dato (id_tipo, tipo_dato) VALUES (%s,%s)'
                                    valor = "nacimiento","consulta","reconsulta","emergencia","log in","log out","registro","modifica","busca"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i,))
                                        a += 1
                                    #llenar tabla descripciones
                                    query = 'INSERT INTO descripciones (id_descripcion, descripcion) VALUES (%s,%s)'
                                    valor = "nuevo registro","cambios en la tabla","revisar historial paciente","entra al sistema","sale del sistema"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i,))
                                        a += 1
                                    #llenar la tabla extension
                                    query = 'INSERT INTO extension (id_extension,tipo, descripcion) VALUES (%s,%s,%s)'
                                    valor = ("CH","Chuquisaca"),("LP","La Paz"),("CB","Cochabamba"),("OR","Oruro"),\
                                            ("PT","Potosí"),("TJ","Tarija"),("SC","Santa Cruz"),("BE","Beni"),("PD","Pando"),\
                                            ("Otro","Otro país")
                                    #valor1="Chuquisaca","La Paz","Cochabamba","Oruro","Potosí","Tarija","Santa Cruz","Beni","Pando","Otro país"
                                    a = 1
                                    for i in valor:
                                        cursor.execute(query, (a, i[0],i[1],))
                                        a += 1
                                    #guardar al admin
                                    query = 'INSERT INTO usuario (cuenta_user,pass,sal,tema) VALUES (%s,%s,%s,%s)'
                                    valor = "administrador","gAAAAABh5ffijKywqmSYjgS9spH_XE2aem6nHw0fTX34TZ_-6yauV81brsPbvv4W4Lfo5gn1xQaCRgWGroAZOsGKJ-q6JemnGw==","6lMvivMhpNEkS2mexhDHNlgpSR5zyDMJPk0Vn7dZDWw=",0
                                    cursor.execute(query,valor)
                                    resp5=1
                                except:
                                    resp5=0
                                #endregion
                                if resp5==1:
                                    self.ui.lbl_progreso.setText("Tablas actualizadas con éxito")
                                    #region Creando las funciones para postgres
                                    try:
                                        self.ui.lbl_progreso.setText("Creando las funciones necesarias")
                                        self.timer.start(5)
                                        query='create function busq_ante_pac(character varying) returns ' \
                                              'TABLE(cod integer, patologicos character varying, alergias character varying) language plpgsql as $$ ' \
                                              'begin return query select a.id_antecedentes, a.patologicos, a.alergias from paciente' \
                                              ' inner join antecedentes a on paciente.id_paciente = a.paciente where id_paciente=$1; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_carnet_fam(character varying) returns TABLE(numero character varying, extension integer, cd_carnet integer)' \
                                              'language plpgsql as $$ begin return query select c.numero, c.extension, c.id_carnet from familiar' \
                                              ' inner join persona p on p.id_persona = familiar.id_persona inner join carnet c on p.id_persona = c.persona where id_familiar=$1;' \
                                              'end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_carnet_pac(character varying) returns TABLE(cod integer, numero character varying, extension integer)' \
                                              'language plpgsql as $$ begin return query select c.id_carnet, c.numero, c.extension from paciente' \
                                              ' inner join persona p on p.id_persona = paciente.id_persona inner join carnet c on p.id_persona = c.persona where id_paciente=$1; ' \
                                              'end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_consul_pac(character varying) ' \
                                              'returns TABLE(nombre_medico character varying, apellido1 character varying, apellido2 character varying, fecha_consulta timestamp without time zone, frec_cardiaca integer, frec_respirat integer, temp numeric, saturacion integer, presion character varying, per_cef numeric, peso numeric, talla numeric, motivo character varying, examen character varying, diagnostico character varying, tratamiento character varying, observacion character varying, prox date) ' \
                                              'language plpgsql as $$ begin return query select p.nombre, p.apellido1, p.apellido2, f.fechayhora, consulta.frecuencia_cardiaca, consulta.frecuencia_respiratoria, consulta.temperatura,' \
                                              ' consulta.saturacion, consulta.presion, consulta.perimetro_cefalico, dg.peso, dg.talla, consulta.motivo, consulta.examen, consulta.diagnostico,consulta.tratamiento,consulta.observaciones,' \
                                              ' consulta.proxima_revision from consulta inner join fecha f on f.id_fecha = consulta.fecha inner join dato_general dg on dg.id_dato = consulta.dato_general ' \
                                              'inner join medico m on m.matricula = consulta.id_medico inner join persona p on p.id_persona = m.id_persona where id_consulta=$1; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_datos_pac(character varying) returns TABLE(nombre character varying, apellido1 character varying, apellido2 character varying, fecha_nac timestamp without time zone, sexo integer, grupo integer, factor integer, procedencia character varying, residencia character varying, direccion character varying, barrio character varying, peso numeric, talla numeric, cod_pac character varying, cod_per character varying, cod_dat integer, cod_fecha integer)' \
                                              'language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,f.fechayhora,p.tipo_sexo,grupo_sanguineo,factor_sanguineo,paciente.procedencia,paciente.residencia,paciente.direccion,paciente.barrio,dg.peso,dg.talla,paciente.id_paciente,p.id_persona,dg.id_dato,p.fecha' \
                                              ' from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha = p.fecha inner join dato_general dg on dg.id_dato = paciente.dato_general where id_paciente=$1; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_fam_pac(character varying) returns TABLE(familiar character varying, nombre character varying, apellido1 character varying, apellido2 character varying, tipo integer, cod_per character varying)' \
                                              'language plpgsql as $$ begin return query select f.id_familiar,p.nombre,p.apellido1,p.apellido2,f.tipo_familiar,p.id_persona from paciente' \
                                              ' inner join familiar f on paciente.id_paciente = f.paciente inner join persona p on p.id_persona = f.id_persona where id_paciente=$1; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_hist1() ' \
                                              'returns TABLE(fecha timestamp without time zone, nom character varying, apellido1 character varying, apellido2 character varying, id_tabla character varying, tabla character varying, descripcion character varying, matricula character varying)' \
                                              'language plpgsql as $$ begin return query select  f.fechayhora,p.nombre,p.apellido1,p.apellido2,historial.id_tabla,historial.tabla,d.descripcion,m.matricula' \
                                              ' from historial inner join fecha f on f.id_fecha = historial.fecha inner join medico m on m.matricula = historial.medico ' \
                                              'inner join descripciones d on d.id_descripcion = historial.descripciones inner join persona p on p.id_persona = m.id_persona; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_hist1_1(character varying) ' \
                                              'returns TABLE(fecha timestamp without time zone, nom character varying, apellido1 character varying, apellido2 character varying, id_tabla character varying, tabla character varying, descripcion character varying, matricula character varying)' \
                                              'language plpgsql as $$ begin return query select  f.fechayhora,p.nombre,p.apellido1,p.apellido2,historial.id_tabla,historial.tabla,d.descripcion,m.matricula' \
                                              ' from historial inner join fecha f on f.id_fecha = historial.fecha inner join medico m on m.matricula = historial.medico inner join descripciones d on d.id_descripcion = historial.descripciones' \
                                              ' inner join persona p on p.id_persona = m.id_persona where m.matricula=$1; end; $$;'
                                        cursor.execute(query)
                                        query='create function busq_hist2(integer, integer, integer) ' \
                                              'returns TABLE(fecha timestamp without time zone, nom character varying, apellido1 character varying, apellido2 character varying, id_tabla character varying, tabla character varying, descripcion character varying, matricula character varying)' \
                                              'language plpgsql as $$ begin return query select  f.fechayhora,p.nombre,p.apellido1,p.apellido2,historial.id_tabla,historial.tabla,d.descripcion,m.matricula' \
                                              ' from historial inner join fecha f on f.id_fecha = historial.fecha inner join medico m on m.matricula = historial.medico inner join descripciones d on d.id_descripcion = historial.descripciones' \
                                              ' inner join persona p on p.id_persona = m.id_persona where extract(year from f.fechayhora)=$1 and extract(month from f.fechayhora)=$2 and extract(day from f.fechayhora)=$3; end; $$;'
                                        cursor.execute(query)
                                        query='create function busqueda_consulta(character varying) ' \
                                              'returns TABLE(fecha timestamp without time zone, id character varying) language plpgsql as $$ begin' \
                                              ' return query select f.fechayhora,id_consulta from consulta inner join fecha f on f.id_fecha = consulta.fecha' \
                                              ' where codigo_paciente=$1 order by f.fechayhora desc; end; $$;'
                                        cursor.execute(query)
                                        query="create function busqueda_paciente1(character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha" \
                                              " inner join consulta c on paciente.id_paciente=c.codigo_paciente inner join fecha f2 on f2.id_fecha = c.fecha " \
                                              "where p.nombre like '%' || $1 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente2(character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha " \
                                              "inner join consulta c on paciente.id_paciente=c.codigo_paciente inner join fecha f2 on f2.id_fecha = c.fecha where p.apellido1 like '%' || $1 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente3(character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha inner join consulta c on paciente.id_paciente=c.codigo_paciente" \
                                              " inner join fecha f2 on f2.id_fecha = c.fecha where p.apellido2 like '%' || $1 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente4(character varying, character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha inner join consulta c on paciente.id_paciente=c.codigo_paciente" \
                                              " inner join fecha f2 on f2.id_fecha = c.fecha where p.nombre like '%' || $1 ||'%' and p.apellido1 like '%' || $2 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente5(character varying, character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone) " \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha " \
                                              "inner join consulta c on paciente.id_paciente=c.codigo_paciente inner join fecha f2 on f2.id_fecha = c.fecha " \
                                              "where p.nombre like '%' || $1 ||'%' and p.apellido2 like '%' || $2 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente6(character varying, character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha inner join consulta c on paciente.id_paciente=c.codigo_paciente" \
                                              " inner join fecha f2 on f2.id_fecha = c.fecha where p.apellido1 like '%' || $1 ||'%' and p.apellido2 like '%' || $2 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_paciente7(character varying, character varying, character varying) " \
                                              "returns TABLE(id_pac character varying, fecha_nac timestamp without time zone, nombre character varying, apellido character varying, apellido2 character varying, fecha_ulti timestamp without time zone)" \
                                              "language plpgsql as $$ begin return query select distinct  on (id_paciente) id_paciente,f.fechayhora,p.nombre,p.apellido1,p.apellido2,f2.fechayhora" \
                                              " from paciente inner join persona p on p.id_persona = paciente.id_persona inner join fecha f on f.id_fecha=p.fecha inner join consulta c on paciente.id_paciente=c.codigo_paciente" \
                                              " inner join fecha f2 on f2.id_fecha = c.fecha where p.nombre like '%' || $1 ||'%' and p.apellido1 like '%' || $2 ||'%'" \
                                              "and p.apellido2 like '%' || $3 ||'%' order by id_paciente,f2.fechayhora desc; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user(character varying, character varying, character varying) returns character varying" \
                                              " language plpgsql as $$ declare c varchar; begin c=(select usuario from medico,persona where nombre =$1 and apellido1=$2" \
                                              " and apellido2=$3); return c; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user1(character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones" \
                                              " inner join persona p on p.id_persona = medico.id_persona where p.nombre like '%' || $1 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user2(character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona" \
                                              " where p.apellido1 like '%' || $1 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user3(character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona" \
                                              " where p.apellido2 like '%' || $1 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user4(character varying, character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona" \
                                              " where p.nombre like '%' || $1 ||'%' and p.apellido1 like '%' || $2 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user5(character varying, character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona" \
                                              " where p.nombre like '%' || $1 ||'%' and p.apellido2 like '%' || $2 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user6(character varying, character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona " \
                                              "where p.apellido1 like '%' || $1 ||'%' and p.apellido2 like '%' || $2 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function busqueda_user7(character varying, character varying, character varying) " \
                                              "returns TABLE(nombre character varying, apellido character varying, apellido2 character varying, correo character varying, estado boolean)" \
                                              "language plpgsql as $$ begin return query select p.nombre,p.apellido1,p.apellido2,medico.correo,v.habilitacion" \
                                              " from medico inner join validaciones v on v.id_validaciones = medico.validaciones inner join persona p on p.id_persona = medico.id_persona" \
                                              " where p.nombre like '%' || $1 ||'%' and p.apellido1 like '%' || $2 ||'%' and p.apellido2 like '%' || $3 ||'%'; end; $$;"
                                        cursor.execute(query)
                                        query="create function datos_usuario(character varying) " \
                                              "returns TABLE(matricula character varying, id_persona character varying, ci integer, validaciones integer, llave character varying, password character varying, correo character varying, numero character varying, extension integer, nombre character varying, apellido1 character varying, apellido2 character varying, sexo integer)" \
                                              "language plpgsql as $$ begin return query select m.matricula,p.id_persona,c.id_carnet,v.id_validaciones,u.sal,u.pass,m.correo,c.numero,c.extension,p.nombre,p.apellido1,p.apellido2,p.tipo_sexo" \
                                              " from medico inner join persona p on p.id_persona = medico.id_persona inner join usuario u on medico.usuario = u.cuenta_user inner join medico m on p.id_persona = m.id_persona" \
                                              " inner join validaciones v on v.id_validaciones = medico.validaciones inner join carnet c on p.id_persona = c.persona where m.usuario=$1; end; $$;"
                                        cursor.execute(query)
                                        query="create function guardar_tema(integer, character varying) returns void language plpgsql as $$" \
                                              " begin update usuario set tema=$1 where cuenta_user=$2; end; $$;"
                                        cursor.execute(query)
                                        query="create function habil(integer) returns void language plpgsql as $$ begin" \
                                              " update validaciones set habilitacion=true where id_validaciones=$1; end; $$;"
                                        cursor.execute(query)
                                        query="create function id_maximo_consulta(character varying) returns character varying" \
                                              " language plpgsql as $$ declare c varchar; begin c=(select max(id_consulta) from consulta where consulta.id_consulta like $1 || '%');" \
                                              "return c; end; $$;"
                                        cursor.execute(query)
                                        query="create function id_maximo_familiar(character varying) returns character varying" \
                                              " language plpgsql as $$ declare c varchar; begin c=(select max(id_familiar) from familiar where familiar.id_familiar like $1 || '%');" \
                                              "return c; end; $$;"
                                        cursor.execute(query)
                                        query="create function id_maximo_paciente(character varying) returns character varying " \
                                              "language plpgsql as $$ declare c varchar; begin c=(select max(id_paciente) from paciente where paciente.id_paciente like $1 || '%');" \
                                              "return c; end; $$;"
                                        cursor.execute(query)
                                        query="create function id_maximo_persona(character varying) returns character varying " \
                                              "language plpgsql as $$ declare c varchar; begin c=(select max(id_persona) from persona where id_persona like $1 || '%');" \
                                              "return c; end; $$;"
                                        cursor.execute(query)
                                        query="create function inhabil(integer) returns void language plpgsql as $$ begin" \
                                              " update validaciones set habilitacion=false where id_validaciones=$1; end; $$;"
                                        cursor.execute(query)
                                        query="create function update_pass_user(character varying, character varying, character varying) returns void " \
                                              "language plpgsql as $$ begin update usuario set pass=$2, sal=$3 where cuenta_user=$1; end; $$;"
                                        cursor.execute(query)
                                        query="create function update_validacion(integer, boolean) returns void language plpgsql as $$ begin" \
                                              " update validaciones set validacion=$2 where id_validaciones=$1; end; $$;"
                                        cursor.execute(query)
                                        query="create function validacion(character varying) returns integer " \
                                              "language plpgsql as $$ declare c integer; begin c=(select validaciones " \
                                              "from medico where usuario=$1); return c; end; $$;"
                                        cursor.execute(query)
                                        resp6=1
                                    except:
                                        resp6=0
                                    #endregion
                                    if resp6==1:
                                        self.ui.lbl_progreso.setText("Funciones creadas con éxito")
                                        #region Crear grupo medico y dar permisos
                                        try:
                                            self.ui.lbl_progreso.setText("Creando grupo medico y otorgando permisos")
                                            self.timer.start(5)
                                            query="create role grupo_medico with inherit;"
                                            cursor.execute(query)
                                            query='grant connect on database "CLINICA" to grupo_medico;'
                                            cursor.execute(query)
                                            query='grant select, insert, update on "CLINICA".public.usuario to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.medico to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.carnet to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.dato_general to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.antecedentes to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.consulta to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.paciente to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.persona to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.familiar to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.telefono to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.fecha to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.validaciones to grupo_medico;'
                                            cursor.execute(query)
                                            query = 'grant select, insert, update on "CLINICA".public.historial to grupo_medico;'
                                            cursor.execute(query)
                                            resp7=1
                                        except:
                                            resp7=0
                                        #endregion
                                        if resp7==1:
                                            self.ui.lbl_progreso.setText("TODAS LAS CONFIGURACIONES SE \n"
                                                                         "REALIZARON CON ÉXITO, PUEDE \n"
                                                                         "INSTALAR EL PROGRAMA PRINCIPAL")
                                        else:
                                            self.ui.lbl_progreso.setText("Algo salió mal, crear grupo médico manualmente")
                                    else:
                                        self.ui.lbl_progreso.setText("No se pudieron crear las funciones")
                                else:
                                    self.ui.lbl_progreso.setText("Algo salio mal no se pudo insertar los datos")
                            else:
                                self.ui.lbl_progreso.setText("No se pudieron crear las tablas")
                        else:
                            self.ui.lbl_progreso.setText("No se pudo conectar a la base de datos")
                    else:
                        self.ui.lbl_progreso.setText("No se pudo crear el admin")
                else:
                    self.ui.lbl_progreso.setText("Ha ocurrido un error\nNo se ha creado la base de datos")


    #endregion
    def Progreso(self):
        global counter
        self.ui.pb_barra1.setVisible(True)
        self.ui.pb_barra1.setValue(counter)
        if counter>100:
            self.timer.stop()
            self.ui.pb_barra1.setVisible(False)
        counter+=1
### ::::::::::: damos inicio a la aplicacion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Iniciar_programa()
    window.show()
    sys.exit(app.exec_())