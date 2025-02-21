'''

                            Online Python Compiler.
         Codifique, compile, ejecute y depure el programa Python en línea.
Escriba su código en este editor y presione el botón "Run" para ejecutarlo.

'''

#empezar a crear smart notes  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QInputDialog, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QRadioButton, QHBoxLayout, QGroupBox, QButtonGroup, QTextEdit, QListWidget

import json

def write_notas():
    namefile = 0
    for name in notes:
        filename = str(namefile) + '.txt'
        with open(filename ,"w",encoding='utf-8') as file:
            file.write(name + '\n')
            file.write(notes[name]['texto'] + '\n')
            tags = notes[name]['etiquetas']
            for tag in tags:
                file.write(tag + '')
        namefile += 1

def read_notes():
    global notes
    
    namefile = 0
    while True:
        filename = str(namefile) + '.txt'
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                name = file.readline()#leer una linea del archivo
                name = name[: -1]#remover el ultimo caracter
                text = file.readline()
                text = text[: -1]
                tags = file.readline()
                tags = tags.split(' ')#convertir a lista separando el texto por espacio
                notes[name] = {}
                notes[name]['texto'] = text
                notes[name]['etiquetas'] = tags
            namefile += 1 #para que busque el siguiente archivo
            
        
        except:
            break
#escribir un archivo inicial
init_json = False
if init_json:
    notes = {'Bienvenido': {'texto' : ' aplicacion de notas' , 'etiquetas' : ['eti1', 'instrucciones']}}
    write_notas()



#crea la ventana
app=QApplication([])
win=QWidget()
win.setWindowTitle('smart notes')
win.resize(900,600)

#organizando los widgets por diseño
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()
field_text=QTextEdit()
col_1.addWidget(field_text)

#col2
list_note_label = QLabel('lista de notas')
list_notes = QListWidget()
col_2.addWidget(list_note_label)
col_2.addWidget(list_notes)

#botones notas
button_note_create = QPushButton('Crear nota') #una ventana aparece con el campo “Ingresar nombre de nota”
button_note_del = QPushButton('Eliminar nota')
button_note_save = QPushButton('Guardar nota')

#botones notas arriba
row1 = QHBoxLayout()
row_2 = QHBoxLayout()

#botones etiquetas abajo
row_3 = QHBoxLayout()
row_4 = QHBoxLayout()

#1
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
col_2.addLayout(row1)
#2
row_2.addWidget(button_note_save)
col_2.addLayout(row_2)

#name buttons
list_tags_label = QLabel('Lista de etiquetas')
list_tags = QListWidget()
field_tag = QLineEdit('')
field_tag.setPlaceholderText('Ingresar etiqueta…')
button_tag_add = QPushButton('Añadir a etiqueta')
button_tag_del = QPushButton('Remover etiqueta')
button_tag_search = QPushButton('Buscar por etiqueta')
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

#3
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
col_2.addLayout(row_3)

#4
row_4.addWidget(button_tag_search)
col_2.addLayout(row_4)

#nose
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
win.setLayout(layout_notes)

#leer el json
notes = {}
read_notes()
list_notes.addItems(notes)#carga las key en la lista de notas

#funciones de las notas 
def show_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        #carga las notas
        field_text.setText(notes[key]["texto"])
        #carga las etiquetas
        list_tags.clear()
        list_tags.addItems(notes[key]["etiquetas"])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        text = field_text.toPlainText()
        notes[key]['texto']=text
        write_notas()

def create_note():
    note_name, result = QInputDialog.getText(win, "Añadir nota", "Nombre de nota: ")
    if result and note_name != '':
        notes[note_name] = {"texto" : "", "etiquetas" : []}
        list_notes.addItem(note_name)

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        write_notas()


#funciones de las etiquetas 
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text() #leer el texto del field
        notes[key]["etiquetas"]
        if not tag in notes[key]["etiquetas"] and tag != '':
            notes[key]["etiquetas"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            write_notas()
        
def del_tag():
    if list_tags.selectedItems() and list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["etiquetas"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["etiquetas"])
        print(notes)
        write_notas()

def search_tag():
    print(button_tag_search)
    tag = field_tag.text()
    if button_tag_search.text() == "Buscar por etiqueta" and tag != '':
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["etiquetas"]:
                notes_filtered[note]=notes[note]
            button_tag_search.setText("Restablecer búsqueda")
            list_notes.clear()
            list_tags.clear()
            list_notes.addItems(notes_filtered)
    elif button_tag_search.text() == "Restablecer búsqueda":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Buscar por etiqueta")
        


#eventos de las notas 
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_create.clicked.connect(create_note)
button_note_del.clicked.connect(del_note)


#eventos de las etiquetas 
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


#funcion
win.show()
app.exec()
