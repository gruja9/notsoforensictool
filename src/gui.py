import os
import tkinter
from tkinter import ttk
from tkinter import messagebox
import utils

class GUI:

	def __init__(self):
	
		# Storage dicts for report generation
		self.allfiles = dict()
		self.specificfiles = dict()
		self.infofiles = dict()
		self.datefiles = dict()
		self.match_hashset = list()

		# Main Window
		self.main_window = tkinter.Tk()
		self.main_window.title("Forensiskt verktyg")

		# Tabs
		self.tab_parent = ttk.Notebook(self.main_window)
		self.tab1 = tkinter.Frame(self.tab_parent)
		self.tab2 = tkinter.Frame(self.tab_parent)
		self.tab3 = tkinter.Frame(self.tab_parent)
		self.tab4 = tkinter.Frame(self.tab_parent)
		self.tab_parent.add(self.tab1, text="Sök")
		self.tab_parent.add(self.tab2, text="Kryptera/Dekryptera")
		self.tab_parent.add(self.tab3, text="Filanalys")
		self.tab_parent.add(self.tab4, text="Other")

		# Frames
			# Tab 1
		self.radio_frame = ttk.Labelframe(self.tab1)
		self.entry_frame = tkinter.Frame(self.tab1)
		self.entryleft_frame = tkinter.Frame(self.entry_frame)
		self.entryright_frame = tkinter.Frame(self.entry_frame)

			# Tab 2
		self.cryptname_frame = tkinter.Frame(self.tab2)
		self.cryptbuttons_frame = tkinter.Frame(self.tab2)
		self.encrypt_frame = tkinter.Frame(self.cryptbuttons_frame)
		self.decrypt_frame = tkinter.Frame(self.cryptbuttons_frame)
		
		# Labels
			# Tab 1
		self.katalog_label = tkinter.Label(self.entryleft_frame, text="Ange en katalog: ")
		self.ext_label = tkinter.Label(self.entryright_frame, text="Ange en filändelse: ")
		self.keyword_label = tkinter.Label(self.entryleft_frame, text="Ange ett sökord: ")
		self.date_label = tkinter.Label(self.entryright_frame, text="Ange ett datum (2020-03-02): ")

			# Tab 2
		self.cryptname_label = tkinter.Label(self.cryptname_frame, text="Ange en fil: ")

			# Tab 3
		self.file1_label = tkinter.Label(self.tab3, text="Fil 1: ")
		self.file2_label = tkinter.Label(self.tab3, text="Fil 2: ")

		# Entries
			# Tab 1
		self.katalog_entry = tkinter.Entry(self.entryleft_frame, width=20, state=tkinter.DISABLED)
		self.ext_entry = tkinter.Entry(self.entryright_frame, width=5, state=tkinter.DISABLED)
		self.keyword_entry = tkinter.Entry(self.entryleft_frame, width=20, state=tkinter.DISABLED)
		self.date_entry = tkinter.Entry(self.entryright_frame, width=10, state=tkinter.DISABLED)

			# Tab 2
		self.cryptname_entry = tkinter.Entry(self.cryptname_frame, width=30)

			# Tab 3
		self.file1_entry = tkinter.Entry(self.tab3, width=35)
		self.file2_entry = tkinter.Entry(self.tab3, width=35)

		# Radiobuttons
		self.radiovar = tkinter.IntVar()
		self.findfiles_radio = tkinter.Radiobutton(self.radio_frame, text="Sök efter filer", variable=self.radiovar, value=1, command=self.enable_entries)
		self.findfilesext_radio = tkinter.Radiobutton(self.radio_frame, text="Sök efter filer med viss filändelse", variable=self.radiovar, value=2, command=self.enable_entries)
		self.searchinfo_radio = tkinter.Radiobutton(self.radio_frame, text="Sök efter viss information i viss filtyp", variable=self.radiovar, value=3, command=self.enable_entries)
		self.date_radio = tkinter.Radiobutton(self.radio_frame, text="Sök efter modifierade filer senast ett visst datum", variable=self.radiovar, value=4, command=self.enable_entries)

		# Buttons
			# Tab 1
		self.search_button = tkinter.Button(self.entryleft_frame, text="Sök!", width=15, command=self.execute_operation)
		self.reset_button = tkinter.Button(self.entryright_frame, text="Återställ!", width=15, command=self.reset)

			# Tab 2
		self.encrypt_button = tkinter.Button(self.encrypt_frame, text="Kryptera", width=10, command=self.encrypt)
		self.decrypt_button = tkinter.Button(self.decrypt_frame, text="Dekryptera", width=10, command=self.decrypt)

			 # Tab 3
		self.diff_button = tkinter.Button(self.tab3, text="Skillnad", width=10, command=self.difference)

			# Tab 4
		self.sysinfo_button = tkinter.Button(self.tab4, text="System Information", width=20, command=self.sysinfo)
		self.genreport_button = tkinter.Button(self.tab4, text="Generate Report", width=20, command=self.genreport)

		# Pack Radiobuttons
		self.findfiles_radio.pack(anchor="w")
		self.findfilesext_radio.pack(anchor="w")
		self.searchinfo_radio.pack(anchor="w")
		self.date_radio.pack(anchor="w")

		# Pack Labels and Entries
			# Tab 1
		self.katalog_label.pack()
		self.katalog_entry.pack()
		self.ext_label.pack()
		self.ext_entry.pack()
		self.keyword_label.pack(pady=5)
		self.keyword_entry.pack()
		self.date_label.pack(pady=5)
		self.date_entry.pack()

			# Tab 2
		self.cryptname_label.pack()
		self.cryptname_entry.pack()

			# Tab 3
		self.file1_label.grid(row=1, column=1, pady=20, padx=30)
		self.file1_entry.grid(row=1, column=2)
		self.file2_label.grid(row=2, column=1)
		self.file2_entry.grid(row=2, column=2)

		# Pack Buttons
			# Tab 1
		self.search_button.pack(pady=10)
		self.reset_button.pack(pady=10)

			# Tab 2
		self.encrypt_button.pack()
		self.decrypt_button.pack()

			# Tab 3
		self.diff_button.grid(row=5, column=2, pady=10)

			# Tab 4
		self.sysinfo_button.grid(row=1, column=0, pady=20, padx=135)
		self.genreport_button.grid(row=2, column=0, pady=10, padx=135)

		# Pack Frames
			# Tab 1
		self.radio_frame.pack(side='top', padx=60, pady=20)
		self.entry_frame.pack(side='bottom')
		self.entryleft_frame.pack(side='left', padx=20)
		self.entryright_frame.pack(side='right')

			# Tab 2
		self.cryptname_frame.pack(side='top')	
		self.cryptbuttons_frame.pack(side='bottom')
		self.encrypt_frame.pack(side='left', anchor='w', padx=10)
		self.decrypt_frame.pack(side='right', anchor='e', padx=10)

		self.cryptbuttons_frame.place(relx=0.22, rely=0.55, x=0, y=0)
		self.cryptname_frame.place(relx=0.22, rely=0.3, x=0, y=0)

		# Pack Notepad
		self.tab_parent.pack(expand=1, fill='both')

		tkinter.mainloop()


	def enable_entries(self):	# Slå på eller av olika entries beroende på valet i radiobuttons
		choice = self.radiovar.get()
		if choice == 1:
			self.katalog_entry.config(state=tkinter.NORMAL)
			self.ext_entry.config(state=tkinter.DISABLED)
			self.keyword_entry.config(state=tkinter.DISABLED)
			self.date_entry.config(state=tkinter.DISABLED)

		elif choice == 2:
			self.katalog_entry.config(state=tkinter.NORMAL)
			self.ext_entry.config(state=tkinter.NORMAL)
			self.keyword_entry.config(state=tkinter.DISABLED)
			self.date_entry.config(state=tkinter.DISABLED)

		elif choice == 3:
			self.katalog_entry.config(state=tkinter.NORMAL)
			self.ext_entry.config(state=tkinter.NORMAL)
			self.keyword_entry.config(state=tkinter.NORMAL)
			self.date_entry.config(state=tkinter.DISABLED)

		elif choice == 4:
			self.katalog_entry.config(state=tkinter.NORMAL)
			self.ext_entry.config(state=tkinter.DISABLED)
			self.keyword_entry.config(state=tkinter.DISABLED)
			self.date_entry.config(state=tkinter.NORMAL)

	def display_results(self, results):	# Gör ett nytt (större) fönster för att visa resultat
		window = tkinter.Tk()
		window.geometry('900x600')
		textbox = tkinter.Text(window)
		textbox.pack(expand=1, fill='both')
		for item in results:
			textbox.insert(tkinter.END, item + '\n')
		window.mainloop()

	def execute_operation(self):	# Anropa olika funktioner beroende på valet i radiobuttons och skapa dictionaries inför generering av rapport
		folder = self.katalog_entry.get()
		ext = self.ext_entry.get()
		keyword = self.keyword_entry.get()
		date = self.date_entry.get()
		
		if self.radiovar.get() == 1:

			if folder:
				if os.path.isdir(folder):
					list_tmp = utils.find_all_files(folder)
					self.match_hashset += utils.verify_files(list_tmp)
					utils.create_dict(folder, self.allfiles, list_tmp)
					self.display_results(list_tmp)
				else:
					tkinter.messagebox.showerror('Error', 'Detta är inte en äkta katalog!')
			else:
				tkinter.messagebox.showerror('Error', 'Du måste ange en katalog!')

		elif self.radiovar.get() == 2:

			if folder and ext:
				if os.path.isdir(folder):
					list_tmp = utils.find_specific_files(folder, ext)
					self.match_hashset += utils.verify_files(list_tmp)
					utils.create_dict(ext, self.specificfiles, list_tmp)
					self.display_results(list_tmp)
				else:
					tkinter.messagebox.showerror('Error', 'Detta är inte en äkta katalog!')
			else:
				tkinter.messagebox.showerror('Error', 'Du måste ange både katalog och filändelse!')

		elif self.radiovar.get() == 3:

			if folder and ext and keyword:
				if os.path.isdir(folder):
					list_tmp = utils.search_files(folder, ext, keyword)
					self.match_hashset += utils.verify_files(list_tmp)
					utils.create_dict(keyword, self.infofiles, list_tmp)
					self.display_results(list_tmp)
				else:
					tkinter.messagebox.showerror('Error', 'Detta är inte en äkta katalog!')
			else:
				tkinter.messagebox.showerror('Error!', 'Du måste ange katalog, filändelse och sökord!')

		elif self.radiovar.get() == 4:

			if folder and date:
				if os.path.isdir(folder):
					list_tmp = utils.find_modified_files(folder, date)
					self.match_hashset += utils.verify_files(list_tmp)
					utils.create_dict(date, self.datefiles, list_tmp)
					self.display_results(list_tmp)
				else:
					tkinter.messagebox.showerror('Error', 'Detta är inte en äkta katalog!')
			else:
				tkinter.messagebox.showerror('Error!', 'Du måste ange katalog och datum!')

	def encrypt(self):
		filename = self.cryptname_entry.get()
		if filename:
			if os.path.isfile(filename):
				filename_enc = utils.encrypt_file(filename)
				tkinter.messagebox.showinfo('Encrypted', 'Filen har krypterats i ' + filename_enc)
			else:
				tkinter.messagebox.showerror('Error', 'Detta är inte en äkta fil!')
		else:
			tkinter.messagebox.showerror('Error', 'Du måste ange en fil!')

	def decrypt(self):
		filename = self.cryptname_entry.get()
		if filename:
			if os.path.isfile(filename):
				filename_dec = utils.decrypt_file(filename)
				tkinter.messagebox.showinfo('Decrypted', 'File har dekrypterats i ' + filename_dec)
			else:
				tkinter.messagebox.showerror('Error', 'Detta är inte en äkta fil!')
		else:
				tkinter.messagebox.showerror('Error', 'Du måste ange en fil!')

	def reset(self):	# Återställa radiobuttons och entries
		self.radiovar.set(0)

		self.katalog_entry.config(state=tkinter.NORMAL)
		self.katalog_entry.delete(0, 'end')
		self.katalog_entry.config(state=tkinter.DISABLED)

		self.ext_entry.config(state=tkinter.NORMAL)
		self.ext_entry.delete(0, 'end')
		self.ext_entry.config(state=tkinter.DISABLED)

		self.keyword_entry.config(state=tkinter.NORMAL)
		self.keyword_entry.delete(0, 'end')
		self.keyword_entry.config(state=tkinter.DISABLED)

		self.date_entry.config(state=tkinter.NORMAL)
		self.date_entry.delete(0, 'end')
		self.date_entry.config(state=tkinter.DISABLED)

	def difference(self):	# Visa skillnader mellan två filer
		file1 = self.file1_entry.get()
		file2 = self.file2_entry.get()
		if file1 and file2:
			if os.path.isfile(file1) and os.path.isfile(file2):
				file1_diff, file2_diff = utils.word_difference(file1, file2)
				results = ["Ord som finns i fil 1, men inte i fil 2:"]
				results += file1_diff
				results.append("\nOrd som finns i fil 2, men inte i fil 1:")
				results += file2_diff
				self.display_results(results)
			else:
				tkinter.messagebox.showerror('Error', 'Dessa är inte äkta filer!')
		else:
			tkinter.messagebox.showerror('Error', 'Du måste ange båda filerna!')

	def sysinfo(self):	# Få systeminformation
		results = utils.system_information()
		self.display_results(results)

	def genreport(self):	# Generera rapport
		dictionary = dict()
		dictionary['sys'] = utils.system_information()
		dictionary['hashset'] = self.match_hashset
		dictionary['allfiles'] = self.allfiles
		dictionary['extfiles'] = self.specificfiles
		dictionary['infofiles'] = self.infofiles
		dictionary['datefiles'] = self.datefiles
		utils.gen_report(dictionary)
		tkinter.messagebox.showinfo('Success', 'Rapporten har genererats i report.pdf!')


if __name__ == '__main__':
	print('Detta är en modul och ska inte köras självständigt!')
	exit()
