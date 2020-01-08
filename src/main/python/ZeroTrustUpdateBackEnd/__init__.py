from OTXv2 import OTXv2Cached, IndicatorTypes
import logging
import json
import time
import os
import boto3


class Feed:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.opened = False
        self.domains = []
        self.hostnames = []
        self.metadata = []
        self.pulses = []
        self.client = boto3.client('s3')

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
        logging.info("uploading rules to s3")
        with open(file_name, "rb") as outfile:
            self.client.upload_fileobj(outfile, "zero-trust-io", "rules.json.updated")

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

