chart = SpectralSequenceChart("Ceta")
chart.set_initial_x_range(0, 40)
chart.set_initial_y_range(0, 20)
chart.set_x_range(0, 80)
chart.set_y_range(0, 40)

A = AdemAlgebra(2)
A.compute_basis(20)
M = FDModule(A, "M", 0)
M.add_generator(0, "x0")
M.add_generator(2, "x2")
M.parse_action("Sq2 x0 = x2", None)
M.freeze()
res_ceta = Resolution("Ceta", chart=chart, module=M)