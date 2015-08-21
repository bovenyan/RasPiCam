import subprocess
import heatmap_rpideploy as heatmap
import pickle
import restAPI
import time
import thread


def collect_proc(command_str, dev_id, pic_file_path,
                 remote_addr, remote_port, clf):
    """ Function for multi-threading to process both cameras simultaneously"""
    rAPI = restAPI.restAPI(remote_addr, remote_port)

    while True:
        prevTime = round(time.time() * 1000)

        # take picture
        subprocess.call(command_str, shell=True)  # csi camera

        # collect heatmap
        hm_data = heatmap.heatMap_proc(pic_file_path,
                                       dev_id, 1, clf)  # csi camera

        # Post data to remote server
        rAPI.post_heatmap(dev_id, hm_data)

        # wait for the next sampling instant
        curTime = round(time.time() * 1000)
        if (curTime - prevTime < sample_freq):
            time.sleep(sample_freq - (curTime - prevTime)/1000)


remote_addr = "192.168.0.105"  # for testing
remote_port = "8080"
sample_freq = 60
device_id = [1, 2]

clfMode = False
clf = None

"""Parse and Apply Configurations"""
f = open("./config", 'r')   # Read configuration

for line in f.readlines():
    temp = line.split("\t")

    if (temp[0] == "RemoteIP"):
        remote_addr = temp[1][:-1]

    if (temp[0] == "RemotePort"):
        remote_port = temp[1][:-1]

    if (temp[0] == "SampleFreq"):
        sample_freq = int(temp[1][:-1])

    if (temp[0] == "DeviceID"):
        sub_temp = temp[1][:-1].split(" ")
        device_id[0] = int(sub_temp[0])
        device_id[1] = int(sub_temp[1])

    if (temp[0] == "CLFmode" and temp[1] == "yes"):
        f1 = open('body_classifier', 'rb')
        clf = pickle.load(f1)
        f1.close()

f.close()


time.sleep(5)  # wait for other initialization
print "Program Running"

file_path_csi = "to_proc_csi.jpg"
file_path_usb = "to_proc_usb.jpg"

command_str_csi = "raspistill -w 1080 -h 1920 \
    -q 75 -t 200 -awb auto -n \
    -o " + file_path_csi  # csi cammera

command_str_usb = "fswebcam -d /dev/video0 \
    -r 1920x1080 --no-banner \
    --delay 0.2 --quiet --jpeg 75 " + file_path_usb  # usb camera

try:
    thread.start_new_thread(collect_proc, (command_str_csi, device_id[0],
                                           file_path_csi, remote_addr,
                                           remote_port, clf, ))
    thread.start_new_thread(collect_proc, (command_str_usb, device_id[1],
                                           file_path_usb, remote_addr,
                                           remote_port, clf, ))
except:
    print "Thread Cannot Be Started!! "

while(1):
    pass
