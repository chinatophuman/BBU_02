from ETH_test import ETH_test
from VGA_test import VGA_test
from USB_test import USB_test
from SATA_test import SATA_test
from CPU_test import CPU_test
from Memory_test import Memory_test
from CONSOLE_test import CONSOLE_test
from PCIE_test import PCIE_test
from SSD_test import SSD_test
from SFP_test import SFP_test
from Search_SN_Maxwell import fetch_MAC
from Write_MAC import write_Mac
from Write_FRU import write_FRU
from Setting import Setting
import wx


class TestItem:
    def __init__(self, vga, mac, fru, eth, sfp, cpu, memory, console, usb, pcie, sata, m2, sn):
        self.vga = vga
        self.mac = mac
        self.fru = fru
        self.eth = eth
        self.sfp = sfp
        self.cpu = cpu
        self.memory = memory
        self.console = console
        self.usb = usb
        self.pcie = pcie
        self.sata = sata
        self.m2 = m2
        self.setting = Setting()
        self.sn = sn

    def test_vga(self):
        if self.vga:
            vga_result = VGA_test(self.setting.logname).test_content()
            print('VGA test result is %s' % vga_result)
        else:
            vga_result = 'not test'
        return vga_result

    def test_mac(self):
        if self.mac:
            mac_address = fetch_MAC(self.setting.logname, self.sn, self.setting.mysql_host, self.setting.mysql_user,
                                    self.setting.mysql_password, self.setting.mysql_database).search_db_sn()
            free_mac = fetch_MAC(self.setting.logname, self.sn, self.setting.mysql_host, self.setting.mysql_user,
                                 self.setting.mysql_password, self.setting.mysql_database).search_free_mac()
            if free_mac < 200:
                warning = wx.MessageBox('MAC地址不足，请联系上海众新补充MAC地址', 'info', wx.OK | wx.ICON_INFORMATION)
                if warning.ShowModal() == wx.ID_OK:
                    warning.Destroy()
            # print('fetch MAC address : ', Mac_address)
            if mac_address == 'No need to fetch MAC':
                with open(self.setting.logname, 'a+') as f:
                    f.write("the board is tested board, skip write MAC_address")
                write_mac_result = 'no write'
            elif mac_address == 'FAIL':
                # print("Operate mysql db error")
                write_mac_result = 'FAIL'
            else:
                write_mac_result = write_Mac(self.setting.logname, self.setting.hostname, self.setting.port,
                                             self.setting.username, self.setting.password, mac_address).test_content()
                print('Write MAC result is %s' % write_mac_result)
        else:
            write_mac_result = 'no write'
        return write_mac_result

    def test_fru(self):
        if self.fru:
            BSN = self.sn
            PSN = self.sn
            write_fru_result = write_FRU(self.setting.logname, self.setting.BMD, self.setting.BMT, BSN,
                                         self.setting.BPN, PSN, self.setting.PPN, self.setting.ProductN,
                                         self.setting.ProductV, self.setting.hostname, self.setting.port,
                                         self.setting.username, self.setting.password).write_content()
            print('Write fru info result is %s' % write_fru_result)
        else:
            write_fru_result = 'not write'
        return write_fru_result

    def test_eth(self):
        if self.eth:
            eth_result = ETH_test(self.setting.logname, self.setting.ETHPORT, self.setting.HOSTPORT,
                                  self.setting.IPMIPORT, self.setting.DEFGW, self.setting.ETHPORT_IP,
                                  self.setting.hostname, self.setting.port, self.setting.username,
                                  self.setting.password).test_content()
            print('ETH test result is %s' % eth_result)
        else:
            eth_result = 'not test'
        return eth_result

    def test_sfp(self):
        if self.sfp:
            sfp_result = SFP_test(self.setting.logname, self.setting.hostname, self.setting.port, self.setting.username,
                                  self.setting.password, self.setting.SFPPORT1, self.setting.SFPPORT2,
                                  self.setting.SFPPORT3, self.setting.SFPPORT4).test_content()
            print('SFP test result is %s' % sfp_result)
        else:
            sfp_result = 'not test'
        return sfp_result

    def test_cpu(self):
        if self.cpu:
            cpu_result = CPU_test(self.setting.logname, self.setting.buildoption_type, self.setting.hostname,
                                  self.setting.port, self.setting.username, self.setting.password).test_content()
            print('CPU test result is %s' % cpu_result)
        else:
            cpu_result = 'not test'
        return cpu_result

    def test_memory(self):
        if self.memory:
            memory_result = Memory_test(self.setting.logname, self.setting.hostname, self.setting.port,
                                        self.setting.username, self.setting.password).test_content()
            print('Memory test result is %s' % memory_result)
        else:
            memory_result = 'not test'
        return memory_result

    def test_console(self):
        if self.console:
            console_result = CONSOLE_test(self.setting.logname, self.setting.hostname, self.setting.port,
                                          self.setting.username, self.setting.password).test_content()
            print('CONSOLE test result is %s' % console_result)
        else:
            console_result = 'not test'
        return console_result

    def test_usb(self):
        if self.usb:
            usb_result = USB_test(self.setting.logname, self.setting.hostname, self.setting.port, self.setting.username,
                                  self.setting.password).test_content()
            print('USB test result is %s' % usb_result)
        else:
            usb_result = 'not test'
        return usb_result

    def test_pcie(self):
        if self.pcie:
            pcie_result = PCIE_test(self.setting.logname, self.setting.hostname, self.setting.port,
                                    self.setting.username, self.setting.password).test_content()
            print('PCIE test result is %s' % pcie_result)
        else:
            pcie_result = 'not test'
        return pcie_result

    def test_sata(self):
        if self.sata:
            sata_result = SATA_test(self.setting.logname, self.setting.hostname, self.setting.port,
                                    self.setting.username, self.setting.password).test_content()
            print('SATA test result is %s' % sata_result)
        else:
            sata_result = 'not test'
        return sata_result

    def test_m2(self):
        if self.m2:
            m2_result = SSD_test(self.setting.logname, self.setting.hostname, self.setting.port, self.setting.username,
                                 self.setting.password).test_content()
            print('M.2 test result is %s' % m2_result)
        else:
            m2_result = 'not test'
        return m2_result
