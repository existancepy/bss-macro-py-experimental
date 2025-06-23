from modules.submacros.hourlyReport import HourlyReport

a = HourlyReport()
a.loadHourlyReportData()
print(a.hourlyReportStats['converting_time'])