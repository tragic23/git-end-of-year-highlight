from dataclasses import dataclass
import os
from datetime import datetime
import string
from xmlrpc.client import boolean

@dataclass
class Info:
    username: str
    token: str
    maxMonthInt: int
    #maxMonthStr: str
    maxMonthCount:  int
    maxDate: str
    maxDateCount: int
    weekendCount: int
    weekendBadge : boolean


    # Overriding the default constructor entirely
    def __init__(self, token: str):
        self.username = os.getenv("USERNAME")
        self.token = token


    def setCommitData(self, maxMonth, maxMonthCount, maxDate, maxDateCount, totalCommitCount, weekendCount):
        self.maxMonthInt = maxMonth
        self.maxMonthCount = maxMonthCount
        self.maxDateCount = maxDateCount
        self.maxDate = maxDate
        self.maxDateCount = maxDateCount    
        self.totalCommitCount = totalCommitCount
        self.weekendCount = weekendCount

        if(weekendCount > 3):
            self.weekendBadge = True

        match self.maxMonthInt:
           case 1:
               self.maxMonthStr = "January"
           case 2:
               self.maxMonthStr = "February"
           case 3:
               self.maxMonthStr =  "March"
           case 4:
               self.maxMonthStr = "April"
           case 5:
               self.maxMonthStr = "May"
           case 6:
               self.maxMonthStr = "June"
           case 7:
               self.maxMonthStr = "July"
           case 8:
               self.maxMonthStr = "August"
           case 9:
               self.maxMonthStr = "September"
           case 10:
               self.maxMonthStr = "October"
           case 11:
               self.maxMonthStr = "November"
           case 12:
               self.maxMonthStr = "December"
           case _:
               self.maxMonthStr = ""  # The default case


  
      
    def __str__(self):
        msg = ""
        msg += f" {self.username}'s Summary for year 2025\n\n"
        msg += f"Month with the most commits: {self.maxMonthStr}\n"
        msg += f"with {self.maxMonthCount} commits\n\n"
        msg += f"Day with the most commits: {self.maxDate}\n"
        msg += f"with {self.maxDateCount} commits\n\n"
        msg += f"Total commits in the year: {self.totalCommitCount}\n"
       
        if( self.weekendBadge == True):
            msg += f"Number of weekends active on: {self.weekendCount}\n"
            

        return msg

        Commit
