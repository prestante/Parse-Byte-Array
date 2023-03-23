import datetime
from os import path
import time
from prettytable import PrettyTable

time0 = time.time()  # timestamp
filepath = r'C:\Lists\List12500 PL Clear.lst'
length = path.getsize(filepath)
table = PrettyTable()
table.field_names = [
    "No",
    "Sec",
    "Reconcile",
    "OnAirTime",
    "ID",
    "Title",
    "SOM",
    "DUR",
    "Seg",
    "DateToAir"]

'''
    "Type"
    "CompileID"
    "CompileSOM"
    "ABOX"
    "ABOXSOM"
    "BBOX"
    "BBOXSOM"
    "ResBuffer"
    "Content"
]
'''
event = 1
with open(filepath, 'rb') as f:
    header = f.read(64)
    while event <= 1:
        row = []
        row.append(event)

        EventType = 2
        value = f.read(EventType)
        #print(value.hex(' ').upper(), ' --  EventType')
        row.append('plug')

        fKey = 8
        value = f.read(fKey)
        #print(value.hex(' ').upper(), ' --  fKey')

        freconcilekey = 32
        value = f.read(freconcilekey)
        #print(value.hex(' ').upper(), ' --  Reconcile')
        row.append(value.decode('ASCII').strip())

        Effects = 3
        value = f.read(Effects)
        #print(value.hex(' ').upper(), ' --  Effects')

        OnAirTime = 4
        value = f.read(OnAirTime)
        #print(value.hex(' '), ' --  OnAirTime')
        row.append(value.hex(' '))

        feid = 32
        value = f.read(feid)
        #print(value.hex(' ').upper(), ' --  ID')
        row.append(value.decode('ASCII').strip())

        fetitle = 32
        value = f.read(fetitle)
        #print(value.hex(' ').upper(), ' --  Title')
        row.append(value.decode('ASCII').strip())

        Som = 4
        value = f.read(Som)
        #print(value.hex(' '), ' --  SOM')
        row.append(value.hex(' '))

        Dur = 4
        value = f.read(Dur)
        #print(value.hex(' '), ' --  DUR')
        row.append(value.hex(' '))

        fechannel = 1
        value = f.read(fechannel)

        fesegment = 1
        value = f.read(fesegment)
        if value == b'\xff':
            row.append('')
        else:
            row.append(ord(value))

        Indexes = 8
        value = f.read(Indexes)

        fdatetoair = 2
        value = f.read(fdatetoair)
        row.append(datetime.date.fromordinal(693596+int.from_bytes(value)))

        feventcontrol = 2
        value = f.read(feventcontrol)

        feventstatus = 4
        value = f.read(feventstatus)

        fcompiletape = 32
        value = f.read(fcompiletape)

        fcompilesom = 4
        value = f.read(fcompilesom)

        fabox = 32
        value = f.read(fabox)

        faboxsom = 4
        value = f.read(faboxsom)

        fbbox = 32
        value = f.read(fbbox)

        fbboxsom = 4
        value = f.read(fbboxsom)

        Indexes2 = 3
        value = f.read(Indexes2)

        extEventControl = 2
        value = f.read(extEventControl)

        fClosedCaptionToFieldsToSource = 26
        value = f.read(fClosedCaptionToFieldsToSource)






        table.add_row(row)
        event = event + 1

time1 = time.time()
print((time1 - time0).__round__(3), 's')  # it was ~1.4 seconds when just pos++ for 8750064 bytes (~9 MB)
print(table)
