import pandas as pd
from schedule import every, repeat, run_pending
import time, os
from datetime import datetime

link = "https://docs.google.com/spreadsheets/export?id={}&exportFormat=csv"
def get_csv(id): return pd.read_csv(link.format(id))

@repeat(every(1).minute, "your-sheet-id")
def demo(id):
    os.system("cls")
    df = get_csv(id)
    for i in range(len(df)): print(t := df.loc[i].to_dict())
    print('\nFetch at', datetime.now())

demo("your-sheet-id")
while time.sleep(1) or True:
    run_pending()
