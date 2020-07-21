from random import uniform

from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.animation import Animation

from kivy3 import Renderer, Scene
from kivy3 import PerspectiveCamera

from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh


class Cube3D(FloatLayout):

    def __init__(self):
        super().__init__()

        '''create renderer'''
        self.renderer = Renderer()

        '''create scene'''
        scene = Scene()

        '''create default cube for scene'''
        cube_geo = BoxGeometry(1, 1, 1)

        '''color: base color, diffuse: color of "shadows", specular:mirror-like reflections'''
        cube_mat = Material(
            transparency=.9,
            color=(1, .2, 0),
            diffuse=(0, 0, 0),
            specular=(.5, .5, .5))
        self.cube = Mesh(
            geometry=cube_geo,
            material=cube_mat
        )
        self.cube.pos.z = -4
        self.cube.pos.y = .7

        '''create camera for scene, fov:distance from the screen, aspect:screen" ratio, near:nearest rendered point, 
            far:farthest rendered point'''
        self.camera = PerspectiveCamera(
            fov=110,
            aspect=0,
            near=1,
            far=10
        )

        '''start rendering the scene and camera'''
        scene.add(self.cube)
        self.renderer.render(scene, self.camera)

        '''set renderer ratio is its size changes
        e.g. when added to parent'''
        self.renderer.bind(size=self._adjust_aspect)

        self.add_widget(self.renderer)

        label1 = Label(text='EuroLeagueStats', font_size='17sp', color=(1, 1, 1, .8), size_hint=(1, None),
                       pos_hint={'center_x': .5, 'center_y': .70}, halign='center', valign='middle')
        label1.bind(width=lambda *x: label1.setter("text_size")(label1, (label1.width, None)),
                    texture_size=lambda *x: label1.setter("height")(label1, label1.texture_size[1]))

        label2 = Label(text='2019 - 20', font_size='14sp', color=(.4, .4, .4, .8), size_hint=(1, None),
                       pos_hint={'center_x': .5, 'center_y': .62}, halign='center', valign='middle')
        label2.bind(width=lambda *x: label2.setter("text_size")(label2, (label2.width, None)),
                    texture_size=lambda *x: label2.setter("height")(label2, label2.texture_size[1]))

        label3 = Label(text='`Monolith`', font_size='16sp', color=(.4, .4, .4, .7), size_hint=(1, None),
                       pos_hint={'center_x': .5, 'center_y': .66}, halign='center', valign='middle')
        label3.bind(width=lambda *x: label3.setter("text_size")(label3, (label3.width, None)),
                    texture_size=lambda *x: label3.setter("height")(label3, label3.texture_size[1]))

        for label in [label1, label2, label3]:
            self.add_widget(label)

        Clock.schedule_interval(self.rotate_cube, .01)
        Clock.schedule_interval(self.scale_cube, 1)

    def update_rect(self, *args):
        self.rect.size = self.size

    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def rotate_cube(self, *dt):
        self.cube.rotation.y += .7
        self.cube.rotation.x += .7

    def scale_cube(self, *dt):
        factor = uniform(1.05, 1.25)

        anim = Animation(x=factor)
        anim &= Animation(y=factor)
        anim &= Animation(z=factor)

        anim.start(self.cube.scale)
