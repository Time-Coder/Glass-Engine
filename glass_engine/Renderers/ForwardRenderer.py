from .CommonRenderer import CommonRenderer
from glass import GLConfig, sampler2D

        
class ForwardRenderer(CommonRenderer):

    def __init__(self):
        CommonRenderer.__init__(self)

    def startup(self):
        CommonRenderer.startup(self)
        screen = self.camera.screen
        if not screen._samples_set_by_user and not screen._is_gl_init:
            screen._set_samples(4)

    def draw_opaque(self):
        if not self._opaque_meshes and \
           not self._opaque_lines and \
           not self._opaque_points:
            return

        with GLConfig.LocalConfig(depth_test=True, blend=False):
            with self.OIT_fbo:
                GLConfig.clear_buffers()

                if self._opaque_meshes:
                    self.prepare_forward_draw_mesh(True)
                    for mesh, instances in self._opaque_meshes:
                        self.forward_draw_mesh(mesh, instances)

                if self._opaque_lines:
                    self.prepare_forward_draw_lines(True)
                    for mesh, instances in self._opaque_lines:
                        self.forward_draw_lines(mesh, instances)

                if self._opaque_points:
                    self.prepare_forward_draw_points(True)
                    for mesh, instances in self._opaque_points:
                        self.forward_draw_points(mesh, instances)

                # 绘制天空盒
                if self.scene.skybox.is_completed:
                    self.scene.skybox.draw(self.camera)

                # 绘制天空穹顶
                elif self.scene.skydome.is_completed:
                    self.scene.skydome.draw(self.camera)

        self.OIT_fbo.draw_to_active(0)

        resolved = self.OIT_fbo.resolved
        self._depth_map = resolved.depth_attachment
        self._view_pos_map = resolved.color_attachment(3)
        self._view_normal_map = resolved.color_attachment(4)
    
    def render(self):
        # profiler.enable()
        self._should_update = False
        sampler2D._should_update = False
        self.classify_meshes()
        self.update_dir_lights_depth()
        self.update_point_lights_depth()
        self.update_spot_lights_depth()
        self.draw_opaque()
        self.draw_transparent()
        # profiler.disable()
        return (self._should_update or sampler2D._should_update)
