from referenceTables import refType, refTypeBuffer, refEventControl, refExtEventControl
from prettytable import PrettyTable
import datetime
import time

eventsToShow = 7

time0 = time.time()  # timestamp
filepath = r'C:\PY\Parse-Byte-Array\List12500 PL Clear.lst'
#filepath = r'C:\PY\Parse-Byte-Array\SwitchOnlyTest.lst'
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
dataFlag = 0
with open(filepath, 'rb') as f:
    header = f.read(64)
    while event <= 12500:
        row = []
        row.append(event)

        EventType = 2
        value = f.read(EventType)
        if value == b'':
            break
        #print(value)
        if not value[0]:  # Primary
            row.append('')
        else:  # Secondary
            if value[1] != 1:  # Secondary with no buffer
                row.append(refType[value[0]])
            else:  # Secondary with buffer
                row.append(refTypeBuffer[0])
                dataFlag = 1

        fKey = 8
        value = f.read(fKey)
        #print(value.hex(' ').upper(), ' --  fKey')

        freconcilekey = 32
        value = f.read(freconcilekey)
        #print(value.hex(' ').upper(), ' --  Reconcile')
        row.append(value.decode('1250').strip())

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
        row.append(value.decode('1250').strip())

        fetitle = 32
        value = f.read(fetitle)
        #print(value.hex(' ').upper(), ' --  Title')
        row.append(value.decode('1250').strip())

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
        row.append(datetime.date.fromordinal(693596+int.from_bytes(value)).__format__('%m/%d/%Y'))

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

        Reserved50 = 50
        value = f.read(Reserved50)
        #print(value.hex(' ').upper())

        OrigTime = 4
        value = f.read(OrigTime)

        OrigDate = 2
        value = f.read(OrigDate)

        fevttype = 1
        value = f.read(fevttype)

        fetriggeredlists = 2
        value = f.read(fetriggeredlists)

        port = 2
        value = f.read(port)

        feventchanged = 1
        value = f.read(feventchanged)

        fbookmark = 1
        value = f.read(fbookmark)

        feventtrigger = 1
        value = f.read(feventtrigger)

        resBufferSize = ord(f.read(1)) + ord(f.read(1)) * 256
        resBuffer = f.read(resBufferSize)

        ratingSize = ord(f.read(1)) + ord(f.read(1)) * 256
        rating = f.read(ratingSize)

        showIDsize = ord(f.read(1)) + ord(f.read(1)) * 256
        showID = f.read(showIDsize)

        showDescrSize = ord(f.read(1)) + ord(f.read(1)) * 256
        showDescr = f.read(showDescrSize)

        if dataFlag:
            dataBufferSize = ord(f.read(1)) + ord(f.read(1)) * 256
            dataBuffer = f.read(dataBufferSize)
            dataFlag = 0
            print('DATAFLAG')

        table.add_row(row)
        event = event + 1

time1 = time.time()
print((time1 - time0).__round__(3), 's')  # it was ~1.4 seconds when just pos++ for 8750064 bytes (~9 MB)
#print(table)
#print(table.get_string(fields=["No", "OnAirDate", "OnAirTime", "Sec", "Type"]))
'''
table.field_names = [
    "No",
    "ID",
    "Title",
    "Sec",
    "Reconcile",
    "OnAirTime",
    "SOM",
    "DUR",
    "Seg",
    "DateToAir",
]
'''
print(table.get_string(end=eventsToShow))
