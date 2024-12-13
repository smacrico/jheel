import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Create a sample data structure for tracking multiple sessions
class RunningAnalysis:
    def __init__(self):
        self.training_log = pd.DataFrame(columns=[
            'date', 'running_economy', 'vo2max', 'distance', 
            'time', 'heart_rate', 'efficiency_score', 'energy_cost'
        ])
    
    def add_session(self, date, running_economy, vo2max, distance, time, heart_rate):
        efficiency_score = self.calculate_efficiency(running_economy, vo2max)
        energy_cost = self.calculate_energy_cost(running_economy, distance, time)
        
        new_session = pd.DataFrame({
            'date': [date],
            'running_economy': [running_economy],
            'vo2max': [vo2max],
            'distance': [distance],
            'time': [time],
            'heart_rate': [heart_rate],
            'efficiency_score': [efficiency_score],
            'energy_cost': [energy_cost]
        })
        
        self.training_log = pd.concat([self.training_log, new_session], ignore_index=True)
    
    def calculate_efficiency(self, running_economy, vo2max):
        return running_economy / vo2max
    
    def calculate_energy_cost(self, running_economy, distance, time):
        # Energy cost in calories per kilometer
        return running_economy * (distance / time)
    
    def visualize_trends(self):
        plt.figure(figsize=(15, 10))
        
        # Plot 1: Running Economy over time
        plt.subplot(2, 2, 1)
        plt.plot(self.training_log['date'], self.training_log['running_economy'], 'b-o')
        plt.title('Running Economy Trend')
        plt.xticks(rotation=45)
        plt.ylabel('Running Economy')
        
        # Plot 2: Efficiency Score over time
        plt.subplot(2, 2, 2)
        plt.plot(self.training_log['date'], self.training_log['efficiency_score'], 'g-o')
        plt.title('Efficiency Score Trend')
        plt.xticks(rotation=45)
        plt.ylabel('Efficiency Score')
        
        # Plot 3: Energy Cost vs Distance
        plt.subplot(2, 2, 3)
        plt.scatter(self.training_log['distance'], self.training_log['energy_cost'])
        plt.title('Energy Cost vs Distance')
        plt.xlabel('Distance (km)')
        plt.ylabel('Energy Cost')
        
        # Plot 4: Heart Rate vs Running Economy
        plt.subplot(2, 2, 4)
        plt.scatter(self.training_log['heart_rate'], self.training_log['running_economy'])
        plt.title('Heart Rate vs Running Economy')
        plt.xlabel('Heart Rate (bpm)')
        plt.ylabel('Running Economy')
        
        plt.tight_layout()
        plt.show()

# Example usage:
analysis = RunningAnalysis()

# Adding sample data (you would replace this with your actual data)
# Using your current session data (RE: 73, VO2Max: 19.0)
analysis.add_session(
    date=datetime.now(),
    running_economy=73,
    vo2max=19.0,
    distance=5,  # example distance in km
    time=27,     # from your data: 27 minutes
    heart_rate=150  # example heart rate
)

# Add more sessions with different values to see trends
# This is example data - you would use your actual historical data
for i in range(5):
    analysis.add_session(
        date=datetime.now() - pd.Timedelta(days=i*7),
        running_economy=73 - i,  # Simulating improvement
        vo2max=19.0 + (i*0.2),
        distance=5 + i,
        time=27 - i,
        heart_rate=150 - i
    )

# Visualize the trends
analysis.visualize_trends()

# Additional analysis function for training zones
def calculate_training_zones(running_economy, vo2max):
    zones = {
        'Recovery': (0.6 * running_economy, 0.7 * running_economy),
        'Endurance': (0.7 * running_economy, 0.8 * running_economy),
        'Tempo': (0.8 * running_economy, 0.9 * running_economy),
        'Threshold': (0.9 * running_economy, running_economy),
        'VO2Max': (running_economy, 1.1 * running_economy)
    }
    return zones

# Print training zones based on current data
training_zones = calculate_training_zones(73, 19.0)
print("\nTraining Zones based on Running Economy:")
for zone, (lower, upper) in training_zones.items():
    print(f"{zone}: {lower:.1f} - {upper:.1f}")