import wx
import wx.glcanvas as glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluPerspective
import numpy as np

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        attribs = [glcanvas.WX_GL_RGBA, glcanvas.WX_GL_DOUBLEBUFFER, glcanvas.WX_GL_DEPTH_SIZE, 16, 0]
        super().__init__(parent, attribList=attribs)

        self.context = glcanvas.GLContext(self)
        self.angle = 0
        self.rotating = False
        self.timer = wx.Timer(self)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

    def init_gl(self):
        """ Initialize OpenGL settings. """
        self.SetCurrent(self.context)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.2, 0.3, 1.0)  # Background color

    def on_paint(self, event):
        self.SetCurrent(self.context)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)  # Move cube back
        glRotatef(self.angle, 1, 1, 0)  # Rotate cube

        self.draw_cube()
        self.SwapBuffers()

    def draw_cube(self):
        """ Draw a simple 3D cube with colored faces. """
        vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Back face
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]   # Front face
        ], dtype=np.float32)

        edges = np.array([
            [0, 1], [1, 2], [2, 3], [3, 0],  # Back
            [4, 5], [5, 6], [6, 7], [7, 4],  # Front
            [0, 4], [1, 5], [2, 6], [3, 7]   # Connections
        ], dtype=np.int32)

        colors = [
            (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
            (1, 0, 1), (0, 1, 1), (1, 1, 1), (0.5, 0.5, 0.5)
        ]

        glBegin(GL_QUADS)
        for i, face in enumerate([(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
                                  (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)]):
            glColor3fv(colors[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    def on_size(self, event):
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = size.width / size.height if size.height > 0 else 1
        gluPerspective(45, aspect, 1, 100)
        glMatrixMode(GL_MODELVIEW)

    def on_timer(self, event):
        """ Update rotation angle when timer is running. """
        if self.rotating:
            self.angle += 2
            self.Refresh()

    def toggle_rotation(self):
        """ Start/Stop cube rotation. """
        self.rotating = not self.rotating
        if self.rotating:
            self.timer.Start(16)  # Approx. 60 FPS
        else:
            self.timer.Stop()


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="wxPython OpenGL Cube", size=(800, 600))

        splitter = wx.SplitterWindow(self)
        panel = wx.Panel(splitter, style=wx.BORDER_SIMPLE)
        self.gl_canvas = OpenGLCanvas(splitter)

        # Side panel layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.toggle_btn = wx.Button(panel, label="Start Rotation")
        self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle_rotation)

        sizer.Add(self.toggle_btn, 0, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # Split window: side panel (left) and OpenGL context (right)
        splitter.SplitVertically(panel, self.gl_canvas, 200)
        splitter.SetSashGravity(0.2)

        self.Bind(wx.EVT_SHOW, self.on_show)

    def on_show(self, event):
        """ Ensure OpenGL initializes when window first appears. """
        if event.IsShown():
            self.gl_canvas.init_gl()

    def on_toggle_rotation(self, event):
        """ Handle button press to start/stop rotation. """
        self.gl_canvas.toggle_rotation()
        self.toggle_btn.SetLabel("Stop Rotation" if self.gl_canvas.rotating else "Start Rotation")


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
