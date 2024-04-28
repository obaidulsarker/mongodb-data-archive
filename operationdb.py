import sqlite3
from setting import get_variables
from logger import Logger

# operation master class
class OperationMaster:
    def __init__(self, operation_id, operation_log, start_datetime, end_datetime, total_duration, operation_status, source_database_ip, destination_database_ip, total_tasks, total_passed_tasks):
        self.operation_id =  operation_id
        self.operation_log = operation_log
        self.start_datetime=start_datetime
        self.end_datetime = end_datetime
        self.total_duration = total_duration
        self.operation_status = operation_status
        self.source_database_ip = source_database_ip
        self. destination_database_ip = destination_database_ip
        self.total_tasks = total_tasks
        self.total_passed_tasks = total_passed_tasks
        

# operation detail class
class OperationDetail:
    def __init__(self, operation_id, task_id, task_name, task_description, task_start_datetime, task_end_datetime, task_duration, task_status, remarks, id_field_name, ts_field_name):
        self.operation_id =  operation_id
        self.task_id=task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_start_datetime = task_start_datetime
        self.task_end_datetime = task_end_datetime
        self.task_duration = task_duration
        self.task_status = task_status
        self.remarks = remarks
        self.id_field_name = id_field_name
        self.ts_field_name = ts_field_name

