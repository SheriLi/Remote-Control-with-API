

import requests
import json

header = {'Content-type': 'application/json', 'Accept': 'text/plain'}


class ClusterInformation(object):
    def __init__(self, cluster_url, analysis_units_links_href, links_href, recording_units_link_href):
        self.cluster_url = cluster_url
        self.analysis_units_links_href = analysis_units_links_href
        self.links_href = links_href
        self.recording_units_link_href = recording_units_link_href

    def get_cluster_information(self):
        try:
            status = requests.get(self.cluster_url)
            href = ""
            if status.status_code == 200:
                data = json.loads(status.text)
                for href in data:
                    self.analysis_units_links_href = href['analysisUnits'][0]['links'][0]['href']
                    print("get_cluster_information analysis units links href return cluster information.")
                    print(self.analysis_units_links_href)
                    self.links_href = href['links'][0]['href']
                    print("get_cluster_information links_href return cluster information.")
                    print(self.links_href)
                    self.recording_units_link_href = href['recordingUnits'][0]['links'][0]['href']
                    print("get_cluster_information recording units links_href return cluster information.")
                    print(self.recording_units_link_href)

            else:
                print("get_cluster_information doesn't return cluster information.")
                print(status.text)
            return status
        except:
            printexception()

    def post_load_mts_configuration(self, mts_configuration):
        try:
            if mts_configuration != "" & self.cluster_url != "":
                url = self.cluster_url + "/openConfiguration"
                status = requests.post(url, data=mts_configuration, headers=header, stream=True)
                data = status.text
                if status.status_code == 200:
                    print("post_load_mts_configuration load the configuration into MTS.")
                    print(status.text)
                else:
                    print("post_load_mts_configuration doesn't load the configuration into MTS.")
                    print(status.text)
            return status
        except:
            printexception()

    def post_load_mo(self, mo_prop):
        try:
            if mo_prop != "" & self.cluster_url != "":
                url = self.cluster_url + "/configuration/createItem"
                status = requests.post(url, json=mo_prop, headers=header, stream=True)
                if status.status_code == 200:
                    print("post_load_mo load the measurement object into MTS.")
                    print(status.text)
                else:
                    print("post_load_mo doesn't load the measurement object into MTS.")
                    print(status.text)
            return status
        except:
            printexception()

    def post_start_recording(self, trigger_information):
        try:
            if trigger_information != "" & self.recording_units_link_href != "":
                url = self.recording_units_link_href + "/startRecording"
                status = requests.post(url, json=trigger_information, headers=header, stream=True)
                if status.status_code == 200:
                    print("post_start_recording has started the recording.")
                    print(status.text)
                else:
                    print("post_start_recording hasn't started the recording..")
                    print(status.text)
            return status
        except:
            printexception()

    def post_stop_recording(self):
        try:
            url = self.recording_units_link_href + "/stopRecording"
            status = requests.post(url)
            if status.status_code == 200:
                print ("Recording has been stopped")
                print (status.text)
            else:
                print ("Recording has not been stopped")
                print (status.text)
            return status
        except:
            printexception()

    def post_create_marker(self, marker_information):
        try:
            if self.recording_units_link_href != "" & marker_information != "":
                url = self.recording_units_link_href + "/setMarker"
                status = requests.post(url,json=marker_information, headers=header, stream=True)
                if status.status_code == 200:
                    print ("Marker has been set")
                    print (status.text)
                else:
                    print ("Marker hasn't been set")
                    print (status.text)
            return status
        except:
            printexception()


import linecache


def printexception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


def main(argv):
    #ip address should be the machine where mts tool is running in silent mode
    ip_address = ""

    if len(argv) > 0:
        for arg in argv:
            key, value = arg.split('=')
            if key == '-h':
                print("python.exe [mtsonlineremotecontrol.py] [-ip=] \n")
                print("Before running the script. Please make sure MTS tool is running in silent mode \n")
                print("Run below command into DOS prompt \n")
                print("measapp.exe -enable-remote-control \n")
                sys.exit()
            if key == 'ip':
                ip_address = value
            else:
                print("Invalid Parameter. Please check the help by using -h token \n")
                sys.exit()

        cluster_url = "http://$$$$$/api/v1/clusters"
        try:
            if ip_address != "":
                cluster_url = cluster_url.replace("$$$$$", ip_address)
                analysis_units_links_href = ""
                links_href = ""
                recording_units_link_href = ""
                cluster_information_object = ClusterInformation (cluster_url, analysis_units_links_href,
                                                                links_href, recording_units_link_href)

                status = cluster_information_object.get_cluster_information()
                if status.status_code == 200:
                    #below information can be filled by user as per the need.
                    #I am not sure on what basis start trigger recording trigger will call
                    trigger_information = {}
                    trigger_information['description'] = ""
                    trigger_information['preTriggerTime'] = 0
                    trigger_information['filePath'] = ""
                    status = cluster_information_object.post_start_recording(trigger_information)
                    if status.status_code == 200:
                        #need to get the information about the trigger
                        marker_information = {}
                        marker_information['description'] = ""
                        marker_information['postTriggerTime'] = 0
                        status = cluster_information_object.post_create_marker(marker_information)
                        if status.status_code == 200:
                            status = cluster_information_object.post_stop_recording()
                            #if status.status_code == 200:
        except:
            printexception()
    else:
        print("User has to give ip address as a parameter. Please use help -h.")


import sys
if __name__ == '__main__':
    main(sys.argv[1:])










