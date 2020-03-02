#/*
# * Licensed to the OpenAirInterface (OAI) Software Alliance under one or more
# * contributor license agreements.  See the NOTICE file distributed with
# * this work for additional information regarding copyright ownership.
# * The OpenAirInterface Software Alliance licenses this file to You under
# * the OAI Public License, Version 1.1  (the "License"); you may not use this file
# * except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.openairinterface.org/?page_id=698
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *-------------------------------------------------------------------------------
# * For more information about the OpenAirInterface (OAI) Software Alliance:
# *      contact@openairinterface.org
# */
#---------------------------------------------------------------------

import os
import re
import sys

def GenerateSpgwcConfigurer(s11c_name, sxc_name):
	spgwcFile = open('./spgwc-cfg.sh', 'w')
	spgwcFile.write('#!/bin/bash\n')
	spgwcFile.write('\n')
	spgwcFile.write('cd /home/scripts\n')
	spgwcFile.write('\n')
	spgwcFile.write('ifconfig lo:s5c 127.0.0.15 up\n')
	spgwcFile.write('ifconfig lo:p5c 127.0.0.16 up\n')
	spgwcFile.write('\n')
	spgwcFile.write('INSTANCE=1\n')
	spgwcFile.write('PREFIX=\'/usr/local/etc/oai\'\n')
	spgwcFile.write('\n')
	spgwcFile.write('MY_APN=\'apn.oai.svc.cluster.local\'\n')
	spgwcFile.write('MY_PRIMARY_DNS=\'192.168.18.129\'\n')
	spgwcFile.write('MY_SECONDARY_DNS=\'8.8.4.4\'\n')
	spgwcFile.write('\n')
	spgwcFile.write('mkdir -p $PREFIX\n')
	spgwcFile.write('cp etc/spgw_c.conf  $PREFIX\n')
	spgwcFile.write('\n')
	spgwcFile.write('declare -A SPGWC_CONF\n')
	spgwcFile.write('\n')
	spgwcFile.write('SPGWC_CONF[@INSTANCE@]=$INSTANCE\n')
	spgwcFile.write('SPGWC_CONF[@PREFIX@]=$PREFIX\n')
	spgwcFile.write('SPGWC_CONF[@PID_DIRECTORY@]=\'/var/run\'\n')
	spgwcFile.write('SPGWC_CONF[@SGW_INTERFACE_NAME_FOR_S11@]=\'' + s11c_name + '\'\n')
	spgwcFile.write('SPGWC_CONF[@SGW_INTERFACE_NAME_FOR_S5_S8_CP@]=\'lo:s5c\'\n')
	spgwcFile.write('SPGWC_CONF[@PGW_INTERFACE_NAME_FOR_S5_S8_CP@]=\'lo:p5c\'\n')
	spgwcFile.write('SPGWC_CONF[@PGW_INTERFACE_NAME_FOR_SX@]=\'' + sxc_name + '\'\n')
	spgwcFile.write('SPGWC_CONF[@DEFAULT_DNS_IPV4_ADDRESS@]=$MY_PRIMARY_DNS\n')
	spgwcFile.write('SPGWC_CONF[@DEFAULT_DNS_SEC_IPV4_ADDRESS@]=$MY_SECONDARY_DNS\n')
	spgwcFile.write('SPGWC_CONF[@DEFAULT_APN@]=$MY_APN\n')
	spgwcFile.write('\n')
	spgwcFile.write('for K in "${!SPGWC_CONF[@]}"; do \n')
	spgwcFile.write('  egrep -lRZ "$K" $PREFIX | xargs -0 -l sed -i -e "s|$K|${SPGWC_CONF[$K]}|g"\n')
	spgwcFile.write('  ret=$?;[[ ret -ne 0 ]] && echo "Tried to replace $K with ${SPGWC_CONF[$K]}"\n')
	spgwcFile.write('done\n')
	spgwcFile.close()

def GenerateSpgwuConfigurer():

#-----------------------------------------------------------
# Usage()
#-----------------------------------------------------------
def Usage():
	print('----------------------------------------------------------------------------------------------------------------------')
	print('generateConfigFiles.py')
	print('   Prepare a bash script to be run in the workspace where either SPGW-C and/or SPGW-U are being built.')
	print('   That bash script will copy configuration template files and adapt to your configuration.')
	print('----------------------------------------------------------------------------------------------------------------------')
	print('Usage: python3 generateConfigFiles.py [options]')
	print('  --help  Show this help.')
	print('------------------------------------------------------------------------------------------------- SPGW-C Options -----')
	print('  --kind=SPGW-C')
	print('  --s11c=[SPGW-C S11 Interface Name]')
	print('  --sxc=[SPGW-C SX Interface Name]')
	print('------------------------------------------------------------------------------------------------- SPGW-U Options -----')
	print('  --kind=SPGW-U')
	print('  --sxc=[SPGW-C SX IP address]')
	print('  --sxu=[SPGW-U SX Interface Name]')

argvs = sys.argv
argc = len(argvs)
cwd = os.getcwd()

kind = ''
s11c = ''
sxc = ''
sxu = ''

while len(argvs) > 1:
	myArgv = argvs.pop(1)
	if re.match('^\-\-help$', myArgv, re.IGNORECASE):
		Usage()
		sys.exit(0)
	elif re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-kind=(.+)$', myArgv, re.IGNORECASE)
		kind = matchReg.group(1)
	elif re.match('^\-\-s11c=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-s11c=(.+)$', myArgv, re.IGNORECASE)
		s11c = matchReg.group(1)
	elif re.match('^\-\-sxc=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-sxc=(.+)$', myArgv, re.IGNORECASE)
		sxc = matchReg.group(1)
	elif re.match('^\-\-sxu=(.+)$', myArgv, re.IGNORECASE):
		matchReg = re.match('^\-\-sxu=(.+)$', myArgv, re.IGNORECASE)
		sxu = matchReg.group(1)
	else:
		Usage()
		sys.exit('Invalid Parameter: ' + myArgv)

if kind == '':
	Usage()
	sys.exit('missing kind parameter')

if kind == 'SPGW-C':
	if s11c == '':
		Usage()
		sys.exit('missing S11 Interface Name on SPGW-C container')
	elif sxc == '':
		Usage()
		sys.exit('missing SX Interface Name on SPGW-C container')
	else:
		GenerateSpgwcConfigurer(s11c, sxc)
		sys.exit(0)

if kind == 'MME':
	if mme_s6a_IP == '':
		Usage()
		sys.exit('missing MME S6A IP address')
	elif hss_s6a_IP == '':
		Usage()
		sys.exit('missing HSS S6A IP address')
	else:
		GenerateMMEConfigurer(mme_s6a_IP, hss_s6a_IP)
		sys.exit(0)
