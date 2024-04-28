from db import DatabaseExecutor
from logger import Logger
from xml_reader import XmlReader
from setting import get_variables
from notification import notification
from operationdb import operation_db, OperationMaster
import time
from timeit import default_timer as timer
from datetime import datetime
from task import *

class Automation(Logger):
    def __init__(self, logfile, operation_id):
        super().__init__(logfile)
        self.operation_log=logfile
        self.operation_id = operation_id

        # Create a list to store Task objects
        self.task_list = []

    # Doing automation tasks
    def start_jobs(self):
        try:
        
            operation_log = self.operation_log

            # Notification Instance
            notification_log_file = get_variables().NOTIFICATION_LOG
            notification_instance = notification(logfile=notification_log_file)

            # Defind SQL execution Instance
            db = DatabaseExecutor(operation_log)
            
            # Collection instance
            collection_list = XmlReader(logfile=operation_log)

            # load operation info into database

            # Get collection list
            self.task_list = collection_list.get_task_list()
            print(f"Total collection: {len(self.task_list)}")
            self.log_info(f"Total collection: {len(self.task_list)}")

            total_passed_tasks = 0
            grand_total_seconds = 0

            source_database_ip = get_variables().MONGODB_HOST
            destination_database_ip = get_variables().ARCHIVE_MONGODB_HOST

            operationMasterObj = OperationMaster(operation_id=self.operation_id,
                                                 operation_log=self.operation_log,
                                                 start_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                 end_datetime=None,
                                                 total_duration=None,
                                                 operation_status="In Progress",
                                                 source_database_ip=source_database_ip,
                                                 destination_database_ip=destination_database_ip,
                                                 total_tasks=len(self.task_list),
                                                 total_passed_tasks=0
                                                 )
            
            operation_db_instance = operation_db(operation_log=operation_log, 
                                                 operation_master=operationMasterObj,
                                                 task_lst=self.task_list
                                                 )
            load_status = operation_db_instance.setup_operation_database()

            # timer
            total_passed_tasks = 0
            grand_total_seconds = 0

            # Get total collection 
            #collection_lst = collection_list.get_collection_list()
            #print(type(collection_lst))

            total_collection = collection_list.total_collection

            #for collection in collection_lst:
            for task in operation_db_instance.operation_detail_lst:
                # Timer
                start = timer()

                print("********************************************************************")
                self.log_info("********************************************************************")
                print(f"Archiving started: {task.task_name}")
                print("===================================================")
                self.log_info(f"Archiving started: {task.task_name}")
                self.log_info("===================================================")

                # Update Task Status
                task.task_start_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task.task_status = "In Progress"
                task_status = task.task_status

                # Update Task into database
                upd_task_status = operation_db_instance.update_operation_detail(OperationDetail=task)

                #total_deleted = db.delete_old_data(collection_name=collection.collection_name ,ts_field_name=collection.ts_field_name, id_field_name=collection.id_field_name)
                total_deleted = db.delete_old_data_by_date(collection_name=task.task_name ,ts_field_name=task.ts_field_name, id_field_name=task.id_field_name)

                # Update task status
                if (total_deleted<0):
                    task.task_status="Failed"
                    task.remarks=f"Unable to archive {task.task_name} collection."
                    self.log_error(f"{task.remarks}")
                    print(f"{task.remarks}")
                    #raise Exception(f"{task.remarks}")
                else:
                    total_passed_tasks = total_passed_tasks + 1
                    task.task_status="Completed"
                
                # Compact database
                compact_status = db.compact_collection(collection_name=task.task_name)
                if (compact_status is None):
                    task.remarks=f"Unable to compact {task.task_name} collection."
                    self.log_error(f"{task.remarks}")
                    print(f"{task.remarks}")

                # Task-wise end time
                end = timer()
                total_seconds = end - start
                duration = time.strftime("%H:%M:%S", time.gmtime(total_seconds))
                grand_total_seconds=grand_total_seconds+total_seconds
                #total_passed_tasks = total_passed_tasks + 1

                print(f"Archiving completed: {task.task_name}, Elapse Duration: {duration}")
                self.log_info(f"Archiving completed: {task.task_name}, Elapse Duration: {duration}")

                print(f"Total Completed Collections: {total_passed_tasks}/{total_collection}")
                self.log_info(f"Total Completed Collections: {total_passed_tasks}/{total_collection}")

                grand_total_duration = time.strftime("%H:%M:%S", time.gmtime(grand_total_seconds))

                # Update Task into database
                # update task
                task.task_end_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task.task_duration=duration
                upd_task_status = operation_db_instance.update_operation_detail(OperationDetail=task)

                # Update master info into database
                operation_db_instance.operation_master.total_duration = grand_total_duration
                operation_db_instance.operation_master.total_passed_tasks = total_passed_tasks
                upd_operation_status = operation_db_instance.update_operation_master()

                print("****************************************************************************")
                self.log_info("********************************************************************")

            # Grand Totol Duration
            grand_total_duration = time.strftime("%H:%M:%S", time.gmtime(grand_total_seconds))
            print(f"Total Elapse Duration: {grand_total_duration}")
            self.log_info(f"Total Elapse Duration: {grand_total_duration}")

            # Update operation into Database
            operation_db_instance.operation_master.end_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            operation_db_instance.operation_master.total_duration = grand_total_duration
            operation_db_instance.operation_master.operation_status = "Completed"
            operation_db_instance.operation_master.total_passed_tasks = total_passed_tasks
            
            upd_operation_status = operation_db_instance.update_operation_master()

            #Final Notication
            notification_instance.single_notification()

            return True
        except Exception as e:
            notification_instance.single_notification()
            print(f"Error: {e}")
            self.log_error(f"Error: {e}")
            return None
        
