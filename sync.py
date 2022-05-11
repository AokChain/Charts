from apscheduler.schedulers.blocking import BlockingScheduler
from service.sync import sync_price

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    scheduler.add_job(sync_price, "interval", minutes=1)

    scheduler.start()
