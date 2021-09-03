def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_graph_utils_graph_info():
    import cfpq_data
    from project import graph_utils

    g = cfpq_data.labeled_binomial_graph(10, 0.5, verbose=False)
    g_info = graph_utils.get_graph_info(g)
    assert g.number_of_edges() == g_info.edges
    assert g.number_of_nodes() == g_info.vertices
    assert cfpq_data.get_labels(g) == g_info.labels


def test_graph_utils_2():
    import cfpq_data
    from project import graph_utils

    graph_utils.generate_and_save_two_cycle(
        10, 4, ("x", "y"), "../res/test_graph_utils_2.dot"
    )
