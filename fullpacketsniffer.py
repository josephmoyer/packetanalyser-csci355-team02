#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Tue Apr 21 14:37:44 2015
#

import wx
import time
import csv
# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

#!/usr/bin/env python
#Packet sniffer in python
#For Linux - Sniffs all incoming and outgoing packets :)
#Silver Moon (m00n.silv3r@gmail.com)




import socket, sys
from struct import *
#Convert a string of 6 characters of ethernet address into a dash separated hex string
def eth_addr (a) :
	  b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
	  return b


class MyFrame(wx.Frame):
	run = False
	packetcount = 0
	starttime = 0.0

	def __init__(self, *args, **kwds):
		# begin wxGlade: MyFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.btnStart = wx.Button(self, wx.ID_ANY, _("Start"))
		self.btnStop = wx.Button(self, wx.ID_ANY, _("Stop"))
		self.btnClear = wx.Button(self, wx.ID_ANY, _("Clear"))
		self.btnPrint = wx.Button(self, wx.ID_ANY, _("Print"))
		self.lstMain = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		self.lstMain.InsertColumn(0, "No.",width=50)
		self.lstMain.InsertColumn(1, "Time")
		self.lstMain.InsertColumn(2, "Source",width=150)
		self.lstMain.InsertColumn(3, "Destination",width=150)
		self.lstMain.InsertColumn(4, "Protocol")
		self.lstMain.InsertColumn(5, "Length",width=50)
		self.lstMain.InsertColumn(6, "Info",width=250)
		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.btnStart_Click, self.btnStart)
		self.Bind(wx.EVT_BUTTON, self.btnStop_Click, self.btnStop)
		self.Bind(wx.EVT_BUTTON, self.btnClear_Click, self.btnClear)
		self.Bind(wx.EVT_BUTTON, self.btnPrint_Click, self.btnPrint)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: MyFrame.__set_properties
		self.SetTitle(_("Packet Analyser"))
		self.SetSize((800, 600))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: MyFrame.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_3.Add(self.btnStart, 0, wx.FIXED_MINSIZE, 0)
		sizer_3.Add(self.btnStop, 0, wx.FIXED_MINSIZE, 0)
		sizer_3.Add(self.btnClear, 0, wx.FIXED_MINSIZE, 0)
		sizer_3.Add(self.btnPrint, 0, wx.FIXED_MINSIZE, 0)
		sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
		sizer_2.Add(self.lstMain, 16, wx.EXPAND, 0)
		sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade

	def sniff(self):
		pktTime = 0.0
		pktSAddr = ''
		pktSPort = ''
		pktDAddr = ''
		pktDPort = ''
		pktProtocol = ''
		pktLength = 0
		pktInfo = ''
		try:
			s = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
		except socket.error , msg:
			print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()

		# receive a packet
		while (self.run == True):
			packet = s.recvfrom(65565)
			pktTime = time.time()
		#packet string from tuple
			packet = packet[0]

		#parse ethernet header
			eth_length = 14
			eth_header = packet[:eth_length]
			eth = unpack('!6s6sH' , eth_header)
			eth_protocol = socket.ntohs(eth[2])
			print 'Destination MAC : ' + eth_addr(packet[0:6]) + ' Source MAC : ' + eth_addr(packet[6:12]) + ' Protocol : ' + str(eth_protocol)
			wx.Yield()
			#Parse IP packets, IP Protocol number = 8
			 #Parse IP packets, IP Protocol number = 8
			if eth_protocol == 8 :
				#Parse IP header
				#take first 20 characters for the ip header
				ip_header = packet[eth_length:20+eth_length]

				#now unpack them :)
				iph = unpack('!BBHHHBBH4s4s' , ip_header)

				version_ihl = iph[0]
				version = version_ihl >> 4
				ihl = version_ihl & 0xF

				iph_length = ihl * 4

				ttl = iph[5]
				self.protocol = iph[6]
				self.s_addr = socket.inet_ntoa(iph[8]);
				pktSAddr = socket.inet_ntoa(iph[8])
				self.d_addr = socket.inet_ntoa(iph[9]);
				pktDAddr = socket.inet_ntoa(iph[9])

				print 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(self.protocol) + ' Source Address : ' + str(self.s_addr) + ' Destination Address : ' + str(self.d_addr)
				wx.Yield()
				#TCP protocol
				if self.protocol == 6 :
					pktProtocol = 'TCP'
					t = iph_length + eth_length
					tcp_header = packet[t:t+20]

					#now unpack them :)
					tcph = unpack('!HHLLBBHHH' , tcp_header)

					self.source_port = tcph[0]
					self.dest_port = tcph[1]
					pktSPort = tcph[0]
					pktDPort = tcph[1]
					sequence = tcph[2]
					acknowledgement = tcph[3]
					doff_reserved = tcph[4]
					tcph_length = doff_reserved >> 4

					print 'Source Port : ' + str(self.source_port) + ' Dest Port : ' + str(self.dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
					wx.Yield()
					h_size = eth_length + iph_length + tcph_length * 4
					data_size = len(packet) - h_size

				   #get data from the packet
					self.data = packet[h_size:]
					pktLength = len(self.data)
					pktInfo = self.data
					print 'Data : ' + self.data
					wx.Yield()
					#ICMP Packets
				elif self.protocol == 1 :
					pktProtocol = 'ICMP'
					u = iph_length + eth_length
					icmph_length = 4
					icmp_header = packet[u:u+4]

					#now unpack them :)
					icmph = unpack('!BBH' , icmp_header)

					icmp_type = icmph[0]
					code = icmph[1]
					checksum = icmph[2]

					print 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)
					wx.Yield()
					h_size = eth_length + iph_length + icmph_length
					data_size = len(packet) - h_size

					#get data from the packet
					self.data = packet[h_size:]
					pktLength = len(self.data)
					pktInfo = self.data
					print 'Data : ' + self.data
					wx.Yield()
					#UDP packets
				elif self.protocol == 17 :
					pktProtocol = 'UDP'
					u = iph_length + eth_length
					udph_length = 8
					udp_header = packet[u:u+8]

				   #now unpack them :)
					udph = unpack('!HHHH' , udp_header)

					self.source_port = udph[0]
					self.dest_port = udph[1]
					pktSPort = udph[0]
					pktDPort = udph[1]
					self.length = udph[2]
					checksum = udph[3]

					print 'Source Port : ' + str(self.source_port) + ' Dest Port : ' + str(self.dest_port) + ' Length : ' + str(self.length) + ' Checksum : ' + str(checksum)
					wx.Yield()
					h_size = eth_length + iph_length + udph_length
					data_size = len(packet) - h_size

					#get data from the packet
					self.data = packet[h_size:]
					pktLength = len(self.data)
					pktInfo = self.data

					print 'Data : ' + self.data
					wx.Yield()
				#some other IP packet like IGMP
				else :
					print 'Protocol other than TCP/UDP/ICMP'
			self.lstMain.InsertStringItem(self.packetcount,str(self.packetcount))
			self.lstMain.SetStringItem(self.packetcount,1,str(pktTime - self.starttime))
			if (pktProtocol == 'ICMP'):
				self.lstMain.SetStringItem(self.packetcount,2,str(pktSAddr))
				self.lstMain.SetStringItem(self.packetcount,3,str(pktDAddr))
			else:
				self.lstMain.SetStringItem(self.packetcount,2,str(pktSAddr) + ':' + str(pktSPort))
				self.lstMain.SetStringItem(self.packetcount,3,str(pktDAddr) + ':' + str(pktDPort))
			self.lstMain.SetStringItem(self.packetcount,4,str(pktProtocol))
			self.lstMain.SetStringItem(self.packetcount,5,str(pktLength))
			# self.lstMain.SetItem(self.packetcount,6,pktInfo)

			# if (pktProtocol == 'ICMP'):
			# 	self.lstMain.Append(self.packetcount,pktTime-self.starttime,str(pktSAddr),str(pktDAddr),pktProtocol,pktLength,pktInfo)
			# else:
			# 	self.lstMain.Append(self.packetcount,pktTime-self.starttime,str(pktSAddr) + ':' + str(pktSPort),str(pktDAddr) + ':' + str(pktDPort),pktProtocol,pktLength,pktInfo)
			self.packetcount += 1
			wx.Yield()


	def btnStart_Click(self, event):  # wxGlade: MyFrame.<event_handler>
		if(self.run == False):
			if(self.lstMain.GetItemCount() != 0):
				confirm = wx.MessageDialog(None,'Are you sure you want to restart?',caption='This will delete all existing data in the window.',style=wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)
				if(confirm.ShowModal() == wx.ID_YES):
					self.lstMain.DeleteAllItems()
					self.packetcount = 0
					self.starttime = time.time()
					self.run = True
					self.sniff()
			else:
				self.starttime = time.time()
				self.run = True
				self.sniff()

	def btnStop_Click(self, event):  # wxGlade: MyFrame.<event_handler>
		if(self.run == True):
			self.run = False

	def btnClear_Click(self, event):  # wxGlade: MyFrame.<event_handler>
		confirm = wx.MessageDialog(None,'Are you sure you want to clear all data?',style=wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)
		if(confirm.ShowModal() == wx.ID_YES):
			self.lstMain.DeleteAllItems()
			self.packetcount = 0

	def btnPrint_Click(self, event):  # wxGlade: MyFrame.<event_handler>
		save_dlg = wx.FileDialog(self, "Save CSV","","New File.csv","CSV files (*.csv)|*.csv|TXT files (*.txt)|*.txt",wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		if save_dlg.ShowModal() == wx.ID_CANCEL:
			return
		path = save_dlg.GetPath()
		with open(path,'wb') as f:
			writer = csv.writer(f,delimiter=',')
			rows = self.lstMain.GetItemCount()
			cols = self.lstMain.GetColumnCount()
			writer.writerow(["No.","Time","Source","Destination","Protocol","Length","Info"])
			for row in range(rows):
				item = []
				for col in range(cols):
					item.append(self.lstMain.GetItem(row,col).GetText())
				writer.writerow(item)

# end of class MyFrame
if __name__ == "__main__":
	gettext.install("app") # replace with the appropriate catalog name

	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	frame_1 = MyFrame(None, wx.ID_ANY, "")
	app.SetTopWindow(frame_1)
	frame_1.Show()
	app.MainLoop()
