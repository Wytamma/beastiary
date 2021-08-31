from beastiary.api import api as app


app.security = True
app.token = "testing"
app.debug = True

headers = {"Authorization": "Bearer testing"}

hcv_coal_first_sample = {
    "state": 0,
    "posterior": -26416.73102683076,
    "likelihood": -26004.576066279948,
    "prior": -412.15496055081064,
    "treeLikelihood": -26004.576066279948,
    "TreeHeight": 4.746566858271142,
    "freqParameter.1": 0.25,
    "freqParameter.2": 0.25,
    "freqParameter.3": 0.25,
    "freqParameter.4": 0.25,
    "rateAC": 1,
    "rateAG": 1,
    "rateAT": 1,
    "rateCG": 1,
    "rateGT": 1,
    "gammaShape": 1,
    "BayesianSkyline": -368.4895759023938,
    "bPopSizes.1": 380,
    "bPopSizes.2": 380,
    "bPopSizes.3": 380,
    "bPopSizes.4": 380,
    "bGroupSizes.1": 16,
    "bGroupSizes.2": 16,
    "bGroupSizes.3": 15,
    "bGroupSizes.4": 15,
}

ebola_first_sample = {
    "state": 0,
    "posterior": -421.4679099978924,
    "likelihood": None,
    "prior": -421.4679099978924,
    "treeLikelihood": None,
    "TreeHeight": 1.3155311776202367,
    "gammaShape": 1,
    "rateAC": 1,
    "rateAG": 1,
    "rateAT": 1,
    "rateCG": 1,
    "rateGT": 1,
    "ucldMean": 1,
    "ucldStdev": 0.1,
    "rate.mean": 1.0209433737704565,
    "rate.variance": 0.010004652847914096,
    "rate.coefficientOfVariation": 0.10006688104941282,
    "CoalescentExponential": -402.4690777041903,
    "ePopSize": 0.3,
    "growthRate": 0.0003,
    "freqParameter.1": 0.25,
    "freqParameter.2": 0.25,
    "freqParameter.3": 0.25,
    "freqParameter.4": 0.25,
}
