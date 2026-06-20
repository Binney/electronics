from math import pi, cos, sin

import app

from events.input import Buttons, BUTTON_TYPES

DISPLAY_SIZE = 240
r1 = 103
r2 = 90

def arrow(size, skew, thickness, x, y, angle):
    points = [(0, 0), (size, skew), (size + thickness, skew), (thickness, 0), (size + thickness, -skew), (size, -skew)]
    points = [(p[0] - size * 1.5 // 2, p[1]) for p in points]
    points = [
        (int(round(px * cos(angle) - py * sin(angle))),
         int(round(px * sin(angle) + py * cos(angle))))
        for px, py in points
    ]
    points = [(p[0] + x, p[1] + y) for p in points]
    return points

def draw_polygon(ctx, points, fill_color):
    ctx.move_to(points[0][0], points[0][1])
    for point in points[1:]:
        ctx.line_to(point[0], point[1])
    ctx.close_path()
    if fill_color is not None:
        ctx.rgb(*fill_color).fill()

def hex_to_tuple(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

nr_red = hex_to_tuple("#db010e")

class ExampleApp(app.App):
    def __init__(self):
        self.button_states = Buttons(self)

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays
            # open. Without it the app would close again immediately.
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        ctx.save()
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        # ctx.rgb(1, 0, 0).move_to(-80, 0).text("Hello world")
        # ctx.rgb(0,0,1).move_to(-80,0).line_to(80,0).line_to(0,80).close_path().stroke()
        ctx.line_width = 5.0
        ctx.rgb(1, 0, 0).arc(0, 0, r1, 0, 2 * pi, True).stroke()
        ctx.rgb(1, 0, 0).arc(0, 0, r2, 0, 2 * pi, True).stroke()
        # triangle = [[-80, 0], [80, 0], [0, 80]]
        # draw_polygon(ctx, triangle, (0, 1, 0))
        angle = 0
        sec_hand_coords = (DISPLAY_SIZE // 2 + int((r1 + 1) * -1 * sin(angle)),
                       DISPLAY_SIZE // 2 + int((r1 + 1) * cos(angle)))
        arr1 = arrow(25, 11, 10, 0, 80, angle)
        draw_polygon(ctx, arr1, nr_red)
        ctx.restore()


__app_export__ = ExampleApp