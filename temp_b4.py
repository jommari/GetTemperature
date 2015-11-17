from azure.storage.blob import BlobService 
import time

while True:
    try:
        f = open('/sys/bus/w1/devices/28-031561b266ff/w1_slave', 'r') #open file and store to 'f'
		#converts file into a list
        list1 = list(f)
        list2 = list(list1[1])

        #creates a list of numbers and adds decimal to the right place
		temperature = list2[29:]
        del temperature[len(temperature)-1]
        temperature.insert(len(temperature)-3,'.')
		
		#converts list back to a string
        tempAsFloat = "".join(temperature)
        print tempAsFloat #prints temperature
		
        #required functions for sending temperature to azure cloud. account_name='blobs name', account_key='blobs key'
        blob_service = BlobService(account_name='subziren', account_key='xdCHRGPpyq5fj85ULW3Zf8sqMwHQr/FMSFfYI1oaECEtK6znbhRapkd3ec+dxsgZ2iMYco60XeZYZof9ZndsQw==')
        #creates a container 'temperature'
        blob_service.create_container('temperature')
        #changes container permissions
        blob_service.set_container_acl('temperature', x_ms_blob_public_access='container')
        #'containers name', 'name of file sent/created to blob', 'name of variable or file path to file', 'BlockBlob'
        blob_service.put_blob('temperature', 'temperature', tempAsFloat, 'BlockBlob')
        time.sleep(10) #loops every 10 seconds to update temperature data in azure
    except:
        pass

f.close() #closes the opened temperature file
