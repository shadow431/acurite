#CMD [ "rtl_433","-v", "-R", "40", "-F", "syslog:sdr_relay:1433" ] # 40 is the device ID for the Acurite 5n1 just print it out and see what it is and send it to the relay
#CMD [ "rtl_433","-v", "-R", "40", "-d", "0", "-F", "syslog:sdr_relay:1433" ] # 40 is the device ID for the Acurite 5n1 just print it out and see what it is and send it to the relay
#CMD [ "rtl_433","-v", "-f", "433.92M", "-f", "915M", "-H", "120", "-F", "syslog:sdr_relay:1433", "-F", "log", "-F", "kv" ] # 40 is the device ID for the Acurite 5n1 just print it out and see what it is and send it to the relay
#CMD [ "rtl_433","-v", "-R", "40", "-F"  ] # 40 is the device ID for the Acurite 5n1 just print it out and see what it is

#ENV DEVICE_PROTOS=40
#ENV DEVICE_ID=0
#ENV FREQUENCY=915M

IFS=';'
PROTOS=$DEVICE_PROTOS
FREQ=$FREQUENCY
r_values=''

echo 0 > /sys/module/usbcore/parameters/usbfs_memory_mb

for r in $PROTOS
do
  r_values="${r_values}-R ${r}"
done

f_values=''
for f in $FREQ
do
  f_values="${f_values}-f ${f}"
done

echo "R Values: ${r_values}"
echo "Device ID: ${DEVICE_ID}"

#rtl_433 -Y classic -s 250k -v ${f_values} ${r_values} -d ${DEVICE_ID} -F syslog:sdr_relay:1433 -F log
#rtl_433 -Y classic -s 250k -v ${f_values} ${r_values} -F syslog:sdr_relay:1433 -F log
rtl_433 -Y classic -s 250k -v ${f_values} ${r_values} -F syslog:sdr_relay:1433 -F log -Y autolevel -Y minmax -Y magest -M level -M noise -M time:usec
