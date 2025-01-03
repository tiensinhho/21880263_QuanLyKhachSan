from models.database import Database


class Report:
    @staticmethod
    def get_monthly_report(month, year, areas=[]):
        where = ""
        if len(areas) > 0:
            list_area = ""
            list_area = ",".join(str(area["Area_Id"]) for area in areas)
            where = f"and a.Id in ({list_area})"
        query = f"select c.Name as 'CategoryName', sum(b.Total) as 'Income' from Bookings b join Rooms r on b.Room_Id = r.Id join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id join Categories c on r.Category_Id = c.Id where b.Status = 'paid' and month(b.CheckInDate) = {month} and year(b.CheckInDate) = {year} {where} group by c.name"
        return Database.execute_query(query)

    @staticmethod
    def get_annual_report(year, areas=[]):
        where = ""
        if len(areas) > 0:
            list_area = ""
            list_area = ",".join(str(area["Area_Id"]) for area in areas)
            where = f"and a.Id in ({list_area})"
        query = f"select month(b.CheckInDate) as 'Month', sum(b.Total) as 'Income' from Bookings b join Rooms r on b.Room_Id = r.Id join Floors f on r.Floor_Id = f.Id join Areas a on f.Area_Id = a.Id where b.Status = 'paid' and year(b.CheckInDate) = {year} {where} group by month(b.CheckInDate)"
        return Database.execute_query(query)
