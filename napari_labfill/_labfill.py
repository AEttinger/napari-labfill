import napari

viewer = napari.Viewer()

points_layer = viewer.add_points()


@points_layer.mouse_drag_callbacks.append
def mark_point(layer, event):
    # print(event)
    if event.type == 'mouse_press':
        print('press')
        print(event.pos)


napari.run()
