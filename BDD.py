import sqlite3

def connect_to_db():
    conn = sqlite3.connect('Telescope_BDD.db')
    return conn



#table Objet
def insert_object(objet):
    inserted_object = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Objet (Nom_obj, Ascension_droite, Declinaison, Magnitude, Id_type, Id_const) VALUES (?, ?, ?, ?, ?, ?)", 
                    (objet['Nom_obj'], objet['Ascension_droite'], objet['Declinaison'],
                    objet['Magnitude'], objet['Id_type'], objet['Id_const'])  )
        conn.commit()
        inserted_object = get_object_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_object


def get_objects():
    objets = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Objet Natural Join Type Natural Join Constellation")
        rows = cur.fetchall()

        # Convert
        for i in rows:
            objet = {}
            objet["Id_obj"] = i["Id_obj"]
            objet["Nom_obj"] = i["Nom_obj"]
            objet["Ascension_droite"] = i["Ascension_droite"]
            objet["Declinaison"] = i["Declinaison"]
            objet["Magnitude"] = i["Magnitude"]
            objet["Nom_type"] = i["Nom_type"]
            objet["Nom_const"] = i["Nom_const"]
            objets.append(objet)

    except:
        objets = []
    return objets


def get_object_by_id(Id_obj):
    objet = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Objet Natural Join Type Natural Join Constellation  WHERE Id_obj = ? ",(Id_obj,))
        row = cur.fetchone()

        # Convert
        objet["Id_obj"] = row["Id_obj"]
        objet["Nom_obj"] = row["Nom_obj"]
        objet["Ascension_droite"] = row["Ascension_droite"]
        objet["Declinaison"] = row["Declinaison"]
        objet["Magnitude"] = row["Magnitude"]
        objet["Id_type"] = row["Id_type"]
        objet["Id_const"] = row["Id_const"]
        objet["Nom_type"] = row["Nom_type"]
        objet["Nom_const"] = row["Nom_const"]
    except:
        objet = {}
    
    return objet


def update_object(objet):
    updated_object = {} 
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE Objet SET Nom_obj = ?, Ascension_droite = ?, Declinaison = ?, Magnitude = ?, Id_type = ?, Id_const = ? WHERE Id_obj = ?",
                    (objet["Nom_obj"], objet["Ascension_droite"], objet["Declinaison"], objet["Magnitude"], objet["Id_type"], objet["Id_const"],
                    objet["Id_obj"],))
        conn.commit()
        #return the object
        updated_object = get_object_by_id(objet["Id_obj"])

    except:
        conn.rollback()
        updated_objet = {}
    finally:
        conn.close()

    return updated_object


def delete_object(Id_obj):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM Objet WHERE Id_obj = ?",
                    (Id_obj,))
        conn.commit()
        message["status"] = "Objet supprimer avec succès"
    except:
        conn.rollback()
        message["status"] = "Impossible de supprimer l'objet"
    finally:
        conn.close()

    return message


objet ={
    "Nom_obj": " ",
    "Ascension_droite": " ",
    "Declinaison": " ",
    "Magnitude": " ",
    "Id_type": " ",
    "Id_const": " "
}



#Table Constellation
def get_constellations():
    constellations = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Constellation")
        rows = cur.fetchall()

        # Convert
        for i in rows:
            constellation = {}
            constellation["Id_const"] = i["Id_const"]
            constellation["Nom_const"] = i["Nom_const"]
            constellations.append(constellation)

    except:
        constellations = []
    return constellations



def get_const_by_id(Id_const):
    constellation = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Constellation WHERE Id_const = ?",(Id_const,))
        row = cur.fetchone()

        # Convert
        constellation["Id_const"] = row["Id_const"]
        constellation["Nom_const"] = row["Nom_const"]
    except:
        constellation = {}
    
    return constellation




#Table Type
def get_types():
    types = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Type")
        rows = cur.fetchall()

        # Convert
        for i in rows:
            _type = {}
            _type["Id_type"] = i["Id_type"]
            _type["Nom_type"] = i["Nom_type"]
            types.append(_type)

    except:
        types = []
    return types



def get_type_by_id(Id_type):
    _type = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Type WHERE Id_type = ?",(Id_type,))
        row = cur.fetchone()

        # Convert
        _type["Id_type"] = row["Id_type"]
        _type["Nom_type"] = row["Nom_type"]
    except:
        _type = {}
    
    return _type
