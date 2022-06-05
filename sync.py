from apscheduler.schedulers.blocking import BlockingScheduler
from service.sync import sync_transaction, sync_address
from service.sync import sync_price, sync_chart_data
from service.sync import sync_token

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(sync_chart_data, "interval", seconds=10)
    # scheduler.add_job(sync_transaction, "interval", minutes=1)
    # scheduler.add_job(sync_address, "interval", minutes=1)
    # scheduler.add_job(sync_price, "interval", minutes=1)
    scheduler.add_job(sync_token, "interval", seconds=10)

    scheduler.start()
