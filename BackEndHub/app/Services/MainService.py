from sqlite3 import IntegrityError
from uu import Error

from fastapi import HTTPException
from app.Entities.BasicEntities import Camera, Log, Note, ParkingSite, User
from app.Helper.DBConnection import DBConnection
import logging
from app.Entities.TrafficViolation import TrafficViolation
#This should've call another script that handle the DB querys...
class MainService():


    def __init__(self):
        self.data = None
        self.tableNameTF = 'TrafficViolation'
        self.tableNameCM = 'Cameras'
        self.tableNamePS = 'ParkingSite'
        self.tableNameUSR = 'Users'
        self.tableNameLOG = 'Logs'
        self.tableNameOP = 'Operations'
        self.tableNameNT = 'Notes'
        self.database = 'OnStreetParking'
 
 ######################
 #      Insert        #
 ######################

    def insertNotes(self, note:Note):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Insert into {self.database}.{self.tableNameNT} (nt_user, nt_text) values ((select usr_id from {self.database}.{self.tableNameUSR} where usr_name = %s)  ,%s) ", (note.nt_user, note.nt_text))
                print(cursor.rowcount, "record inserted.")                
            connection.commit()
 
    def insertOrUpdatePolygon(self, cm_id, cm_ps_id, cm_polygon):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Insert into {self.database}.{self.tableNameCM} (cm_id, cm_ps_id, cm_polygon) values (%s,%s,%s) ON DUPLICATE KEY UPDATE cm_polygon = %s ", (cm_id,cm_ps_id,cm_polygon,cm_polygon))
                print(cursor.rowcount, "record inserted.")                
            connection.commit()
 
    def insertTrafficViolation(self, tf_id, tf_desc, tf_location, tf_ref):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                tf_ref = tf_ref.replace('"','')
                cursor.execute(f"Insert into {self.database}.{self.tableNameTF} (tf_id, tf_desc, tf_location, tf_ref_parksite) values (%s,%s,%s,%s) ", (tf_id,tf_desc,tf_location,tf_ref))
                print(cursor.rowcount, "record inserted.")                
            connection.commit()

    def insertOnStreetParking(self,idd,desc,location,max_ps):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Insert into {self.database}.{self.tableNamePS} (ps_id, ps_description, ps_location, ps_max_parking_spots) values (%s,%s,%s,%s)" ,(idd,desc,location,max_ps))
                print(cursor.rowcount, "record inserted.")                
            connection.commit()
            
    def insertUser(self, user : User):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"Insert into {self.database}.{self.tableNameUSR} ( usr_name, usr_email, usr_role,usr_profile_pic) values (%s,%s,%s,%s)" ,
                                (user.usr_name, user.usr_email, "user", user.usr_profile_pic))
                    print(cursor.rowcount, "record inserted.")                
                except :
                    raise Error("Something went wrong...")
                finally:
                    logging.debug(" do something after...")
            connection.commit()
            
    def insertLog(self, log : Log):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(f"Insert into {self.database}.{self.tableNameLOG} (lg_operation_id, lg_user_id, lg_description ) values ( (select op_id from {self.database}.{self.tableNameOP} where op_type = %s and op_level =%s), %s, %s) " ,
                                (log.lg_operation.op_type, log.lg_operation.op_level, log.lg_user_id, log.lg_description))
                    print(cursor.rowcount, "record inserted.")                
                except Error as e:
                    logging.error(e.__cause__)
                    raise Error("Something went wrong...")
                finally:
                    logging.debug(" do something after...")
            connection.commit()


 ######################
 #      Get           #
 ######################

    def getTrafficViolationById(self, tf_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved from {self.database}.{self.tableNameTF} where tf_id= %s ", (tf_id,))
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList[0]
 
    def getUserByEmail(self, email):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select usr_id,usr_name,usr_email,usr_creation_date,usr_role, usr_profile_pic from {self.database}.{self.tableNameUSR} where usr_email = %s ", (email,))
                print(cursor.rowcount, "records")                
                output = cursor.fetchone()
                if output:
                    return User(**output) #type: ignore
        return

    def getUsers(self):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select usr_id,usr_name,usr_email,usr_creation_date,usr_role, usr_profile_pic from {self.database}.{self.tableNameUSR} ")
                print(cursor.rowcount, "records")                
                output = cursor.fetchall()
                if output:
                    return output #type: ignore
        return

    def getNotesByUser(self, nt_user):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select nt_id,nt_user,nt_text from {self.database}.{self.tableNameNT} join {self.database}.{self.tableNameUSR} on nt_user = usr_id where usr_name = %s order by nt_date desc", (nt_user,))
                print(cursor.rowcount, "records")                
                output = cursor.fetchall()
                if output:
                    return output #type: ignore
        return

    def getNotesByUserLatest(self, nt_user):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select nt_id,nt_user,nt_text,nt_date from {self.database}.{self.tableNameNT}  join {self.database}.{self.tableNameUSR} on nt_user = usr_id where usr_name  = %s order by nt_date desc", (nt_user,))
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList[0]

    def getLogs(self):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select lg.lg_id, op.op_type, op.op_level, us.usr_name, lg.lg_description, lg.lg_date_ins from {self.database}.{self.tableNameLOG} lg join {self.database}.{self.tableNameOP} op on op.op_id = lg.lg_operation_id join {self.database}.{self.tableNameUSR} us on lg.lg_user_id = us.usr_id")
                print(cursor.rowcount, "records")                
                output = cursor.fetchall()
                if output:
                    return output #type: ignore
        return

    def getCameraById(self, id):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select cm_id, cm_ps_id, cm_polygon from {self.database}.{self.tableNameCM} where cm_id = %s ", (id,))
                print(cursor.rowcount, "records")                
                output = cursor.fetchone()
                if output:
                    return Camera(**output) #type: ignore
        return

    def getAllCameras(self):
        db = DBConnection()
        output = None
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select cm_id, cm_ps_id, cm_polygon from {self.database}.{self.tableNameCM}",)
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList #type: ignore

    def getTrafficViolationStats(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT tf_ref_parksite, count(*) FROM {self.database}.{self.tableNameTF} group by tf_ref_parksite ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList

    def getTrafficViolationStats1(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT tf_ref_parksite, date(tf_date_ins), count(*) FROM {self.database}.{self.tableNameTF} as t group by tf_ref_parksite,date(tf_date_ins) ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList

    def getTrafficViolationStats2(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT tf_ref_parksite, tf_resolved, count(*) FROM {self.database}.{self.tableNameTF} group by tf_ref_parksite,tf_resolved ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList

    def getTrafficViolationStats3(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT coalesce(date(tf_date_resolved),date(now())), count(*) FROM {self.database}.{self.tableNameTF} as t group by coalesce(date(tf_date_resolved),date(now())) order by 2 ")
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList

    def getTrafficViolationList(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved,tf_user_name from {self.database}.{self.tableNameTF} order by tf_resolved asc, tf_date_resolved desc")
                print(cursor.rowcount, "records")                
                for item in cursor.fetchall():
                    tf_obj = TrafficViolation(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]) # type: ignore
                    outputList.append(tf_obj)                
        return outputList
    
    def getTrafficViolationListUnresolved(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved,tf_user_name from {self.database}.{self.tableNameTF} where tf_resolved = 0 order by tf_resolved asc")
                print(cursor.rowcount, "records")                
                for item in cursor.fetchall():
                    tf_obj = TrafficViolation(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7]) # type: ignore
                    outputList.append(tf_obj)               
        return outputList
           
    def getTrafficViolationListByPsId(self, ps_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select tf_id,tf_desc,tf_location,tf_ref_parksite,tf_date_ins,tf_date_resolved,tf_resolved, tf_user_name from {self.database}.{self.tableNameTF} where tf_ref_parksite = %s ", (ps_id,))
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList
     
    def getParkingSiteList(self):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute(f"Select ps_id, ps_description, ps_location, ps_max_parking_spots from {self.database}.{self.tableNamePS} ")
                print(cursor.rowcount, "records")                
                output = cursor.fetchall()
                for item in output:
                    print(item)
                    outputList.append(ParkingSite(**item)) #type: ignore
        return outputList
        
    def getParkingSiteById(self, ps_id):
        db = DBConnection()
        outputList = []
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"Select ps_id, ps_description, ps_location, ps_max_parking_spots from {self.database}.{self.tableNamePS} where ps_id = %s ", (ps_id,))
                print(cursor.rowcount, "records")                
                outputList = cursor.fetchall()
        return outputList[0]
    
    
 ######################
 #      Update        #
 ######################
    
    def updateTFResolved(self, tf_id,tf_resolved, tf_username):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"update {self.database}.{self.tableNameTF} set tf_resolved = {tf_resolved}, tf_date_resolved = now(), tf_user_name = %s where tf_id = %s ", (tf_username,tf_id,))
                print(cursor.rowcount, "records")                
            connection.commit()

    def updateParkingSite(self, ps_id,ps_desc, ps_number):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"update {self.database}.{self.tableNamePS} set ps_description = %s, ps_max_parking_spots = %s where ps_id = %s ", (ps_desc,int(ps_number),ps_id,))
                print(cursor.rowcount, "records")                
            connection.commit()
            
 ######################
 #      Delete        #
 ######################
            
    def deleteParkingSite(self, ps_id):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"delete from {self.database}.{self.tableNamePS} where ps_id = %s ", (ps_id,))
                print(cursor.rowcount, "records")                
            connection.commit()
            
    def deleteNote(self, nt_id):
        db = DBConnection()
        with db.getConnection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"delete from {self.database}.{self.tableNameNT} where nt_id = %s ", (nt_id,))
                print(cursor.rowcount, "records")                
            connection.commit()