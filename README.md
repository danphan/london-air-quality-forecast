## Overview

In this repo, I scraped online air quality data from the [London Air Quality Network](https://www.londonair.org.uk/london/asp/datadownload.asp), published online by Imperial College London.

In my EDA of the data, I also performed an analysis similar to what was done by [Zoest et al. (2018)](https://link.springer.com/article/10.1007/s11270-018-3756-7) to look for outliers in the air quality data. These outliers correspond to days with especially bad (or good) air quality. My outlier analysis takes into account the different types of site monitors, the seasonality of the data, and the long-tail-nature of the air quality distributions.

This real-world data has many missing values, which I impute using a custom procedure similar to the outlier analysis, taking into account the yearly and weekly seasonality of the data. In the future, I plan to impute missing data from a site using its (geographical) nearest-neighbor sites.

Using this data, I constructed and trained machine learning (linear, dense, and LSTM) models to forecast air quality. In the future, I plan to also take into account the geographic distibution of the sites, modeling the data using a graph neural network.

Other possible future avenues:
* Supplementing the forecast to take as input meterological data (wind speed, temperature, sunniness.)
* Using an SARIMA model rather than a deep learning model.
* Using a pretrained forecasting model and fine-tuning it on our data.
* London instituted ultra-low-emission zones (ULEZ) in the city center on Apr. 8, 2019. I would like to perform causality analysis to see if this policy led to a statistically lower emissions in these zones.

