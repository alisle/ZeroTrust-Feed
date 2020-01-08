from OTXv2 import OTXv2Cached, IndicatorTypes
from datetime import datetime
import logging
import json
import time
import boto3
from botocore.exceptions import ClientError

class Feed:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.opened = False
        self.domains = []
        self.hostnames = []
        self.metadata = []
        self.pulses = []
        self.client = boto3.client('s3')
        self.buck_name = "zero-trust-io"

    def open(self, api_key):
        if not self.opened:
            logging.info("opening OTX")
            self.otx = OTXv2Cached(api_key)
            self.opened = True
        else:
            logging.info("skipping opening because we're already opened")

    def update(self):
        logging.info("updating pulses")
        self.pulses = self.otx.getall()

        for pulse in self.pulses:
            self.process_pulse(pulse)

    def run(self, sleep_time_mins, outfile):
        logging.info("running")
        wait = sleep_time_mins * 60

        while True:
            self.update()
            self.write(outfile)
            self.upload(outfile)


            logging.info("finishing for now, sleeping for " + str(sleep_time_mins) + " mins")
            time.sleep(wait)

    def write(self, file_name):
        logging.info("writing output to file")
        with open(file_name, 'w') as outfile:
            rules = {
                "metadata": self.metadata,
                "domains": self.domains,
                "hostnames": self.hostnames
            }

            json.dump(rules, outfile)

    def upload(self, file_name):
        timestamp = datetime.now().strftime("%Y:%m:%d-%H:%M:%S")
        name_with_timestamp = "rules-{}.json".format(timestamp)

        try:
            with open(file_name, "rb") as outfile:
                logging.info("uploading " + name_with_timestamp + " to s3")
                self.client.upload_fileobj(outfile, self.buck_name, name_with_timestamp)

            copy_source = {'Bucket': self.buck_name, 'Key': name_with_timestamp}
            logging.info("copying " + name_with_timestamp + " to rules-current.json")
            self.client.copy_object(CopySource=copy_source, Bucket=self.buck_name, Key="rules-current.json")
        except ClientError as e:
            logging.error(e)



    def process_pulse(self, pulse):
        logging.info("processing pulse")

        id = pulse['id']
        description = pulse['description']
        name = pulse['name']
        references = pulse['references']
        created = pulse['created']
        needed = False

        for indicator in pulse['indicators']:
            if indicator['type'] == 'domain':
                logging.info("writing new domain indicator")
                needed = True
                self.domains.append({
                    'indicator': indicator['indicator'],
                    "metat_id": id
                })
            elif indicator['type'] == 'hostname':
                logging.info("writing new hostname indicator")
                needed = True
                self.hostnames.append({
                    'indicator': indicator['indicator'],
                    "metat_id": id
                })

        if needed:
            self.metadata.append({
                "id": id,
                "description": description,
                "name": name,
                "references": references,
                "created": created
            })

