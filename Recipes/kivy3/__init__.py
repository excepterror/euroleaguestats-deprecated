from pythonforandroid.recipe import PythonRecipe
import shutil


class Kivy3Recipe(PythonRecipe):

    version = 'master'
    url = 'https://github.com/KeyWeeUsr/kivy3/archive/{version}.zip'

    depends = ['kivy']

    site_packages_name = 'kivy3'

    '''Due to setuptools.'''
    call_hostpython_via_targetpython = False

    def build_arch(self, arch):
        super().build_arch(arch)

        shutil.copyfile(self.get_build_dir(arch.arch) + '/kivy3/default.glsl', self.get_build_dir(arch.arch).split('/other_builds')[0] + '/python-installs/euroleaguestats/kivy3/default.glsl')

recipe = Kivy3Recipe()
