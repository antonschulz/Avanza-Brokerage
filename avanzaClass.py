#! python
import pandas as pd
import re

# Columns= ['Datum', 'Konto', 'Typ av transaktion', 'Värdepapper/beskrivning',
# 'Antal', 'Kurs', 'Belopp', 'Courtage', 'Valuta', 'ISIN']

# TODO: stockBrokerage should not return stock if brokerage < zero but it does
# TODO: depositsmonthlygraph doesnt take specific days, only months


class Avanza:
    def __init__(self, file):
        self.rawData = rawData = pd.read_csv(file, sep=";")
        # dates and brokerage-fee dataframe
        self.courtageDF = self.courtageDF()

    def getFileDates(self):
        data = self.rawData.set_index("Datum")
        startDate = str(data.index.values[1])
        endDate = str(data.index.values[::-1][0])
        return startDate, endDate

    # drops unneccessary columns for calculating brokerage fee("Courtage")
    def courtageDF(self):
        courtage = self.rawData.drop(columns=[
            'Konto', 'Typ av transaktion','Antal', 'Kurs', 'Belopp', 'Valuta', 'ISIN']).set_index("Datum")

        courtage["Courtage"] = courtage["Courtage"].apply(lambda x: x.replace("-","0"))
        courtage["Courtage"] = courtage["Courtage"].apply(lambda x: float(x.replace(",",".")))
        return courtage

    # each individual stock's brokerage-fee is summed up for the inserted time period
    def stockBrokerage(self, startDate, endDate):
        stockBrokerage = self.courtageDF.loc[endDate:startDate].\
                          groupby('Värdepapper/beskrivning').sum()
        stockBrokerage = stockBrokerage.sort_values(by=["Courtage"], ascending=False)
        return stockBrokerage

    # Creates dataframe with cumulative brokerage fee for selected timeperiod
    def courtageGraph(self, startDate, endDate):
        data = self.courtageDF.drop(columns=["Värdepapper/beskrivning"])
        data = data.groupby(["Datum"]).sum()
        data = data.loc[startDate:endDate]
        data["Courtage"] = data["Courtage"].cumsum()
        return data
    
    def depositsDF(self):
        data = self.rawData.drop(columns=[
            'Konto', 'Värdepapper/beskrivning', 'Antal', 'Kurs', 'Courtage', 'Valuta', 'ISIN'])

        data = data.loc[
            (data["Typ av transaktion"] == "Insättning")
            | # Deposits OR withdrawal
            (data["Typ av transaktion"] == "Uttag")]

        data["Belopp"] = data["Belopp"].apply(
            lambda x: float(x.replace(",",".")))

        return data

    # Dataframe for monthly deposits
    def depositsMonthlyGraph(self, startDate, endDate):
        data = self.depositsDF()
        # Convert %Y-%m-%d into %Y-%m format
        data["Datum"] = data["Datum"].apply(
            lambda x: x[:-3])

        data = data.groupby("Datum").apply(sum)
        data = data.drop(columns=[
            "Datum", "Typ av transaktion"])
        data = data.loc[startDate:endDate] # move this up and change to navigate in datum column
        return data

    def depositsLineData(self, startDate, endDate):
        data = self.depositsDF()
        data = data.groupby(["Datum"]).sum()
        data = data.loc[startDate:endDate]
        data["Belopp"] = data["Belopp"].cumsum()
        return data

