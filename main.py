#!/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------
import time
import wx
import subprocess
from Verify_SN import Verify_SN
from Setting import Setting
from Test_item import TestItem

value2 = ''


class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(720, 50), size=(1080, 720))
        self.Bind(wx.EVT_CLOSE, self.close_frame)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        # self.Bind(wx.EVT_KEY_UP, self.on_key_release)

        global panel, hbox
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Font configuration
        self.font_00 = wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_01 = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Text for window title
        self.m_text = wx.StaticText(panel, -1, "Maxwell Function Test!")
        self.m_text.SetFont(self.font_00)
        self.m_text.SetSize(self.m_text.GetBestSize())
        vbox.Add(self.m_text, 0, wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        # Test button
        self.test_bt = wx.Button(panel, wx.ID_CLOSE, "Start Test", size=(200, 30))
        self.test_bt.SetFont(self.font_01)
        self.test_bt.Bind(wx.EVT_BUTTON, self.start_test)
        vbox.Add(self.test_bt, 0, wx.ALIGN_LEFT | wx.ALL, 6)

        # Serial number
        self.m_text_SN = wx.StaticText(panel, 1, "Scan SN:")
        self.m_text_SN.SetFont(self.font_01)
        self.m_text_SN.SetSize(self.m_text_SN.GetBestSize())
        hbox.Add(self.m_text_SN, 1, flag=wx.ALL, border=6)

        # Serial number Text entry 02CB091800002
        self.m_serial = wx.TextCtrl(panel, 1,)
        hbox.Add(self.m_serial, 2, flag=wx.ALL, border=6)

        self.T_01_VGA = wx.CheckBox(panel, 1, '01-VGA Test')
        self.T_01_VGA.SetValue(True)
        self.T_02_Write_MAC = wx.CheckBox(panel, 2, '02-Write_MAC')
        self.T_02_Write_MAC.SetValue(True)
        self.T_03_Write_FRU = wx.CheckBox(panel, 3, '03-Write_FRU')
        self.T_03_Write_FRU.SetValue(True)

        self.T_04_ETH = wx.CheckBox(panel, 4, '04-ETH_Test')
        self.T_04_ETH.SetValue(True)
        self.T_05_SFP = wx.CheckBox(panel, 5, '05-SFP_Test')
        self.T_05_SFP.SetValue(True)
        self.T_06_CPU = wx.CheckBox(panel, 6, '06-CPU_Test')
        self.T_06_CPU.SetValue(True)

        self.T_07_Memory = wx.CheckBox(panel, 7, '07-Memory_Test')
        self.T_07_Memory.SetValue(True)
        self.T_08_Console = wx.CheckBox(panel, 8, '08-Console_Test')
        self.T_08_Console.SetValue(True)
        self.T_09_USB = wx.CheckBox(panel, 9, '09-USB_Test')
        self.T_09_USB.SetValue(True)

        self.T_10_PCI_E = wx.CheckBox(panel, 10, '10-PCI-E_Test')
        self.T_10_PCI_E.SetValue(True)
        self.T_11_SATA = wx.CheckBox(panel, 11, '11-SATA_Test')
        self.T_11_SATA.SetValue(True)
        self.T_12_M_2 = wx.CheckBox(panel, 12, '12-M.2_Test')
        self.T_12_M_2.SetValue(True)

        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1, id2=3)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=2)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=3)
        vbox.Add(hbox, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_01_VGA, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_02_Write_MAC, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_03_Write_FRU, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_04_ETH, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_05_SFP, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_06_CPU, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_07_Memory, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_08_Console, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_09_USB, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_10_PCI_E, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_11_SATA, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_12_M_2, 0, flag=wx.ALL, border=6)

        panel.SetSizer(vbox)
        panel.Layout()

        # setting variable
        self.setting = Setting()

    # def on_key_press(self, event):
    #     # print('key press')
    #     global Key_Code,value,value2,t_press
    #     t_press = time.time()
    #     Key_Code = event.GetKeyCode()
    #     if (48 <= Key_Code <= 90):
    #         value = switch_keycode(Key_Code).switch_content()
    #         value2 = str(value2) + str(value)
    #         # print(value)
    #         # print(value2)
    #     # event.Skip()
    #
    # def on_key_release(self, event):
    #     # print('key release')
    #     t_realease = time.time()
    #     duration = t_realease - t_press
    #     # print(duration)
    #     global value2
    #     if duration > 0.04:
    #         warning_message = wx.MessageDialog(None, "please do not input manually", "warning", wx.OK | wx.ICON_INFORMATION)
    #         value2 = ''
    #         self.m_serial.Clear()
    #         if warning_message.ShowModal() == wx.ID_OK:
    #             warning_message.Destroy()
    #     elif Key_Code == 13:
    #         # print('press enter')
    #         self.m_serial.SetValue(value2)
    #     # event.Skip()

    def start_test(self, event):

        start_dialog = wx.MessageDialog(None, "要进行测试吗？ Do You Want To Test?", "测试", wx.YES_NO | wx.ICON_QUESTION)
        start_result = start_dialog.ShowModal()
        start_dialog.Destroy()

        if start_result == wx.ID_YES:
            subprocess.getoutput("rm -f %s" % self.setting.logname)
            # self.start_dialog.Destroy()
            Serial_number = self.m_serial.GetValue()
            SN_check = Verify_SN(Serial_number).test_content()
            connect = subprocess.getoutput("ping -c 2 %s" % self.setting.hostname)
            if SN_check == 'FAIL':
                warning_message = wx.MessageDialog(None, "Wrong serial or serial number has lower case", "warning",
                                                   wx.OK | wx.ICON_INFORMATION)
                if warning_message.ShowModal() == wx.ID_OK:
                    warning_message.Destroy()

            elif '100% packet loss' in connect:
                warning_message = wx.MessageDialog(None, "Connect to BBU failed, test stop", "warning", wx.OK |
                                                   wx.ICON_INFORMATION)
                if warning_message.ShowModal() == wx.ID_OK:
                    warning_message.Destroy()

            else:
                T_101_VGA = self.T_01_VGA.GetValue()
                T_102_Write_MAC = self.T_02_Write_MAC.GetValue()
                T_103_Write_FRU = self.T_03_Write_FRU.GetValue()

                T_104_ETH = self.T_04_ETH.GetValue()
                T_105_SFP = self.T_05_SFP.GetValue()
                T_106_CPU = self.T_06_CPU.GetValue()

                T_107_Memory = self.T_07_Memory.GetValue()
                T_108_Console = self.T_08_Console.GetValue()
                T_109_USB = self.T_09_USB.GetValue()

                T_110_PCI_E = self.T_10_PCI_E.GetValue()
                T_111_SATA = self.T_11_SATA.GetValue()
                T_112_M_2 = self.T_12_M_2.GetValue()

                self.m_serial.Enable(False)
                self.test_bt.Disable()
                self.test_bt.SetBackgroundColour((0, 220, 18))
                self.test_bt.SetFont(self.font_01)
                self.test_bt.SetLabelText("Testing")

                sn = self.m_serial.GetValue()
                # print(sn)

                VGA_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_vga()
                Write_MAC_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU
                                            , T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2
                                            , Serial_number).test_mac()
                Write_FRU_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU
                                            , T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2
                                            , Serial_number).test_fru()
                # print(T_101_VGA)
                # print(T_102_Write_MAC)
                # print(T_103_Write_FRU)
                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 30%")

                ETH_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_eth()
                SFP_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_sfp()
                CPU_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_cpu()
                # print(T_104_ETH)
                # print(T_105_SFP)
                # print(T_106_CPU)

                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 60%")

                Memory_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                         T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                         Serial_number).test_memory()
                CONSOLE_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                          T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                          Serial_number).test_console()
                USB_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_usb()
                # print(T_107_Memory)
                # print(T_108_Console)
                # print(T_109_USB)

                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 90%")

                PCIE_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                       T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                       Serial_number).test_pcie()
                SATA_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                       T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                       Serial_number).test_sata()
                SSD_result = TestItem(T_101_VGA, T_102_Write_MAC, T_103_Write_FRU, T_104_ETH, T_105_SFP, T_106_CPU,
                                      T_107_Memory, T_108_Console, T_109_USB, T_110_PCI_E, T_111_SATA, T_112_M_2,
                                      Serial_number).test_m2()
                # print(T_110_PCI_E)
                # print(T_111_SATA)
                # print(T_112_M_2)

                # time.sleep(2)
                self.test_bt.SetLabelText("Testing 100%")
                # print("Yes")

                test_result = 'MAC: %s \rFRU: %s \rVGA: %s \rETH: %s \rSFP: %s \rCPU: %s\r' \
                              'Memory: %s\rCONSOLE: %s\rUSB: %s\rPCIE: %s\r SATA: %s\rM.2: %s\r' \
                              % (Write_MAC_result, Write_FRU_result, VGA_result, ETH_result, SFP_result, CPU_result,
                                 Memory_result, CONSOLE_result, USB_result, PCIE_result, SATA_result, SSD_result)

                summary_dialog = wx.MessageDialog(None, "测试结果如下：", test_result, wx.OK | wx.ICON_INFORMATION)
                summary_dialog.ShowModal()
                summary_dialog.Destroy()

                self.Destroy()

        else:
            print("No")
            print("No")
            print("No")
            print("No")
            print("No")
            print("No")
            self.Destroy()

    def close_frame(self, event):
        dialog = wx.MessageDialog(None, "Do You Want To Exit?", "Close", wx.YES_NO | wx.ICON_QUESTION)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_YES:
            self.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        frame = Frame("Function Test Platform V1.0")
        # self.Bind(wx.EVT_KEY_DOWN, self.frame.on_key_press)
        # self.Bind(wx.EVT_KEY_UP, self.frame.on_key_release)
        frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
