def pytest_addoption(parser):
    parser.addoption(
        "--iterations",
        action="store",
        type=int,
        default=1,
        help="How many times to repeat tests that accept the 'iteration' fixture.",
    )

def pytest_generate_tests(metafunc):
    iters = metafunc.config.getoption("--iterations")
    if "iteration" in metafunc.fixturenames:
        metafunc.parametrize("iteration", range(1, iters + 1))
