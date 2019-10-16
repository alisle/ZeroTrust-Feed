from OTXv2 import OTXv2Cached, IndicatorTypes
import logging
import os
import json

logging.basicConfig(level=logging.INFO)

API_KEY = os.getenv("OTX_API_KEY")
OUTPUT_FILE = os.getenv("RULES_FILE")

otx = OTXv2Cached(API_KEY)

otx.update()

pulses = otx.getall()

domains = []
hostnames = []
metadata = []

for i in pulses:
	id = i['id']
	description = i['description']
	name = i['name']
	references = i['references']
	created = i['created']
	needed = False
	for x in i['indicators']:
		if x['type'] == 'domain':
			needed = True
			domains.append( { "indicator": x['indicator'], "meta_id": id})
		elif x['type'] == 'hostname':
			needed = True
			hostnames.append( { "indicator": x['indicator'], "meta_id": id})

	if needed:
		metadata.append({
			"id": id,
			"description": description,
			"name": name,
			"references": references,
			"created": created
		})



rules = {"metadata": metadata, "domains": domains, "hostnames": hostnames}

with open(OUTPUT_FILE, 'w') as outfile:
	json.dump(rules, outfile)