class OperationMasterData(Logger):
    def __init__(self, logfile, OperationMasterObj):
        super().__init__(logfile)
        self.operation_id =  OperationMasterObj.operation_id
        self.operation_log = OperationMasterObj.operation_log
        self.start_datetime=OperationMasterObj.start_datetime
        self.end_datetime = OperationMasterObj.end_datetime
        self.total_duration = OperationMasterObj.total_duration
        self.operation_status = OperationMasterObj.operation_status
        self.source_database_ip = OperationMasterObj.source_database_ip
        self. destination_database_ip = OperationMasterObj.destination_database_ip
        self.total_tasks = OperationMasterObj.total_tasks
        self.total_passed_tasks = OperationMasterObj.total_passed_tasks
        self.db = get_variables().AUTOMATION_DB

    def connect(self):
        try:
            connection = sqlite3.connect(self.db)
            connection.isolation_level = None

            # print(f"Connected to {self.db}")

            return connection  # Success
        except Exception as e:
            print(f"Error: {e}")
            self.log_error(f"Exception: {str(e)}")
            return None  # Error
             
    #@staticmethod
    def create(self):
        try:
            cursor = self.connect().cursor()
            sql = f"""INSERT INTO operation (operation_id, operation_log, start_datetime, end_datetime, total_duration, operation_status, source_database_ip, destination_database_ip, 
            total_tasks, total_passed_tasks)
            VALUES ('{self.operation_id}', '{self.operation_log}', '{self.start_datetime}', '{self.end_datetime}', '{self.total_duration}', '{self.operation_status}', '{self.source_database_ip}', '{self.destination_database_ip}', '{self.total_tasks}', '{self.total_passed_tasks}');
            """
            #print(sql)
            cursor.execute(sql)
            self.connect().commit()

            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return False
    
    #@staticmethod
    def read_all(self):
        try:
            cursor = self.connect().cursor()
            cursor.execute("SELECT * FROM operation")
            rows = cursor.fetchall()
            return [OperationMaster(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None
    
    #@staticmethod
    def read_by_id(self, id):
        try:
            sql = f"SELECT * FROM operation WHERE operation_id='{id}'"
            cursor = self.connect().cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [OperationMaster(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None
        
    #@staticmethod
    def update(self):
        try:
            if (id==None):
                raise Exception("Please provide Id of the operation!")
            
            #print("START---")
            sql_upd_col = "UPDATE operation SET "
            sql_where = f" WHERE operation_id='{self.operation_id}';"
            col_no = 0

            if (self.operation_log!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" operation_log='{self.operation_log}'"
                else:
                    sql_upd_col = sql_upd_col + f", operation_log='{self.operation_log}'"
                col_no = col_no +1

            if (self.start_datetime!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" start_datetime='{self.start_datetime}'"
                else:
                    sql_upd_col = sql_upd_col + f", start_datetime='{self.start_datetime}'"
                col_no = col_no +1
            
            if (self.end_datetime!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" end_datetime='{self.end_datetime}'"
                else:
                    sql_upd_col = sql_upd_col + f", end_datetime='{self.end_datetime}'"
                col_no = col_no +1

            if (self.total_duration!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" total_duration='{self.total_duration}'"
                else:
                    sql_upd_col = sql_upd_col + f", total_duration='{self.total_duration}'"
                col_no = col_no +1

            if (self.operation_status!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" operation_status='{self.operation_status}'"
                else:
                    sql_upd_col = sql_upd_col + f", operation_status='{self.operation_status}'"
                col_no = col_no +1

            if (self.source_database_ip!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" source_database_ip='{self.source_database_ip}'"
                else:
                    sql_upd_col = sql_upd_col + f", source_database_ip='{self.source_database_ip}'"
                col_no = col_no +1

            if (self.destination_database_ip!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" destination_database_ip='{self.destination_database_ip}'"
                else:
                    sql_upd_col = sql_upd_col + f", destination_database_ip='{self.destination_database_ip}'"
                col_no = col_no +1

            if (self.total_tasks!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" total_tasks={self.total_tasks}"
                else:
                    sql_upd_col = sql_upd_col + f", total_tasks={self.total_tasks}"
                col_no = col_no +1

            if (self.total_passed_tasks!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" total_passed_tasks={self.total_passed_tasks}"
                else:
                    sql_upd_col = sql_upd_col + f", total_passed_tasks={self.total_passed_tasks}"
                col_no = col_no +1

            # concat
            sql = sql_upd_col +" "+ sql_where
            # print(sql)
            # self.log_info(sql)

            cursor = self.connect().cursor()
            cursor.execute(sql)
            self.connect().commit()

            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None

    #@staticmethod
    def delete(self, id):
        try:
            sql = f"DELETE FROM operation WHERE operation_id = '{id}'"
            cursor = self.connect().cursor()
            cursor.execute(sql)
            self.connect().commit()
            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None

# Operation Details
class OperationDetailData(Logger):
    def __init__(self, logfile, OperationDetailObj):
        super().__init__(logfile)
        self.db = get_variables().AUTOMATION_DB
        self.operation_id =  OperationDetailObj.operation_id
        self.task_id=OperationDetailObj.task_id
        self.task_name = OperationDetailObj.task_name
        self.task_description = OperationDetailObj.task_description
        self.task_start_datetime = OperationDetailObj.task_start_datetime
        self.task_end_datetime = OperationDetailObj.task_end_datetime
        self.task_duration = OperationDetailObj.task_duration
        self.task_status = OperationDetailObj.task_status
        self.remarks = OperationDetailObj.remarks
        self.id_field_name = OperationDetailObj.id_field_name
        self.ts_field_name = OperationDetailObj.ts_field_name

    def connect(self):
        try:
            connection = sqlite3.connect(self.db)

            connection.isolation_level = None

            return connection  # Success
        
        except Exception as e:
            print(f"Error: {e}")
            self.log_error(f"Exception: {str(e)}")
            return None  # Error
             
    #@staticmethod
    def create(self):
        try:
            sql = f"""INSERT INTO operation_details (operation_id, task_id, task_name, task_description, task_start_datetime, task_end_datetime, task_duration, task_status, remarks, id_field_name, ts_field_name)
              VALUES  ('{self.operation_id}', {self.task_id}, '{self.task_name}', '{self.task_description}', '{self.task_start_datetime}', '{self.task_end_datetime}', '{self.task_duration}', '{self.task_status}', '{self.remarks}', '{self.id_field_name}', '{self.ts_field_name}');
"""
            #print(sql)
            cursor = self.connect().cursor()
            cursor.execute(sql)
            self.connect().commit()

            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return False
    
    #@staticmethod
    def read_all(self):
        try:
            cursor = self.connect().cursor()
            cursor.execute("SELECT * FROM operation_details")
            rows = cursor.fetchall()
            return [OperationDetail(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None
    
    #@staticmethod
    def read_by_id(self, id):
        try:
            cursor = self.connect().cursor()
            cursor.execute(f"SELECT * FROM operation_details WHERE operation_id='{id}'")
            rows = cursor.fetchall()
            return [OperationDetail(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None
        
    #@staticmethod
    def update(self):
        try:
            if (self.operation_id==None):
                raise Exception("Id should be empty!")
            
            sql_upd_col = "UPDATE operation_details SET "
            sql_where = f" WHERE operation_id='{self.operation_id}' AND tasK_id='{self.task_id}';"
            col_no = 0

            if (self.task_id!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_id={self.task_id}"
                else:
                    sql_upd_col = sql_upd_col + f", task_id={self.task_id}"
                col_no = col_no +1

            if (self.task_name!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_name='{self.task_name}'"
                else:
                    sql_upd_col = sql_upd_col + f",  task_name='{self.task_name}'"
                col_no = col_no +1

            if (self.task_description!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_description='{self.task_description}'"
                else:
                    sql_upd_col = sql_upd_col + f", task_description='{self.task_description}'"
                col_no = col_no +1

            if (self.task_start_datetime!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_start_datetime='{self.task_start_datetime}'"
                else:
                    sql_upd_col = sql_upd_col + f", task_start_datetime='{self.task_start_datetime}'"
                col_no = col_no +1

            if (self.task_end_datetime!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_end_datetime='{self.task_end_datetime}'"
                else:
                    sql_upd_col = sql_upd_col + f", task_end_datetime='{self.task_end_datetime}'"
                col_no = col_no +1

            if (self.task_duration!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_duration='{self.task_duration}'"
                else:
                    sql_upd_col = sql_upd_col + f", task_duration='{self.task_duration}'"
                col_no = col_no +1

            if (self.task_status!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" task_status='{self.task_status}'"
                else:
                    sql_upd_col = sql_upd_col + f", task_status='{self.task_status}'"
                col_no = col_no +1

            if (self.remarks!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" remarks='{self.remarks}'"
                else:
                    sql_upd_col = sql_upd_col + f", remarks='{self.remarks}'"
                col_no = col_no +1

            if (self.id_field_name!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" id_field_name='{self.id_field_name}'"
                else:
                    sql_upd_col = sql_upd_col + f", id_field_name='{self.id_field_name}'"
                col_no = col_no +1

            if (self.ts_field_name!=None):
                if (col_no==0):
                    sql_upd_col = sql_upd_col + f" ts_field_name='{self.ts_field_name}'"
                else:
                    sql_upd_col = sql_upd_col + f", ts_field_name='{self.ts_field_name}'"
                col_no = col_no +1

            # concat
            sql = sql_upd_col +" "+ sql_where
            #print(sql)
            #self.log_info(sql)
            
            cursor = self.connect().cursor()
            cursor.execute(sql)

            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None

    #@staticmethod
    def delete(self):
        try:
            cursor = self.connect().cursor()
            sql = f"DELETE FROM operation_details WHERE operation_id='{self.operation_id}' AND tasK_id='{self.task_id}';"
            cursor.execute(sql)
            self.connect().commit()
            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None

#Read Operation DB ******************************************************************************
class read_operation_db:
    def __init__(self, operation_id) -> None:
        self.operation_id = operation_id
        self.db = get_variables().AUTOMATION_DB

    def connect(self):
        try:
            connection = sqlite3.connect(self.db)
            connection.isolation_level = None

            print(f"Connected to {self.db}")

            return connection  # Success
        except Exception as e:
            print(f"Error: {e}")
            self.log_error(f"Exception: {str(e)}")
            return None  # Error
        
    # Read operation master info
    def read_operation_master(self):
        try:
            sql = f"SELECT * FROM operation WHERE operation_id='{self.operation_id}'"
            cursor = self.connect().cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [OperationMaster(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            #self.log_error(f"Exception: {str(e)}")
            return None

    # read operation detail info
    def read_operation_detail(self):
        try:
            cursor = self.connect().cursor()
            cursor.execute(f"SELECT * FROM operation_details WHERE operation_id='{self.operation_id}'")
            rows = cursor.fetchall()
            return [OperationDetail(*row) for row in rows]
        except Exception as e:
            print(f"Exception: {str(e)}")
            #self.log_error(f"Exception: {str(e)}")
            return None

# Operation DB Wraper Class **************************************************************************
class operation_db:
    def __init__(self, operation_log, operation_master, task_lst):
        self.operation_log = operation_log
        self.operation_master = operation_master 
        self.task_lst = task_lst
        self.operation_detail_lst = []

    # Initialize operation database
    def setup_operation_database(self):
        try:
            current_datetime = self.operation_master.start_datetime
            
            operation_id=self.operation_master.operation_id
            #operation_obj = OperationMaster(operation_id=self.operation_id, operation_log=self.operation_log, self.start_datetime=current_datetime, end_datetime=None, total_duration=None, operation_status="In-Progress", source_database_vm_name=source_vm_name, source_database_vm_ip=source_database_vm_ip, total_tasks=total_tasks, total_passed_tasks=0, output_dump_file=None, output_data_disk_snapshot=None)
            operation_master_data = OperationMasterData(logfile=self.operation_log, 
                                                        OperationMasterObj=self.operation_master)
            result= operation_master_data.create()
            if (result==False):
                raise Exception("Unable to save operational master information into database!")
            

            for task in self.task_lst:
                operation_detail_obj = OperationDetail(operation_id=operation_id, 
                                                       task_id=task.task_no, 
                                                       task_name=task.task_name, 
                                                       task_description=task.task_description, 
                                                       task_start_datetime=None, 
                                                       task_end_datetime=None, 
                                                       task_duration=None, 
                                                       task_status="Not Started", 
                                                       remarks=None,
                                                       id_field_name=task.id_field_name,
                                                       ts_field_name = task.ts_field_name
                                                       )
                # Append into List
                self.operation_detail_lst.append(operation_detail_obj)

                operation_detail_data = OperationDetailData(logfile=self.operation_log, 
                                                            OperationDetailObj=operation_detail_obj)
                result= operation_detail_data.create()
                if (result==False):
                    raise Exception("Unable to save operational detail information into database!")
            
            return True
        except Exception as e:
            print(f"Exception: {str(e)}")
            return None

    def update_operation_master(self):
        try:
            operation_master_data = OperationMasterData(logfile=self.operation_log, 
                                                        OperationMasterObj=self.operation_master)
            status = operation_master_data.update()
            
            return status
        except Exception as e:
            print(f"Exception: {str(e)}")
            return None
    
    def update_operation_detail(self, OperationDetail):
        try:
            operation_detail_data = OperationDetailData(
                logfile=self.operation_log,
                OperationDetailObj=OperationDetail
            )
            status = operation_detail_data.update()
            
            return status
        except Exception as e:
            print(f"Exception: {str(e)}")
            return None
        
# if __name__ == "__main__":

#     operation_log="logs\log_7ce9a471-0c09-4092-8ee1-22c8739f9fec_2024-04-16_12-46-10.log"

#     #Defind SQL execution Instance
#     operation_obj = OperationMaster(operation_id="5af7fd65-8edd-444d-ab1d-68909f8bda0a", start_datetime="2023-10-23 23:19:34", end_datetime="2023-10-23 23:19:34", total_duration="", operation_status="Inprogress", source_database_vm_name="VM1", source_database_vm_ip="10.10.01.01", total_tasks=26, total_passed_tasks="", output_dump_file="", output_data_disk_snapshot="")
#     operation_master_data = OperationMasterData(logfile=operation_log, OperationMasterObj=operation_obj)
#     result= operation_master_data.update(id="5af7fd65-8edd-444d-ab1d-68909f8bda0a", end_datetime="2023-11-08 17:00:00", total_duration="08:00:10")
#     print(result)
#     result = operation_master_data.read_by_id(id="5af7fd65-8edd-444d-ab1d-68909f8bda0a")
#     for r in result:
#         print(r.total_duration)

#     result= operation_master_data.delete(id="5af7fd65-8edd-444d-ab1d-68909f8bda0a")
                                         
#     operation_detail_obj = OperationDetail(operation_id="5af7fd65-8edd-444d-ab1d-68909f8bda0a", task_id="1", task_name="Connect_Google_Cloud", task_description="Test Google cloud connection", task_start_datetime="2023-11-08 28:00:00", task_end_datetime="2023-11-08 28:00:00", task_duration="09:00:00", task_status="Pedning", remarks=None)
#     operation_detail_data = OperationDetailData(logfile=operation_log, OperationDetailObj=operation_detail_obj)
#     result=operation_detail_data.update(id="5af7fd65-8edd-444d-ab1d-68909f8bda0a", task_name="Connect_Google_Cloud2")
#     print(result)
#     result = operation_detail_data.read_by_id(id="5af7fd65-8edd-444d-ab1d-68909f8bda0a")
#     for r in result:
#         print(r.task_name)

