-- operation definition

DROP TABLE operation;

CREATE TABLE operation(
	operation_id VARCHAR(128) NOT NULL,
	operation_log text,
	start_datetime	text NOT NULL,
	end_datetime	text,
	total_duration text,
	operation_status	VARCHAR(20) NOT NULL,
	source_database_ip VARCHAR(128) NOT NULL,
	destination_database_ip VARCHAR(20) NOT null,
	total_tasks		INTEGER NOT NULL,
	total_passed_tasks	INTEGER
);


-- operation_details definition

DROP TABLE operation_details;

CREATE TABLE operation_details(
	operation_id VARCHAR(128) NOT null,
	task_id	INTEGER,
	task_name VARCHAR(100) not null,
	task_description text not null,
	task_start_datetime text,
	task_end_datetime	text,
	task_duration text,
	task_status VARCHAR(20),	
	remarks	text,
	id_field_name text,
	ts_field_name text
);