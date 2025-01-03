from models.report_model import Report
from werkzeug.exceptions import BadRequest
from models.room_model import Room

class ReportService:
    def __init__(self):
        self.report_repo=Report()

    def get_monthly_report(self, request, areas=[]):
        month = int(request.get("month", 0))
        year = int(request.get("year", 0))
        if month <= 0 or month > 12 or year <= 1900:
            raise BadRequest('month or year is invalid')
        data={}
        details=Report.get_monthly_report(month, year, areas)
        sum=0
        for item in details:
            sum += item["Income"]
        for item in details:
            item["Percent"]=round(item["Income"]/sum*100, 1)
        data["Details"]=details
        data["Total"]=round(sum, 1)
        return data
    
    def get_annual_report(self, request, areas=[]):
        year = int(request.get("year", 0))
        if int(year) <= 1900:
            raise BadRequest('Year is invalid')
        data={}
        details=Report.get_annual_report(year, areas)
        sum=0
        for item in details:
            sum += item["Income"]
        for item in details:
            item["Percent"]=round(item["Income"]/sum*100, 1)
        data["Details"]=details
        data["Total"]=round(sum, 1)
        return data
