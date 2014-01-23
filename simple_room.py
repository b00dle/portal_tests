import avango
import avango.gua

def create():

	graph = avango.gua.nodes.SceneGraph(Name = "SimpleRoom")

	loader = avango.gua.nodes.GeometryLoader()


	# create light
	spot = avango.gua.nodes.SpotLightNode(Name = "sun",
																				Color = avango.gua.Color(1.0, 0.0, 0.0),
																				Falloff = 0.009,
																				Softness = 0.003,
																				EnableShadows = True,
																				EnableGodrays = False,
																				EnableDiffuseShading = True,
																				EnableSpecularShading = True,
																				ShadowMapSize = 2048,
																				ShadowOffset = 0.001)

	spot.Transform.value = avango.gua.make_trans_mat(0.0, 40.0, 40.0) * \
													avango.gua.make_rot_mat(-45.0, 1.0, 0.0, 0.0) * \
													avango.gua.make_scale_mat(100.0, 100.0, 160.0)

	graph.Root.value.Children.value.append(spot)

	# create floor
	floor = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	floor.Transform.value = avango.gua.make_scale_mat(20,1,20)

	graph.Root.value.Children.value.append(floor)

	# create walls
	wall1 = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	wall1.Transform.value = avango.gua.make_trans_mat(10, 2.5, 0) * \
													avango.gua.make_rot_mat(-90, 1, 0, 0) * \
													avango.gua.make_rot_mat(90, 0, 0, 1) * \
													avango.gua.make_scale_mat(20,1,5)

	graph.Root.value.Children.value.append(wall1)

	wall2 = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	wall2.Transform.value = avango.gua.make_trans_mat(-10, 2.5, 0) * \
													avango.gua.make_rot_mat(-90, 1, 0, 0) * \
													avango.gua.make_rot_mat(90, 0, 0, 1) * \
													avango.gua.make_scale_mat(20,1,5)

	graph.Root.value.Children.value.append(wall2)

	wall3 = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	wall3.Transform.value = avango.gua.make_trans_mat(0, 2.5, 10) * \
													avango.gua.make_rot_mat(-90, 0, 1, 0) * \
													avango.gua.make_rot_mat(90, 0, 0, 1) * \
													avango.gua.make_scale_mat(5,1,20)

	graph.Root.value.Children.value.append(wall3)

	wall4 = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	wall4.Transform.value = avango.gua.make_trans_mat(0, 2.5, -10) * \
													avango.gua.make_rot_mat(-90, 0, 1, 0) * \
													avango.gua.make_rot_mat(90, 0, 0, 1) * \
													avango.gua.make_scale_mat(5,1,20)

	graph.Root.value.Children.value.append(wall4)

	# screen
	screen = avango.gua.nodes.ScreenNode(Name = "screen", Width = 1.6, Height = 0.9)

	screen.Transform.value = avango.gua.make_rot_mat(-90.0, 0, 1, 0) * \
														avango.gua.make_trans_mat(0, 1.5, 0)

	# head, mono_eye, left und right eye
	head = avango.gua.nodes.TransformNode(Name = "head")
	head.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 1.7)

	mono_eye = avango.gua.nodes.TransformNode(Name = "mono_eye")

	left_eye = avango.gua.nodes.TransformNode(Name = "left_eye")
	left_eye.Transform.value = avango.gua.make_trans_mat(-0.05, 0.0, 0.0)

	right_eye = avango.gua.nodes.TransformNode(Name = "right_eye")
	right_eye.Transform.value = avango.gua.make_trans_mat(0.05, 0.0, 0.0)

	head.Children.value = [mono_eye, left_eye, right_eye]

	# head an screen
	screen.Children.value.append(head)
	# screen an root
	graph.Root.value.Children.value.append(screen)

	return graph