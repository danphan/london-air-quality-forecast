## Overview

In this repo, I scraped online air quality data from the [London Air Quality Network](https://www.londonair.org.uk/london/asp/datadownload.asp), published online by Imperial College London.

### Anomaly Detection

In my EDA of the data, I also performed an analysis similar to what was done by [Zoest et al. (2018)](https://link.springer.com/article/10.1007/s11270-018-3756-7) to look for outliers in the air quality data. These outliers correspond to days with especially bad (or good) air quality. My outlier analysis takes into account the different types of site monitors, the seasonality of the data, and the long-tail-nature of the air quality distributions.

### Data Imputation

This real-world data has many missing values, which need to be imputed prior to forecasting. Here, I impute missing values which is most easily understood via the following example:  assume you have a site by the side of the road (i.e. it is in the Roadside class), and it is missing the NO2 concentration on 01/01/2010. Then its value is imputed by calculating the average NO2 concentrations of all other Roadside sites on the same date (01/01/2010.) In the future, I plan to update this imputation method by only averaging over nearest-neighbor sites of the same class, to more accurately include the geographic distribution.

### Air Quality Forecasting
Using this imputed data, I constructed and trained machine learning (linear, dense, and LSTM) models to forecast air quality. In the future, I plan to also take into account the geographic distibution of the sites, modeling the data using a graph neural network.

### Causal Inference and Hypothesis Testing

I also used this imputed data to perform causal inference, using Google's Causal Impact hypothesis testing to see if London's institution of ultra-low-emission zones (ULEZ) in the city center in 2019 led to statistically better air quality afterwards.

### Future Work

Other possible future avenues:
* Supplementing the forecast to take as input meterological data (wind speed, temperature, sunniness.)
* Using an SARIMA model rather than a deep learning model.
* Using a pretrained forecasting model and fine-tuning it on our data.

