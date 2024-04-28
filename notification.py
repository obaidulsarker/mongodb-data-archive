import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from logger import *
from setting import get_variables
from operationdb import read_operation_db
from email_template_generation import email_template

class notification(Logger):
    def __init__(self, logfile):
        super().__init__(logfile)
        self.pid_file=get_variables().PID_FILE
        self.opt_log_file = get_variables().LOG_FILE
        self.notification_interval = get_variables().NOTIFICATION_INTERVAL_HOUR
        self.smtp_server = get_variables().SMTP_SERVER
        self.smtp_username = get_variables().SMTP_LOGIN_USERNAME
        self.smtp_password = get_variables().SMTP_LOGIN_PASSWORD
        self.smtp_port = get_variables().SMTP_PORT
        self.sender_email_address = get_variables().SENDER_EMAIL
        # self.sender_email_password = get_variables().SENDER_EMAIL_PASSWORD
        self.receiver_email_address = get_variables().RECEEIVER_EMAIL.split(",")
        self.tls_enabled = get_variables().TLS_ENABLED
        self.password_auth_enabled = get_variables().EMAIL_PASS_AUTH_ENABLED
        self.email_subject = get_variables().EMAIL_SUBJECT

    # Return PID
    def get_pid(self):
        try:
            pid = None
            # Open the file in read mode
            with open(self.pid_file, 'r') as file:
                pid = file.read()

            if len(pid.strip())==0:
                pid=None

            return pid
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None

    # Return Operation Log
    def get_log_file(self):
        try:
            log_file_path = None
            # Open the file in read mode
            with open(self.opt_log_file, 'r') as file:
                log_file_path = file.read()

            if len(log_file_path.strip())==0:
                log_file_path=None

            return log_file_path
        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}")
            return None    

    def send_email(self, subject, body):
        status = False

        for receiver_email in self.receiver_email_address:
            try:
                # Email configuration
                sender_email = self.sender_email_address
                
                # Create the email content
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message.attach(MIMEText(body, "html"))
                
                #print("Started-1")
                # Connect to the SMTP server (Gmail, in this case)
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:

                    # If TLS is enabled in SMTP Server
                    if self.tls_enabled=="YES":
                        server.starttls()

                    #print("Started-2")

                    # If password authentication is enabeld in SMTP Server
                    if self.password_auth_enabled=="YES":
                        server.login(self.smtp_username, self.smtp_password)

                    #print("Started-3")

                    server.sendmail(sender_email, receiver_email, message.as_string())

                    #print("Started-4")

                status = True
            except Exception as e:
                print(f"Exception: {str(e)}")
                self.log_error(f"Exception: {str(e)}")
                status = False
        return status
    
    # Get Email Body
    def get_email_body(self, pid):
        try:
            if len(pid)<=0:
                raise Exception("PID is not found!")
            
            # get operation info
            operation_db = read_operation_db(operation_id=pid)
            operation_master_data = operation_db.read_operation_master()
            operation_detail_data = operation_db.read_operation_detail()

            #print(operation_detail_data)
            print(f"Total Duration: {operation_master_data[0].total_duration}")
            print(f"Task Passed: {operation_master_data[0].total_passed_tasks}")

            # email template instance
            template = email_template(
                logfile=self.log_file,
                operation_id=operation_master_data[0].operation_id,
                operation_start_datetime=operation_master_data[0].start_datetime,
                operation_end_datetime=operation_master_data[0].end_datetime,
                operation_status=operation_master_data[0].operation_status,
                total_task = operation_master_data[0].total_tasks,
                completed_tasks=operation_master_data[0].total_passed_tasks,
                total_duration=operation_master_data[0].total_duration,
                task_list=operation_detail_data
            )

            #print("Templated")

            return template.get_email_body()
        
        except Exception as e:
            print(f"Exception: {str(e)}")  
            self.log_error(f"Exception: {str(e)}")
            return None  

    # Notify until job completion
    def start_notification(self):
        try:
            # Convert Hour into Seconds
            interval_seconds = int(self.notification_interval) * 60 * 60

            email_subject = self.email_subject
            receiver_email = self.receiver_email_address
            
            # Sleep 2 Minutes
            time.sleep(120)
            pid = self.get_pid()

            print(f"pid: {pid}")
            self.log_info(f"pid: {pid}")
            
            while (pid != None):
                email_body = self.get_email_body(pid)
                email_status = self.send_email( subject=email_subject, body=email_body)
                print(f"email_status={email_status}")
                if (email_status):
                    self.log_info(f"Email Subject: {email_subject}")
                    self.log_info(f"Email Recipient: {receiver_email}")
                    self.log_info("****************** EMAIL BODY ****************************************")
                    self.log_info(email_body)
                    print("Email is sent.")
                    self.log_info("Email is sent.")
                else:
                    print("Unable to send email!")
                    self.log_error("Unable to send email!")
                
                # Read PID
                pid = self.get_pid()
                print(f"pid: {pid}")
                self.log_info(f"pid: {pid}")

                # wait for next notification
                if pid !=None:
                    #time.sleep(30)
                    time.sleep(interval_seconds)

        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}") 

    # Notify until job completion
    def single_notification(self):
        try:
            email_subject = self.email_subject
            receiver_email = self.receiver_email_address
            
            # Sleep 2 Minutes
            time.sleep(120)
            pid = self.get_pid()

            print(f"pid: {pid}")
            self.log_info(f"pid: {pid}")
            
            email_body = self.get_email_body(pid)

            if (pid != None):
                
                email_status = self.send_email( subject=email_subject, body=email_body)
                if (email_status):
                    self.log_info(f"Email Subject: {email_subject}")
                    self.log_info(f"Email Recipient: {receiver_email}")
                    self.log_info("****************** EMAIL BODY ****************************************")
                    self.log_info(email_body)
                    print("Email is sent.")
                    self.log_info("Email is sent.")
                else:
                    print("Unable to send email!")
                    self.log_error("Unable to send email!")

        except Exception as e:
            print(f"Exception: {str(e)}")
            self.log_error(f"Exception: {str(e)}") 

# if __name__ == "__main__":

#     log_file = get_variables().NOTIFICATION_LOG
#     notify = notification(logfile=log_file)
#     notify.start_notification()