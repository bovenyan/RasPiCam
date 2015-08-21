#!/bin/bash
device_id=0
cam_id=1
while true; do
	Date=$(date +"%d_%H%M%S")
	file_name=USBCamCapture.$Date.jpg
	fswebcam -d /dev/video1 -r 1920x1080 --no-banner --delay 5 --quiet --jpeg 75 $file_name
	python heatmap_rpideploy.py $file_name $device_id $cam_id
done