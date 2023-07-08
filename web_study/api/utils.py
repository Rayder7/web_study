from admin import FieldStudyResource, StudyGroupResource 
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, LoadOptions, SaveFormat


def make_excel():
    datafieldstudy = FieldStudyResource().export()
    dataStudygroup = StudyGroupResource().export()

    LoadOptions = LoadOptions(FileFormatType.CSV)
    workbook_1 = Workbook("datafieldstudy", LoadOptions)
    workbook_2 = Workbook("datastudygroup", LoadOptions)

    workbook_1.save("FieldStudy.xlsx", SaveFormat.XLSX)
    workbook_2.save("studygroup.xlsx", SaveFormat.XLSX)
