from beastiary.api import api as app
from beastiary.db.database import Database


app.security = True
app.token = "testing"
app.debug = True

db = Database()
db.create_table("Trace")
db.create_table("TraceSample")
db.create_table("Tree")
db.create_table("TreeSample")
app.db = db

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


csv_first_sample = {
    "state": 0,
    "joint": -155630.5237,
    "prior": -886.9146445,
    "likelihood": -154743.6091,
    "treeModel.rootHeight": 5.008836179,
    "age(root)": 2016.581164,
    "treeLength": 65.24956578,
    "tmrca(B117)": 1.980307323,
    "tmrca(B1351)": 2.318969125,
    "tmrca(P1)": 3.580619699,
    "tmrca(B16172)": 4.262129944,
    "age(B117)": 2019.609693,
    "age(B1351)": 2019.271031,
    "age(P1)": 2018.00938,
    "age(B16172)": 2017.32787,
    "exponential.popSize": 1,
    "exponential.growthRate": 0,
    "gtr.rates.rateAC": 1,
    "gtr.rates.rateAG": 1,
    "gtr.rates.rateAT": 1,
    "gtr.rates.rateCG": 1,
    "gtr.rates.rateCT": 1,
    "gtr.rates.rateGT": 1,
    "alpha": 0.5,
    "clock.rate": 1,
    "B117.rate": 1,
    "B1351.rate": 1,
    "P1.rate": 1,
    "B16172.rate": 1,
    "meanRate": 1,
    "coefficientOfVariation": 0,
    "covariance": None,
    "treeLikelihood": -154743.6091,
    "branchRates": 0,
    "coalescent": -807.7452903,
}
