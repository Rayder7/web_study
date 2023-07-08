""" from api.admin import FieldStudyResource, StudyGroupResource
import jpype
import asposecells
jpype.startJVM()
from asposecells.api import Workbook, LoadOptions, SaveFormat


datafieldstudy = FieldStudyResource().export()
dataStudygroup = StudyGroupResource().export()
workbook_1 = Workbook("datafieldstudy", LoadOptions)
workbook_2 = Workbook("datastudygroup", LoadOptions)


def make_excel():
    workbook_1.save("FieldStudy.xlsx", SaveFormat.XLSX)
    workbook_2.save("studygroup.xlsx", SaveFormat.XLSX)
 """