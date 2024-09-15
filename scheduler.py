from apscheduler.schedulers.background import BackgroundScheduler
from backend.data_collection import collect_data

def update_data():
    # Example function to update data
    competitors = ["CompanyA", "CompanyB"]
    industry = "Tech"
    collect_data(competitors, industry)
    print("Data updated")

scheduler = BackgroundScheduler()
scheduler.add_job(update_data, 'interval', minutes=60)
scheduler.start()
