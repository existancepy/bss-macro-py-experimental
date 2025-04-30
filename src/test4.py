from modules.submacros.hourlyReport import HourlyReport, BuffDetector

bd = BuffDetector(True, "retina")
h = HourlyReport(bd)
h.generateHourlyReport()