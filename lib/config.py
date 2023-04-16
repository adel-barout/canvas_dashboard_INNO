from datetime import datetime
import pytz

API_URL = "https://canvas.hu.nl/"
timezone = pytz.timezone("Europe/Amsterdam")
actual_date = datetime.now()
start_date = datetime.strptime('06-02-23', '%d-%m-%y')
end_date = datetime.strptime('26-06-23', '%d-%m-%y')
actual_day = (actual_date - start_date).days
not_graded = "Nog niet beoordeeld."
plot_path = "./dashboard - lokaal/plotly/"


group_names = {
    61406: "TEAM",
    62667: "GILDE",
    63004: "Peilmomenten",
    62149: "AI",
    62903: "BIM",
    61719: "CSC",
    61367: "SD_B",
    62609: "SD_F",
    62138: "TI",
}

score_tabel = {0: "Geen voortgang", 1: "Onvoldoende voortgang", 2: "Voldoende voortgang", 3: "Goede voortgang"}

roles = {"AI": "AI",
         "BIM": "BIM",
         "CSC-B": "CSC",
         "CSC-C": "CSC",
         "SD-C-Back-End": "SD_B",
         "SD-D-Front-End": "SD_F",
         "SD-AB-Back-End-Verlenger": "SD_B",
         "TI": "TI",
         "Innovation 1": "INNO"
         }

def get_role(name):
    if roles.get(name):
        return roles[name]
    else:
        return ""

def getDateTimeObj(dateTimeStr):
    dateTimeObj = datetime.strptime(dateTimeStr, '%Y-%m-%dT%H:%M:%S.%f%z')
    dateTimeObj = dateTimeObj.astimezone(timezone)
    return dateTimeObj

def str_date_to_day(actual_date_str):
    if actual_date_str != None:
        actual_date = datetime.strptime(actual_date_str, '%Y-%m-%dT%H:%M:%SZ')
    else:
        actual_date = datetime.strptime("2023-02-14", '%Y-%m-%d')
    return (actual_date - start_date).days
