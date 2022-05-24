from fastapi.testclient import TestClient
from beastiary import crud
from beastiary.schemas import TreeCreate
from .utils import app, headers
from beastiary.api.core import add_tree


client = TestClient(app)

path = "tests/data/test.trees"

tree = add_tree(client.app.db, TreeCreate(path=path))


def test_no_tree() -> None:
    response = client.get("/api/trees/100/samples", headers=headers)
    assert response.status_code == 404


def test_get_sample() -> None:
    response = client.get(f"/api/trees/{tree['id']}/samples", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert json[0]["tree_id"] == tree["id"]
    assert (
        json[0]["newick"]
        == """((((((((((((((((((((((1[&type="NewZealand"]:0.3067539819241729)120[&type="HongKong"]:0.05026628906461594,54[&type="HongKong"]:0.2693490409887198)74[&type="HongKong"]:0.11743489528252415,((((9[&type="NewZealand"]:0.22710629273151328)122[&type="HongKong"]:0.02031699690660982,((34[&type="HongKong"]:0.07650146241489358,(39[&type="HongKong"]:0.012902982960001086,48[&type="HongKong"]:0.24030024296008995)63[&type="HongKong"]:0.03072175945478861)64[&type="HongKong"]:0.12856677646507958,38[&type="HongKong"]:0.16945179887996065)67[&type="HongKong"]:0.2423550507581954)69[&type="HongKong"]:0.2643228323216714,31[&type="HongKong"]:0.1364036519597167)71[&type="HongKong"]:0.12514954828358538,35[&type="HongKong"]:0.050594300243378854)73[&type="HongKong"]:0.32523073602798735)75[&type="HongKong"]:0.08723786889897722,(((36[&type="HongKong"]:0.12561692330279084,56[&type="HongKong"]:0.024247063302813787)72[&type="HongKong"]:0.0968335499433628)150[&type="NewZealand"]:0.20955667835655323)151[&type="HongKong"]:0.17352150356756502)76[&type="HongKong"]:0.39739308375688376,(7[&type="NewZealand"]:0.45209083383583093)121[&type="HongKong"]:0.4522007650912563)77[&type="HongKong"]:0.43177927932187554,((50[&type="HongKong"]:0.29484871160966364)142[&type="NewZealand"]:0.4377311317814421)143[&type="HongKong"]:0.48568281485794174)84[&type="HongKong"]:0.23619653070908608,((((((((((16[&type="NewZealand"]:0.08835763659582711)127[&type="HongKong"]:0.2889451273986475,32[&type="HongKong"]:0.2512753639945902)65[&type="HongKong"]:0.02716934975737717,37[&type="HongKong"]:0.2592666337518931)66[&type="HongKong"]:0.30867305744156465)144[&type="NewZealand"]:0.3090802849012291)145[&type="HongKong"]:0.4231407950550712)146[&type="NewZealand"]:0.715606280722479)147[&type="HongKong"]:0.2855849134948545,(22[&type="NewZealand"]:0.04921728652365065)129[&type="HongKong"]:0.17268262884356833)85[&type="HongKong"]:0.0636655479499666,41[&type="HongKong"]:0.006113403317145938)87[&type="HongKong"]:0.014414242136541855,51[&type="HongKong"]:0.3684728554537222)88[&type="HongKong"]:0.08324661350450269)89[&type="HongKong"]:0.17487804965113352,57[&type="HongKong"]:0.1033098486091859)91[&type="HongKong"]:0.711281663813955)153[&type="NewZealand"]:0.32590596746840816)154[&type="HongKong"]:0.04198613876408386,(((12[&type="NewZealand"]:0.3562296752378935)126[&type="HongKong"]:0.2822233686788054,59[&type="HongKong"]:0.19735715391665654)90[&type="HongKong"]:1.0543496879406575,52[&type="HongKong"]:0.13389862185739876)98[&type="HongKong"]:0.04584526679843126)100[&type="HongKong"]:0.14615873841367577,(53[&type="HongKong"]:0.14862615512325483,58[&type="HongKong"]:0.24999601512323189)99[&type="HongKong"]:0.18275592194618984)101[&type="HongKong"]:0.13203332736837314,46[&type="HongKong"]:0.00862088443786746)102[&type="HongKong"]:0.14539743208415157,49[&type="HongKong"]:0.4718265365219798)105[&type="HongKong"]:0.25990971852994793,40[&type="HongKong"]:0.055023925051827405)106[&type="HongKong"]:0.3659115743740182,(((((((((2[&type="NewZealand"]:0.10594715810602562,(((13[&type="NewZealand"]:0.839087518121873,((14[&type="NewZealand"]:0.01721796006379711,15[&type="NewZealand"]:0.03091659006370512)61[&type="NewZealand"]:0.4028181421971983,(17[&type="NewZealand"]:0.27820428570190203,30[&type="NewZealand"]:0.21793031570210375)62[&type="NewZealand"]:0.23772222655890418)68[&type="NewZealand"]:0.4491884058609512)70[&type="NewZealand"]:0.03840515383719467)148[&type="HongKong"]:0.19488331980536078)149[&type="NewZealand"]:0.9568588363416333)79[&type="NewZealand"]:0.10880262958655607,6[&type="NewZealand"]:0.2229689676925508)81[&type="NewZealand"]:2.644089344370215E-4,25[&type="NewZealand"]:0.13556214662714616)82[&type="NewZealand"]:0.20233570528296108,(3[&type="NewZealand"]:0.12104389982091845,4[&type="NewZealand"]:0.1511808898209921)83[&type="NewZealand"]:0.18671696208911515)86[&type="NewZealand"]:0.710712229531838,(5[&type="NewZealand"]:0.7743529656004315,((33[&type="HongKong"]:0.7164466273947885,(55[&type="HongKong"]:0.9816870900421577,60[&type="HongKong"]:0.10223504004210326)78[&type="HongKong"]:0.16215679735253774)80[&type="HongKong"]:0.5506234514981108)152[&type="NewZealand"]:0.15659795670758925)92[&type="NewZealand"]:0.2769968358414223)93[&type="NewZealand"]:0.2930502267937536,((24[&type="NewZealand"]:0.2267708449866941)130[&type="HongKong"]:0.03276978396516528)131[&type="NewZealand"]:0.06294159928376519)96[&type="NewZealand"]:0.25422909067857313,27[&type="NewZealand"]:0.4890400789142344)97[&type="NewZealand"]:1.0387468637566153,28[&type="NewZealand"]:0.4647732426707938)107[&type="NewZealand"]:0.07862821187221769)156[&type="HongKong"]:0.0693148648829105)108[&type="HongKong"]:0.3400903562645228,43[&type="HongKong"]:0.7993820256904112)111[&type="HongKong"]:0.49292841897438233,44[&type="HongKong"]:0.1745022246648782)115[&type="HongKong"]:0.4571401728799733)158[&type="NewZealand"]:0.38803199530998445,((((((8[&type="NewZealand"]:0.11245200453613347,(29[&type="NewZealand"]:0.19660951455883158,(47[&type="HongKong"]:0.15123559392239683)141[&type="NewZealand"]:0.07003145063644789)94[&type="NewZealand"]:0.11858221997715024)95[&type="NewZealand"]:0.6132557142648238)155[&type="HongKong"]:0.18929401565026982,(10[&type="NewZealand"]:0.19990215221468866)123[&type="HongKong"]:0.8411269822364229)103[&type="HongKong"]:0.01270688796651065,((45[&type="HongKong"]:0.6618052688209124)139[&type="NewZealand"]:0.14743599703760157)140[&type="HongKong"]:0.030796126559154757)104[&type="HongKong"]:0.7364366228829482,(19[&type="NewZealand"]:0.5043123247588541)128[&type="HongKong"]:0.3077781305418208)109[&type="HongKong"]:1.3258734007977475)157[&type="NewZealand"]:0.28718998675644336)117[&type="NewZealand"]:0.22544836826131665,((((((11[&type="NewZealand"]:0.21546251838511576)124[&type="HongKong"]:0.2759919395808019)125[&type="NewZealand"]:0.16936619874483938,((18[&type="NewZealand"]:0.2722180851380669,26[&type="NewZealand"]:0.2968756251379743)110[&type="NewZealand"]:0.20912240474501864,(20[&type="NewZealand"]:0.23571103522199977,23[&type="NewZealand"]:0.2576288452218769)112[&type="NewZealand"]:0.09494452466118819)113[&type="NewZealand"]:0.3164664668276611)114[&type="NewZealand"]:0.23904593863851442,21[&type="NewZealand"]:0.921784405349376)116[&type="NewZealand"]:0.012156813475789008)159[&type="HongKong"]:0.023052363613247806)160[&type="NewZealand"]:0.8662113686777717)118[&type="NewZealand"]:1.0507331526643524,(((((((42[&type="HongKong"]:0.0567086444534155)132[&type="NewZealand"]:0.004060774179835747)133[&type="HongKong"]:0.02875077348702515)134[&type="NewZealand"]:0.41379794136175363)135[&type="HongKong"]:0.12104358785592417)136[&type="NewZealand"]:1.1849197152423043)137[&type="HongKong"]:1.3770628535257217)138[&type="NewZealand"]:0.21636093367444076)119[&type="NewZealand"]:0.0;"""
    )


def test_get_sample_limit() -> None:
    response = client.get(f"/api/trees/{tree['id']}/samples?limit=1", headers=headers)
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    response = client.get(
        f"/api/trees/{tree['id']}/samples?limit=1000000", headers=headers
    )
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 6
