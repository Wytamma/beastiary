from beastiary.api import api as app


app.security = True
app.token = "testing"
app.debug = True

headers = {"Authorization": "Bearer testing"}
headers_line = "state posterior likelihood prior treeLikelihood TreeHeight freqParameter.1 freqParameter.2 freqParameter.3 freqParameter.4 rateAC rateAG rateAT rateCG rateGT gammaShape BayesianSkyline bPopSizes.1 bPopSizes.2 bPopSizes.3 bPopSizes.4 bGroupSizes.1 bGroupSizes.2 bGroupSizes.3 bGroupSizes.4"
last_byte = 6479
first_sample = {
    "state": 0,
    "data": {
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
    },
    "id": 1,
    "trace_id": 1,
}
