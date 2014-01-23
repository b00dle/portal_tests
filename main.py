#!/usr/bin/python

import avango
import avango.script
from avango.script import field_has_changed
import avango.gua
import time
import math

import examples_common.navigator
from examples_common.GuaVE import GuaVE

import simple_scene
import simple_room

simplescene = simple_scene.create()
simpleroom = simple_room.create()

class UpdatePortalTransform(avango.script.Script):

  PortalTransformIn = avango.gua.SFMatrix4()
  ViewTransformIn = avango.gua.SFMatrix4()
  ScreenTransformIn = avango.gua.SFMatrix4()
  ViewTransformOut = avango.gua.SFMatrix4()

  def evaluate(self):
    self.ViewTransformOut.value = avango.gua.make_inverse_mat(self.PortalTransformIn.value) * \
                                  self.ScreenTransformIn.value * self.ViewTransformIn.value


class PortalUser(avango.script.Script):

	UserPositionIn = avango.gua.SFMatrix4()

	def __init__(self):
		self.super(PortalUser).__init__()

	def my_constructor(self, VIEWER, PORTAL, NAV_NODE):
		
		self.VIEWER = VIEWER
		self.PORTAL = PORTAL
		self.PORTAL_POSITION = PORTAL.Transform.value
		self.NAV_NODE = NAV_NODE

		self.switched = False

	def evaluate(self): 
		# calculate distance player to portal
		_pos_p1 = self.UserPositionIn.value.get_translate()
		_pos_p2 = self.PORTAL_POSITION.get_translate()

		_distance = math.sqrt(math.pow(_pos_p1.x - _pos_p2.x, 2) + math.pow(_pos_p1.y - _pos_p2.y, 2) + math.pow(_pos_p1.z - _pos_p2.z, 2))

		if _distance < 1.0 and self.switched == False:
			
			switch_scene(self.VIEWER)

			self.switched = True

			# create a new navigator
			_navigator = examples_common.navigator.Navigator()
			_nav_node = simpleroom["/screen"]
			_nav_node.Transform.value = self.PORTAL_POSITION

			_navigator.StartLocation.value = _nav_node.Transform.value.get_translate()
			_navigator.OutTransform.connect_from(_nav_node.Transform)

			_navigator.RotationSpeed.value = 0.2
			_navigator.MotionSpeed.value = 0.04

			_nav_node.Transform.connect_from(_navigator.OutTransform)

			# TODO:
			# Append new Portal to new scene
			# Change Portal Updater



def switch_scene(VIEWER):
	
	# Exchange cameras of the two scenes
	
	camera_scene = avango.gua.nodes.Camera(LeftEye = "/screen/head" + "/mono_eye",
																		RightEye = "/screen/head" + "/mono_eye",
																		LeftScreen = "/screen",
																		RightScreen = "/screen",
																		SceneGraph = "SimpleRoom")

	VIEWER.Pipelines.value[0].Camera.value = camera_scene


	camera_room = avango.gua.nodes.Camera(LeftEye = "/screen/head" + "/mono_eye",
																		RightEye = "/screen/head" + "/mono_eye",
																		LeftScreen = "/screen",
																		RightScreen = "/screen",
																		SceneGraph = "SimpleScene")

	VIEWER.Pipelines.value[0].PreRenderPipelines.value[0].Camera.value = camera_room


def create_pipeline(SCENE, ROOM, NAME):
	width = 1920;
	height = int(width * 9.0 / 16.0)
	size = avango.gua.Vec2ui(width, height)

	# Camera for Portal Room Scene
	room_camera = avango.gua.nodes.Camera(LeftEye = "/screen/head" + "/mono_eye",
																		RightEye = "/screen/head" + "/mono_eye",
																		LeftScreen = "/screen",
																		RightScreen = "/screen",
																		SceneGraph = ROOM)

	pre_pipe = avango.gua.nodes.Pipeline(Camera = room_camera,
																				OutputTextureName = "room")

	pre_pipe.LeftResolution.value  = avango.gua.Vec2ui(width/2, height/2)
	pre_pipe.EnableStereo.value = False
	pre_pipe.BackgroundTexture.value = "data/textures/sky.jpg"

	# Camera for main scene
	camera = avango.gua.nodes.Camera(LeftEye = "/screen/head" + "/mono_eye",
																		RightEye = "/screen/head" + "/mono_eye",
																		LeftScreen = "/screen",
																		RightScreen = "/screen",
																		SceneGraph = SCENE)

	window =  avango.gua.nodes.Window()

	window.Size.value = size
	window.LeftResolution.value = size
	window.EnableVsync.value = True

	pipe = avango.gua.nodes.Pipeline(Window = window, Camera = camera, Name = NAME)
	# set skybox
	pipe.BackgroundTexture.value = "data/textures/sky.jpg"
	pipe.EnableStereo.value = False
	pipe.EnableBackfaceCulling.value = False

	pipe.PreRenderPipelines.value = [pre_pipe]

	return pipe


def start():
	avango.gua.load_shading_models_from("data/materials")
	avango.gua.load_materials_from("data/materials")

	# Quat to texture with portal view
	portal = avango.gua.nodes.TexturedQuadNode(Name = "portal",
																							Texture = "room",
																							Width = 1.6,
																							Height = 0.9)

	portal.Transform.value = avango.gua.make_trans_mat(0,2.5,2.0) *\
														avango.gua.make_rot_mat(-90.0, 0, 1, 0) *\
														avango.gua.make_scale_mat(2.0,6.0,2.0)

	simplescene.Root.value.Children.value.append(portal)

	# Portal updater for angle of view
	#portal_updater = UpdatePortalTransform()
	#portal_updater.PortalTransformIn.connect_from(portal.Transform)
	#portal_updater.ViewTransformIn.connect_from(simplescene["/screen/head"].Transform)
	#portal_updater.ScreenTransformIn.connect_from(simplescene["/screen"].Transform)
	#simpleroom["/screen/head"].Transform.connect_from(portal_updater.ViewTransformOut)

	# create pipeline, portal and frame
	pipe = create_pipeline("SimpleScene", "SimpleRoom", "firstpipe")

	# create navigator
	navigator = examples_common.navigator.Navigator()
	nav_node = simplescene["/screen"]
	nav_node.Transform.value = avango.gua.make_trans_mat(2.0,3.0,0.0)

	navigator.StartLocation.value = nav_node.Transform.value.get_translate()
	navigator.OutTransform.connect_from(nav_node.Transform)

	navigator.RotationSpeed.value = 0.2
	navigator.MotionSpeed.value = 0.04

	nav_node.Transform.connect_from(navigator.OutTransform)

	viewer = avango.gua.nodes.Viewer()
	viewer.Pipelines.value = [pipe]
	viewer.SceneGraphs.value = [simpleroom,simplescene]

	# If user ist near portal --> change the scene
	portal_user = PortalUser()
	portal_user.my_constructor(viewer, portal, nav_node)
	portal_user.UserPositionIn.connect_from(nav_node.Transform)

	guaVE = GuaVE()
	guaVE.start(locals(), globals())

	viewer.run()

if __name__ == '__main__':
	start()