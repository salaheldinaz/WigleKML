#!/usr/bin/python
import simplekml
import json
import sys
import getopt

'''
Author: Salaheldinaz
Description : Convert Wigle.net json result file to Kml. So it can be used in Google earth.
usage: main.py -i <inputfile> -u <icon_url>
'''


def main(argv):
    inputfile = ''  # .json
    iconurl = 'https://www.iconfinder.com/icons/1249982/download/png/512'
    outputfile = ''  # .kml
    try:
        opts, args = getopt.getopt(argv, "hi:u:", ["inputfile=", "iconurl="])
    except getopt.GetoptError:
        print('wiglej2k.py -i <inputfile> -u <icon_url>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('wiglej2k.py -i <inputfile> -u <iconurl>')
            sys.exit()
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
            outputfile = str(arg).replace('json', 'kml')
        elif opt in ("-u", "--iconurl"):
            iconurl = arg

    if inputfile:
        with open(inputfile) as json_file:
            json_data = json.load(json_file)

        # Create KMl file
        kml_data = simplekml.Kml()
        kml_data.document.name = outputfile.replace('.kml', '')
        devices_collection = kml_data.newfolder(name="Devices")
        sharedstyle = simplekml.Style()
        sharedstyle.iconstyle.icon.href = iconurl

        count = 0
        print(f'Parsing Devices:')
        for device in json_data["results"]:
            name = device['ssid']
            latitude = device["trilat"]
            longitude = device["trilong"]
            description = ''
            for key, value in device.items():
                description += f'{key}: {value}\n'

            print(f'{name} at {longitude}, {latitude}')

            pnt = devices_collection.newpoint(name=name, description=description, coords=[(longitude, latitude)])
            pnt.style = sharedstyle
            count += 1

        print(f'Added {count} devices to KML file {outputfile}.')
        kml_data.save(outputfile)
    else:
        print('Please select input file using -i <inputfile>')
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
