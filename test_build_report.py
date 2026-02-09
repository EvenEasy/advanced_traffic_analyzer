from bin.advanced_traffic_analyzer import InputNamespace, build_report


def test_build_report():
    inp = InputNamespace(
        filepath = 'test/test_access.log',
        method = None,
        status = None,
        start = None,
        end = None,
        top = 3
    )
    build_report(inp)

test_build_report()
