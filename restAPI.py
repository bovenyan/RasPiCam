import json
import requests
import logging


class restAPI():
    """ REST API class
    translate features that needs to be uploaded to rest requests
    """

    def __init__(self, addr, port):
        """ Configure the remote ip address from conf_file"""
        self.remote_addr = addr
        self.remote_port = port

        # logging configuration
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] \
                            %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='./log/RESTerror.log',
                            filemode='a')

    def post_heatmap(self, device_id, heatmap_res):
        """ Posting the local json string to remote_conf """

        payload = {"device_id": device_id, "count": heatmap_res["count"],
                   "heat_map": heatmap_res["heat_map"]}
        url = "http://" + self.remote_addr + ":" + self.remote_port + \
            "/api/info/store?client_id=asdf&name=liu&time=now"

        # Try connecting to the server for 3 sec, otherwise log errors
        try:
            requests.post(url, data=json.dumps(payload),
                          headers={"content-type": "application/json"},
                          timeout=5)
            print json.dumps(payload)
        except requests.exceptions.Timeout as e:
            logging.error(" ERROR Connecting to the server !")
        except requests.exceptions.HTTPError as e:
            logging.error(e.message)
