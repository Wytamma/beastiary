from beastiary.api.core import get_headers


def test_get_mr_bayes() -> None:
    path = "tests/data/mr_bayes.p"
    last_byte, headers_line = get_headers(path=path, delimiter="\t")
    assert (
        headers_line
        == "state\tLnL\tLnPr\tTL\tr(A<->C)\tr(A<->G)\tr(A<->T)\tr(C<->G)\tr(C<->T)\tr(G<->T)\tpi(A)\tpi(C)\tpi(G)\tpi(T)\talpha\tpinvar"
    )
    assert last_byte == 124

def test_get_space_in_name() -> None:
    path = "tests/data/space.in.name.log"
    last_byte, headers_line = get_headers(path=path, delimiter="\t")
    assert (
        headers_line
        == "state\tjoint\tprior\tlikelihood\tLocation.clock.rate\tLocation.meanRate\tCurrent Tree\tLocation.rates.California.NewYork\tLocation.rates.California.Other\tLocation.rates.NewYork.Other\tLocation.indicators.California.NewYork\tLocation.indicators.California.Other\tLocation.indicators.NewYork.Other\tLocation.nonZeroRates\tLocation.branchRates\tc_California_reward[1]\tc_NewYork_reward[1]\tc_Other_reward[1]\tc_allTransitions[1]"
    )
    assert last_byte == 693