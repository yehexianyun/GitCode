import pymysql
db = pymysql.connect(host='localhost',
                     user='root',
                     password='mysql123456',
                     database='guba',
                     charset='utf8')

company_list = [300059,
600309,
600276,
568,
2415,
2475,
651,
601899,
2352,
601328,
2714,
300124,
2142,
1,
725,
601668,
300015,
600048,
2304,
600031,
600436,
600919,
600016,
600050,
600837,
2466,
600089,
601225,
300122,
601988,
601688,
601919,
601169,
600570,
601211,
601229,
600009,
601390,
600660,
338,
601009,
601669,
100,
600019,
600999,
600958,
776,
963,
600029,
2241,
601006,
601989,
1979,
538,
600926,
601939,
601633,
166,
601186,
601600,
768,
600233,
600015,
600383,
603993,
601111,
2074,
600188,
600085,
600115,
601877,
601788,
601117,
601800,
600741,
157,
895,
2736,
601021,
601336,
2007,
2555,
723,
603833,
69,
600674,
300033,
600332,
601878,
601155,
600362,
601898,
601998,
601216,
600606,
601966
]

for company in company_list:
    cur = db.cursor()
    sql = "CREATE TABLE IF NOT EXISTS code_600031_2 (index_id int NOT NULL AUTO_INCREMENT, guba_read varchar(10) NULL,guba_comment varchar(10) NULL,guba_date varchar(15) NULL,guba_title TEXT NULL,guba_id varchar(20) NULL,PRIMARY KEY (index_id)) engine = InnoDB "
    cur.execute(sql)
    db.commit()
    cur.close()

db.close()



















