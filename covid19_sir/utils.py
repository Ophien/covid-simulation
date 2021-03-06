import matplotlib.pyplot as plt
import pandas as pd
from model import CovidModel, Location, get_parameters

class SimpleLocation(Location):
    def __init__(self, unique_id, model, size, **kwargs):
        super().__init__(unique_id, model, size)
        
class BasicStatistics():
    def __init__(self, model):
        self.susceptible = []
        self.infected = []
        self.recovered = []
        self.hospitalization = []
        self.icu = []
        self.death = []
        self.cycles_count = 0
        self.covid_model = model

    def start_cycle(self, model):
        self.cycles_count += 1
        pop = model.total_population
        s1 = s2 = s3 = s4 = s5 = s6 = 0
        for location in model.locations:
            s1 += location.susceptible_count
            s2 += location.infected_count
            s3 += location.recovered_count
            s4 += location.moderate_severity_count
            s5 += location.high_severity_count
            s6 += location.death_count
        self.susceptible.append(s1 / pop)
        self.infected.append(s2 / pop)
        self.recovered.append(s3 / pop)
        self.hospitalization.append((s4 + s5) / pop)
        self.icu.append(s5 / pop)
        self.death.append(s6 / pop)

    def end_cycle(self, model):
        pass

    def export_chart(self, fname):
        df = pd.DataFrame(data={
            'Susceptible': self.susceptible,
            'Infected': self.infected,
            'Recovered': self.recovered,
            'Death': self.death,
            'Hospitalization': self.hospitalization,
            'Severe': self.icu
        })
        color = {
            'Susceptible' : 'lightblue',
            'Infected': 'gray',
            'Recovered': 'lightgreen',
            'Death': 'black',
            'Hospitalization': 'orange',
            'Severe': 'red'
        }
        fig, ax = plt.subplots()
        ax.set_title('Contagion Evolution')
        ax.set_xlim((0, self.cycles_count))
        ax.axhline(y=get_parameters().hospitalization_capacity, c="black", ls='--', label='Critical limit')
        for col in df.columns.values:
            ax.plot(df.index.values, df[col].values, c=color[col], label=col)
        ax.set_xlabel("Days")
        ax.set_ylabel("% of Population")
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='upper right')
        fig.savefig(fname)

    def export_csv(self, fname):
        df = pd.DataFrame(data={
            'Susceptible': self.susceptible,
            'Infected': self.infected,
            'Recovered': self.recovered,
            'Death': self.death,
            'Hospitalization': self.hospitalization,
            'Severe': self.icu
        })
        df.to_csv(fname)
