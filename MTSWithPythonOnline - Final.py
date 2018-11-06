import time
time.sleep(15) 

import requests

# problem while adding Generic Device. After adding user need to go to the 
#property panel and select HFL from Drop down
#but if we load the config file with generic device in it. It works properly.

#So solution now is either load the config file with all the MOs.
#Or add generic device MO and save the config and then load the config using Auto script.


headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
MOPrpo = {"class": "GenericDevice", "name": "HFL", "instanceNumber" : 0, "properties": [ { "name": "ECU ID","value": 1607} ] }



#load the config
resp = requests.post('http://10.0.0.20/api/v1/clusters/0c22069b9bca49b6a1fa69785b4cc5de/aus/0759d2e85b8c40cca41ff793cbc8d790/openConfiguration', data='hfl110_ALL_online',headers=headers, stream=True)

#load AOE MO
#add AOE Advanced Online Evaluator
MOPrpo = {"class": "Advanced Online Evaluator", "name": "AOE", "properties": [ 
                                                                               { "name": "Ini file",
            																	 "value": "D:\DataAnalysisBox\mts_measurement\data\HFL110TA10_System_Integration_Test.tcd" 
																			   },
																			   {  "name": "Report Name", 
																			      "value": "HFLReport" 
																			   },
																			   {
																			      "name": "Report Path",
																				  "value": "D:\DataAnalysisBox\mts_measurement\data"
																			   }
																			] }
resp = requests.post('http://10.0.0.20/api/v1/clusters/0c22069b9bca49b6a1fa69785b4cc5de/aus/0759d2e85b8c40cca41ff793cbc8d790/configuration/createItem', json=MOPrpo,headers=headers)








