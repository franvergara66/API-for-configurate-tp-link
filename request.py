from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
import requests
import base64
import json
import re


class RouterConfig(object):

    def change_simcard(self, isp_code, username='entelpcs', country_code=42,
                       passwd='entelpcs', apn='imovil.entelpcs.cl',
                       dial_num='*99'):
        params = {'selloc': country_code,
                  'isp': isp_code,
                  'username': username,
                  'passwd': passwd,
                  'apn': apn,
                  'linktype': 2,
                  'authtype': 0,
                  'dial_num': dial_num,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/MobileCfgRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/MobileCfgRpm.htm'
        return url_petition, params, url_refer

    def port_configuration(self, ex_port, in_port, ip_address):
        if not in_port:
            in_port = ex_port

        params = {'ExPort': ex_port,
                  'InPort': in_port,
                  'Ip': ip_address,
                  'Protocol': 1,
                  'State': 1,
                  'Commonport': 0,
                  'Changed': 0,
                  'SelIndex': 0,
                  'Page': 1,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/VirtualServerRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/VirtualServerRpm.htm?Add=Add&Page=1'
        return url_petition, params, url_refer

    def dynamic_dns(self, user_noip='user@email.com', passwd_noip='your_password',
                    cabina='00'):
        cliUrl = 'your_no_ip_id'+str(cabina)+'.ddns.net'
        params = {'provider':  3,
                  'username':  user_noip,
                  'pwd': passwd_noip,
                  'cliUrl': cliUrl,
                  'EnDdns': 2,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/NoipDdnsRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/DdnsAddRpm.htm?provider=3'
        return url_petition, params, url_refer

    def address_reservation(self, mac_address, dir_ip, state=1, changed=0,
                            selindex=0, page=1):
        params = {'Mac': mac_address,
                  'Ip': dir_ip,
                  'State': state,
                  'Changed': changed,
                  'SelIndex': selindex,
                  'Page': page,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/FixMapCfgRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/FixMapCfgRpm.htm?Add=Add&Page=1'
        return url_petition, params, url_refer

    def reboot_router():
        params = {'Reboot': 'Reboot'}
        url_petition = 'http://192.168.0.1/userRpm/SysRebootRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/SysRebootRpm.htm'
        return url_petition, params, url_refer

    def change_password(self, newname, newpassword, newpassword2,
                        oldname='admin', oldpassword='admin',
                        ):
        params = {'oldname': oldname,
                  'oldpassword': oldpassword,
                  'newname': newname,
                  'newpassword': newpassword,
                  'newpassword2': newpassword2,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/ChangeLoginPwdRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/ChangeLoginPwdRpm.htm'
        return url_petition, params, url_refer

    def dhcp_settings(self, activate_dhcp=1, start_ip='192.168.0.110',
                      end_ip='192.168.0.112', lease_time=30,
                      gateway='192.168.0.1', default_domain='',
                      primary_dns='0.0.0.0', secondary_dns='0.0.0.0'):

        params = {'dhcpserver': activate_dhcp,
                  'ip1': start_ip,
                  'ip2': end_ip,
                  'Lease': lease_time,
                  'gateway': gateway,
                  'domain': default_domain,
                  'dnsserver': primary_dns,
                  'dnsserver2': secondary_dns,
                  'Save': 'Save'
                  }
        url_petition = 'http://192.168.0.1/userRpm/LanDhcpServerRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/LanDhcpServerRpm.htm'
        return url_petition, params, url_refer

    def internet_access(self, connection_mode=0):
        params = {
            'connmode': connection_mode,
            'Save': 'Save'
        }
        url_petition = 'http://192.168.0.1/userRpm/ConnModeCfgRpm.htm'
        url_refer = 'http://192.168.0.1/userRpm/ConnModeCfgRpm.htm'
        return url_petition, params, url_refer

    def send_petition(self, user, passwd, **kwargs):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        auth_key = str(
            base64.b64encode(bytes(user+':'+passwd, 'utf-8')), 'utf-8')
        headers = {'User-Agent': user_agent,
                   'Authorization': auth_key,
                   'Referer': ''
                   }
        url_petition, params, url_refer = self.reboot_router()
        r = requests.get(url_petition, headers=headers, params=params)

    def get_mac_adress_router(self, ip_address='192.168.0.1'):
        pid = Popen(["arp", "-n", ip_address], stdout=PIPE)
        arp_result = (pid.communicate()[0]).decode('utf-8')
        router_mac_address = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})",
                                       arp_result)
        router_mac_address = router_mac_address.groups()[0].upper().replace(
            ":", "")
        return router_mac_address

    def get_brand_router(self, ip_address='192.168.0.1'):
        vendor_router = 'Marca no identificada'
        try:
            mac_address = (self.get_mac_adress_router(ip_address))
            macOUI = mac_address[:6]
            json_file = open("vendors.json", "r")
            json_data = json.load(json_file)
            if json_data.get(macOUI):
                vendor_router = json_data.get(macOUI)
            return vendor_router
        except Exception as e:
            return 'Error: Conexion no posible con el router'

    def get_model_router(self, user, passwd, ip_address='192.168.0.1'):
        model_router = 'Modelo no identificado'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        try:
            url_petition = 'http://192.168.0.1/userRpm/StatusRpm.htm'
            url_refer = 'http://192.168.0.1/userRpm/MenuRpm.htm'
            auth_key = str(
                base64.b64encode(bytes(user+':'+passwd, 'utf-8')), 'utf-8')
            headers = {'User-Agent': user_agent,
                       'Authorization': auth_key,
                       'Referer': url_refer
                       }
            r = requests.get(url_petition, headers=headers)
            doc = r.text
            soup = BeautifulSoup(''.join(doc), "html.parser")
            titleTag = (soup.html.head.title).string
            if titleTag:
                model_router = titleTag
            return model_router
        except Exception as e:
            return 'Error: Conexion nsso posible con el router'

test = RouterConfig()
print(test.get_brand_router(), test.get_model_router('admin', 'admin'))
