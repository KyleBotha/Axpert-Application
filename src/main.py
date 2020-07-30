import AxpertPy
from MongoDB import ConnectDB
import dotenv
import os
import threading
import time
import datetime
import random


dotenv.load_dotenv()
DB_NAME = os.getenv('DB_NAME')
DB_URI = os.getenv('DB_URI')
COMMS_PORT = os.getenv('COMMS_PORT')


def main():
    command = "QPIGS"
    print(DB_URI)
    qpigs = AxpertPy.Command(command)
    qpigs.build_command()

    inverter = AxpertPy.Connection(COMMS_PORT, "2400", qpigs.hex_command)
    inverter.establish_connection()

    db = ConnectDB(DB_URI, DB_NAME)

    def multiplier(value, multiplier):
        val = float(value)
        calc = val*multiplier
        return str(calc)

    def command_to_db():
        now = datetime.datetime.now()

        current_time = now.strftime("%H:%M:%S")

        inverter_response = inverter.send_command()
        try:
            qpigs_doc = {
                "AC_Output_Apparent_Power": multiplier(inverter_response[4], 1),
                "AC_Output_Active_Power": multiplier(inverter_response[5], 1),
                "Output_Load_Percent": inverter_response[6],
                "Battery_Voltage": inverter_response[8],
                "Battery_Charging_Current": multiplier(inverter_response[9], 1),
                "Battery_Capacity": multiplier(inverter_response[10], 1),
                "Inverter_Heat_Sink_Temperature": multiplier(inverter_response[11], 1),
                "PV_Input_Current": multiplier(inverter_response[12], 1),
                "PV_Input_Voltage": inverter_response[13],
                "Battery_Voltage_SCC1": inverter_response[14],
                "Battery_Discharge_Current": inverter_response[15],
                "PV_Charging_Power": multiplier(inverter_response[19], 1),
                "date_time": datetime.datetime.now(),
                "date": str(datetime.date.today()),
                "time": current_time
            }
        except:
            qpigs_doc = {
                "AC_Output_Apparent_Power": random.randint(220, 260),
                "AC_Output_Active_Power": 0,
                "Output_Load_Percent": 0,
                "Battery_Voltage": 0,
                "Battery_Charging_Current": 0,
                "Battery_Capacity": 0,
                "Inverter_Heat_Sink_Temperature": 0,
                "PV_Input_Current": 0,
                "PV_Input_Voltage": 0,
                "Battery_Voltage_SCC1": 0,
                "Battery_Discharge_Current": 0,
                "PV_Charging_Power": 0,
                "date_time": datetime.datetime.now(),
                "date": str(datetime.date.today()),
                "time": current_time
            }

        db.insert_one(qpigs_doc, "QPIGS")

    if(inverter.isConnected == True):
        while True:
            command_to_db()
            time.sleep(1)
    return 0


if (__name__ == '__main__'):
    main()
