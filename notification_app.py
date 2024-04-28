from notification import notification
from setting import get_variables
from logger import Logger

if __name__ == "__main__":
    try:

        # Nofication Log
        notification_log_file = get_variables().NOTIFICATION_LOG

        # Log Instance
        log = Logger(logfile=notification_log_file)

        print("**************************Notification service is started **********************************")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log.log_info("**************************Notification service is started **********************************")
        log.log_info("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        # Notification Instance
        notification_instance = notification(logfile=notification_log_file)
        notification_instance.start_notification()

        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("**************************Notification service is stopped ************************************")
        log.log_info("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        log.log_info("**************************Notification service is stopped *************************************")

    except Exception as e:
        print(f"Exception: {str(e)}")