'''
June 2018
@author: Hanifa Arrumaisha
'''

# =======================
# imports
# =======================
import tkinter as tk
from tkinter import ttk
from tkinter import *

class CrawlerGUI:
	def __init__(self):
		# Create instance
		self.win = tk.Tk() 

		# Add a title       
		self.win.title("Crawler Dattabot")     

		# Change the main windows icon
		# self.win.iconbitmap('dattabot.jpg') 

		self.create_widgets()

	def radSocmedCall(self):
		print("Radiobutton value: ",self.radSocmedVar.get())

	def productCall(self, *args):
		print("Product menu value: ", self.productVar.get())

	def _spin(self):
		print("Spin value: ", self.spin.get())

	def createListBox(self):
		lblListBox = ttk.Label(self.frame1, text=" Pilih Keyword:")
		lblListBox.grid(column=0, row=5, sticky=tk.NW)
		listFrame = ttk.Frame(self.frame1)
		listFrame.grid(column=1, row=5, columnspan=3, padx=20, pady=30)

		scrollBar = ttk.Scrollbar(listFrame)
		scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
		self.listBox = Listbox(listFrame, selectmode=MULTIPLE)
		self.listBox.pack(side=tk.LEFT, fill=tk.Y)
		scrollBar.config(command=self.listBox.yview)
		self.listBox.config(yscrollcommand=scrollBar.set) 

	def insertListBox(self, listInsert):
		for item in listInsert:
			self.listBox.insert(END, item)

	def selectAllList(self):
		self.listBox.select_set(0, END)

	def unselectAllList(self):
		self.listBox.selection_clear(0, END)

	def createRadioBtn(self, frame, variable, lst, callback, row):
		variable.set(99)                                 
		 
		# Now we are creating all Radiobutton widgets within one loop
		for col in range(len(lst)):                             
			curRad = tk.Radiobutton(frame, text=lst[col], variable=variable, value=col, command=callback)          
			curRad.grid(column=col+1, row=row, sticky=tk.W)             # row=6

	def radKeywOptCall(self):
		print(self.radKeywOptVar.get())
		# check for input listbox
		if (self.radKeywOptVar.get()==0):
			# TODO
			# give input for file
			print("ask for input file csv")

			# TODO
			# read input file then show it on listbox

		else:
			pass
			# TODO
			# read keyword from selected database then input to listbox


	def create_widgets(self):
		# Create frame 1 to choose social media to crawl
		self.frame1 = ttk.Frame(self.win)
		lblFrame1 = ttk.Label(self.frame1, text=' Select social media to crawl: ')
		self.frame1.pack(side=tk.TOP)
		lblFrame1.grid(column=0, row=0)

		socmed = ["Instagram", "Twitter"]   
        
		# create three Radiobuttons using one variable
		self.radSocmedVar = tk.IntVar()
		self.createRadioBtn(frame=self.frame1, variable=self.radSocmedVar, lst=socmed, callback=self.radSocmedCall, row=0)

		# Now we select the database or the product
		product = ["Amild", "Marlboro", "Umild", "Magnum", "GG", "Camel"]

		# Create Dropdown menu to choose database or product
		lblProduct = ttk.Label(self.frame1, text=" Select product to search:")
		lblProduct.grid(column=0, row=2, sticky=tk.W)
		self.productVar = tk.StringVar()
		self.productVar.set("Amild")
		self.productMenu = OptionMenu(self.frame1, self.productVar, *product, command=self.productCall)
		self.productMenu.grid(column=1, row=2, sticky=tk.W)

		# Create ListBox to select keyword 
		self.createListBox()
		
		# create option to select keyword from csv or db
		lblKeywOpt = ttk.Label(self.frame1, text=" Select keyword from: ")
		lblKeywOpt.grid(column=0, row=4, sticky=tk.W)
		self.radKeywOptVar = tk.IntVar()
		self.createRadioBtn(self.frame1, self.radKeywOptVar, ['csv', 'database'], self.radKeywOptCall, 4)

		# TODO
		# show button to select all
		# show button to deselect all
		# show button to craw selected keyword
		


crawler = CrawlerGUI()
crawler.win.mainloop()