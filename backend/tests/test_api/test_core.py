from beastiary.api.core import get_headers


def test_get_mr_bayes() -> None:
    path = "tests/data/mr_bayes.p"
    last_byte, headers_line = get_headers(path=path)
    assert (
        headers_line
        == "state LnL LnPr TL r(A<->C) r(A<->G) r(A<->T) r(C<->G) r(C<->T) r(G<->T) pi(A) pi(C) pi(G) pi(T) alpha pinvar"
    )
    assert last_byte == 124
