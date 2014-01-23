import avango
import avango.gua

def create():

	graph = avango.gua.nodes.SceneGraph(Name = "SimpleScene")

	loader = avango.gua.nodes.GeometryLoader()


	# create light
	spot = avango.gua.nodes.SpotLightNode(Name = "sun",
																				Color = avango.gua.Color(1.0, 1.0, 1.0),
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
	plane = loader.create_geometry_from_file('floor', 'data/objects/plane.obj', 'Stones', avango.gua.LoaderFlags.DEFAULTS)
	plane.Transform.value = avango.gua.make_scale_mat(20,1,20)

	graph.Root.value.Children.value.append(plane)

	# screen
	screen = avango.gua.nodes.ScreenNode(Name = "screen", Width = 3.0, Height = 1.97)

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