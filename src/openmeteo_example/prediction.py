# -*- coding: utf-8 -*-
"""
Created on Thurs May 16 2025 09:56

@author: samhill

Using data science techniques to predict what the weather will be
in the future.
"""

from openmeteo_example import MeteoHistorical
import torch
import torch.nn as nn
import datetime as dt
from torch.optim import Adam
from tqdm.notebook import trange


class WeatherPredictor(nn.Module):
    def __init__(self, weather_data: MeteoHistorical) -> None:
        """Initialises object by reading in data"""
        super().__init__()

        self.weather = weather_data

        # We'll use the last 7 days of data
        days = 7
        hours = 24
        meas = 4

        # Define model architecture
        self.fc1 = nn.Linear(days * hours * meas, 4096)
        self.fc2 = nn.Linear(4096, 512)
        self.fc3 = nn.Linear(512, 750)
        self.fc4 = nn.Linear(750, 24)
        self.activation = nn.ReLU()

    def _select_training_data(self, day: dt.datetime) -> torch.tensor:
        """Selects appropriate data (7 days worth) for model"""
        # Find index of day
        datetimes = self.weather.temperature[0]
        day_index = datetimes.index(day)

        # Create tensor to hold data - we'll use last 7 days of data
        days = 7
        hours = 24
        meas = 4
        data = torch.empty(days * hours * meas)

        # Iterate through Temperature, Cloud Cover, Precipitation and Windspeed
        start_index = day_index - days * hours
        for i, meas in enumerate(self.weather._measures.keys()):
            start = i * days * hours
            end = start + days * hours
            buff = self.weather._return_data(meas)[1][start_index:day_index]
            data[start:end] = torch.Tensor(buff)

        return data

    def _select_label_data(self, day: dt.datetime) -> torch.tensor:
        """Select temperature data for that day"""
        # Find index of day
        datetimes = self.weather.temperature[0]
        day_index = datetimes.index(day.replace(hour=0, minute=0, second=0))

        dat = torch.Tensor(self.weather.temperature[1][day_index : day_index + 24])
        return dat

    def forward(self, day: dt.datetime) -> torch.tensor:
        """Define the model architecture showing the
        forward propagation of the model
        """
        # Select data
        data = self._select_training_data(day)
        buff = self.activation(self.fc1(data))
        buff = self.activation(self.fc2(buff))
        buff = self.activation(self.fc3(buff))
        result = self.fc4(buff)

        return result.squeeze()

    def save_model(self, path: str) -> None:
        """Saves model weights to disk to allow for use later on"""
        torch.save(self.state_dict(), path)

    def load_model(self, path: str) -> None:
        """Retrieves model parameters from disk"""
        self.load_state_dict(torch.load(path, weights_only=True))
        self.eval()


def perm_cpu(pop_size: int, num_samples: int) -> torch.Tensor:
    """Chooses num_samples at random from a population size of pop_size."""
    return torch.randperm(pop_size)[:num_samples]


# Also create function to optimise parameters
def train_model(
    days: torch.utils.data.Subset, model: WeatherPredictor, n_epochs: int = 50
) -> tuple[WeatherPredictor, list[float]]:
    """Function to optimise parameters of neural network"""
    # Define stocastic gradient descent optimiser with MSE loss
    opt = Adam(model.parameters(), lr=0.0001)
    L = nn.MSELoss()

    # Train model
    losses = []

    # Get length of data
    training_size = len(days)

    # Generate training data
    label_data = torch.stack([model._select_label_data(day) for day in days])

    for _ in trange(n_epochs):
        # Choose subset of data
        rand_inds = perm_cpu(training_size, training_size // n_epochs)
        epoch_days = [days[idx] for idx in rand_inds]

        # Calculate current predictions
        input_data = torch.stack([model(day) for day in epoch_days])

        # Compute current loss
        loss_value = L(input_data, label_data[rand_inds])

        # Compute gradient via backwards propagation and optimize
        opt.zero_grad()
        loss_value.backward()
        opt.step()

        # Append loss value to list
        losses.append(loss_value.item())

    return model, losses
